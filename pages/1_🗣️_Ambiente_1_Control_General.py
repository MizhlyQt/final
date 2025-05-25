import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# Configuración MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando(mensaje):
    try:
        mqtt.single(MQTT_TOPIC, mensaje.lower(), hostname=MQTT_BROKER)  # Envía en minúsculas
        st.success(f"✅ Comando enviado: '{mensaje}'")
    except Exception as e:
        st.error(f"❌ Error al enviar: {str(e)}")

# Interfaz de usuario
st.set_page_config(page_title="Control Casa Inteligente", layout="centered")
st.title("🏠 Control de Casa Inteligente")

# Modo de control
modo = st.radio("Modo de control:", ["🎤 Voz", "⌨️ Texto"], horizontal=True, key="modo_control")

if modo == "🎤 Voz":
    st.subheader("Control por Voz")
    st.write("Presiona el botón y di claramente:")
    
    voice_btn = Button(label=" 🎤 HABLAR AHORA ", width=300, button_type="success")
    
    voice_btn.js_on_event("button_click", CustomJS(code="""
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(e) {
            const value = e.results[0][0].transcript;
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
        
        recognition.start();
    """))
    
    result = streamlit_bokeh_events(
        voice_btn,
        events="GET_TEXT",
        key="voice_control",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0
    )
    
    if result and "GET_TEXT" in result:
        comando = result.get("GET_TEXT")
        st.info(f"🎤 Comando detectado: '{comando}'")
        enviar_comando(comando)

else:
    st.subheader("Control por Texto")
    col1, col2 = st.columns(2)
    
    with col1:
        dispositivo = st.selectbox("Dispositivo:", ["luces", "puerta"])
    
    with col2:
        if dispositivo == "luces":
            accion = st.radio("Acción:", ["enciende", "apaga"], horizontal=True)
        else:
            accion = st.radio("Acción:", ["abre", "cierra"], horizontal=True)
    
    if st.button("🚀 Enviar Comando", type="primary"):
        comando = f"{accion} las {dispositivo}"
        enviar_comando(comando)

# Footer
st.markdown("---")
st.caption(f"🔗 Conectado a: {MQTT_BROKER} | 📡 Topic: {MQTT_TOPIC}")
