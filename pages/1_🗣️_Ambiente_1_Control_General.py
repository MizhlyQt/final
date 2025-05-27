import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# 1. Configuración MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando(mensaje):
    """Función segura para enviar comandos"""
    try:
        # Conversión y limpieza robusta del mensaje
        mensaje = str(mensaje).lower().strip() if mensaje else ""
        
        # Validación de comandos sin split()
        if not mensaje:
            st.warning("No se detectó comando")
            return
            
        if "enciende" in mensaje and "luces" in mensaje:
            mqtt.single(MQTT_TOPIC, "enciende las luces", hostname=MQTT_BROKER)
            st.success("✅ Luces encendidas")
        elif "apaga" in mensaje and "luces" in mensaje:
            mqtt.single(MQTT_TOPIC, "apaga las luces", hostname=MQTT_BROKER)
            st.success("✅ Luces apagadas")
        elif "abre" in mensaje and "puerta" in mensaje:
            mqtt.single(MQTT_TOPIC, "abre la puerta", hostname=MQTT_BROKER)
            st.success("✅ Puerta abierta")
        elif "cierra" in mensaje and "puerta" in mensaje:
            mqtt.single(MQTT_TOPIC, "cierra la puerta", hostname=MQTT_BROKER)
            st.success("✅ Puerta cerrada")
        else:
            st.warning("Comando no válido. Ejemplos: 'Enciende las luces', 'Abre la puerta'")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# 2. Interfaz de usuario
st.set_page_config(page_title="Control por Voz", layout="centered")
st.title("🏠 Control por Voz")

# 3. Botón de voz mejorado
voice_btn = Button(label=" 🎤 HABLAR ", width=200, button_type="success")
voice_btn.js_on_event("button_click", CustomJS(code="""
    try {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.maxAlternatives = 1;
        
        recognition.onresult = function(e) {
            const transcript = e.results[0][0].transcript;
            document.dispatchEvent(new CustomEvent("GET_TEXT", {
                detail: transcript || ""
            }));
        };
        
        recognition.onerror = function(e) {
            console.error("Error de voz:", e.error);
            document.dispatchEvent(new CustomEvent("ERROR", {
                detail: "Error de micrófono: " + e.error
            }));
        };
        
        recognition.start();
    } catch(error) {
        document.dispatchEvent(new CustomEvent("ERROR", {
            detail: "Error inicializando: " + error
        }));
    }
"""))

# 4. Manejo de eventos seguro
result = streamlit_bokeh_events(
    voice_btn,
    events=["GET_TEXT", "ERROR"],
    key="voice",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# 5. Procesamiento a prueba de errores
if result:
    if "GET_TEXT" in result:
        texto = result.get("GET_TEXT")
        if isinstance(texto, str):  # Verificación crucial
            enviar_comando(texto)
        else:
            st.error("Error: El comando no es texto válido")
    
    if "ERROR" in result:
        error = result.get("ERROR")
        st.error(f"Error de voz: {str(error)}")

# 6. Instrucciones
st.markdown("""
**Comandos válidos:**
- Enciende las luces
- Apaga las luces
- Abre la puerta
- Cierra la puerta
""")
