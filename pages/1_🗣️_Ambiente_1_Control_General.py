import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# Configuración MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando(mensaje):
    """Envía comandos a Wokwi y muestra feedback en Streamlit"""
    try:
        # Asegurarnos que el mensaje es un string
        if not isinstance(mensaje, str):
            mensaje = str(mensaje)
            
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

# Configuración de la página
st.set_page_config(page_title="Control por Voz", layout="centered")
st.title("🎤 Control por Voz - Casa Inteligente")

# Botón de voz con manejo robusto de errores
voice_btn = Button(label=" 🎤 HABLAR ", width=200, button_type="success")
voice_btn.js_on_event("button_click", CustomJS(code="""
    try {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = function(e) {
            const value = String(e.results[0][0].transcript || ''); // Asegurar string
            if (value.trim()) {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        };

        recognition.onerror = function(e) {
            document.dispatchEvent(new CustomEvent("ERROR", {detail: String(e.error)}));
        };

        recognition.start();
    } catch(error) {
        document.dispatchEvent(new CustomEvent("ERROR", {detail: String(error)}));
    }
"""))

# Procesamiento seguro de resultados
result = streamlit_bokeh_events(
    voice_btn,
    events=["GET_TEXT", "ERROR"],
    key="voice_control",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        comando = str(result.get("GET_TEXT", "")).strip()
        if comando:
            st.info(f"🎤 Detectado: '{comando}'")
            enviar_comando(comando)
    
    if "ERROR" in result:
        error = str(result.get("ERROR", "Error desconocido"))
        st.error(f"🔇 Error: {error}")

# Instrucciones
st.markdown("""
**Instrucciones:**
1. Haz clic en el botón **HABLAR**
2. Di claramente:
   - *"Enciende las luces"*
   - *"Apaga las luces"*
   - *"Abre la puerta"*
   - *"Cierra la puerta"*
""")

