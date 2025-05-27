import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# Configuración MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando(mensaje):
    """Envía comandos a Wokwi"""
    try:
        mensaje = str(mensaje).lower().strip()
        mqtt.single(MQTT_TOPIC, mensaje, hostname=MQTT_BROKER)
        st.success(f"✅ Comando enviado: {mensaje}")
    except Exception as e:
        st.error(f"❌ Error al enviar: {str(e)}")

# Configuración de la página
st.set_page_config(page_title="Control Casa Inteligente", layout="centered")
st.title("🏠 Control de Casa Inteligente")

# Modo de control - Manteniendo ambos sistemas
modo = st.radio("Modo de control:", ["🎤 Voz", "⌨️ Botones"], horizontal=True, key="modo_control")

if modo == "🎤 Voz":
    st.subheader("Control por Voz")
    st.write("Presiona el botón y di claramente:")
    
    # Botón de voz simplificado (sin parámetros problemáticos)
    voice_btn = Button(label=" 🎤 HABLAR AHORA ", width=300, button_type="success")
    voice_btn.js_on_event("button_click", CustomJS(code="""
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.onresult = function(e) {
            const value = String(e.results[0][0].transcript || '');
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
        recognition.start();
    """))
    
    # Configuración mínima de eventos
    result = streamlit_bokeh_events(
        voice_btn,
        events="GET_TEXT",
        key="voice_control"
    )
    
    if result and "GET_TEXT" in result:
        comando = str(result.get("GET_TEXT", "")).strip()
        if comando:
            st.info(f"🎤 Comando detectado: '{comando}'")
            # Traducción de comandos de voz
            if "enciende" in comando and "luces" in comando:
                enviar_comando("enciende las luces")
            elif "apaga" in comando and "luces" in comando:
                enviar_comando("apaga las luces")
            elif "abre" in comando and "puerta" in comando:
                enviar_comando("abre la puerta")
            elif "cierra" in comando and "puerta" in comando:
                enviar_comando("cierra la puerta")
            else:
                st.warning("Comando no reconocido")

else:
    st.subheader("Control por Botones")
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
