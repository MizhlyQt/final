import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# Configuración MQTT (broker público)
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando(mensaje):
    """Envía comandos a Wokwi y muestra feedback en Streamlit"""
    try:
        mensaje = mensaje.lower().strip()
        # Traduce comandos de voz a acciones específicas
        if "enciende" in mensaje and "luces" in mensaje:
            accion = "enciende las luces"
        elif "apaga" in mensaje and "luces" in mensaje:
            accion = "apaga las luces"
        elif "abre" in mensaje and "puerta" in mensaje:
            accion = "abre la puerta"
        elif "cierra" in mensaje and "puerta" in mensaje:
            accion = "cierra la puerta"
        else:
            st.warning("⚠️ Comando no reconocido. Di por ejemplo: 'Enciende las luces'")
            return

        mqtt.single(MQTT_TOPIC, accion, hostname=MQTT_BROKER)
        st.success(f"✅ Comando ejecutado: {accion}")
        
    except Exception as e:
        st.error(f"❌ Error al enviar: {str(e)}")

# Interfaz de usuario
st.set_page_config(page_title="Control por Voz", layout="centered")
st.title("🎤 Control por Voz - Casa Inteligente")
st.markdown("""
**Instrucciones:**
1. Haz clic en el botón **HABLAR**.
2. Di claramente:  
   - *"Enciende las luces"*  
   - *"Apaga las luces"*  
   - *"Abre la puerta"*  
   - *"Cierra la puerta"*
""")

# Botón de voz con configuración optimizada
voice_btn = Button(label=" 🎤 HABLAR ", width=200, button_type="success", css_classes=["voice-btn"])
voice_btn.js_on_event("button_click", CustomJS(code="""
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
        document.dispatchEvent(new CustomEvent("START_LISTENING"));
    };

    recognition.onresult = function(e) {
        const value = e.results[0][0].transcript;
        if (value) {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    };

    recognition.onerror = function(e) {
        document.dispatchEvent(new CustomEvent("ERROR", {detail: e.error}));
    };

    recognition.start();
"""))

# Captura eventos del botón
result = streamlit_bokeh_events(
    voice_btn,
    events=["GET_TEXT", "START_LISTENING", "ERROR"],
    key="voice_control",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Procesamiento de resultados
if result:
    if "GET_TEXT" in result:
        comando = result.get("GET_TEXT")
        st.info(f"🎤 Detectado: *'{comando}'*")
        enviar_comando(comando)
        
    elif "ERROR" in result:
        error = result.get("ERROR")
        st.error(f"🔇 Error de micrófono: {error}. Usa Chrome/Edge y permite acceso al micrófono.")

# Estilos CSS personalizados
st.markdown("""
<style>
.voice-btn {
    background: #FF4B4B !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
}
.voice-btn:hover {
    background: #FF0000 !important;
}
</style>
""", unsafe_allow_html=True)
