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
        # Limpieza más robusta del mensaje
        mensaje = str(mensaje).lower().strip().replace(".", "").replace("!", "").replace("?", "")
        mqtt.single(MQTT_TOPIC, mensaje, hostname=MQTT_BROKER)
        st.success(f"✅ Comando enviado: {mensaje}")
    except Exception as e:
        st.error(f"❌ Error al enviar: {str(e)}")

# Configuración de la página
st.set_page_config(page_title="Control Casa Inteligente", layout="centered")
st.title("🏠 Control de Casa Inteligente")

# Instrucciones mejoradas
st.markdown("""
**🗣️ Comandos de voz que funcionan (di exactamente):**
- "enciende las luces"
- "apaga las luces"
- "abre la puerta"
- "cierra la puerta"

*El sistema es sensible a mayúsculas y signos de puntuación.*
""")

# Modo de control
modo = st.radio("Modo de control:", ["🎤 Voz", "⌨️ Botones"], horizontal=True, key="modo_control")

if modo == "🎤 Voz":
    st.subheader("Control por Voz")
    st.write("Presiona el botón y di claramente uno de los comandos:")
    
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
    
    result = streamlit_bokeh_events(
        voice_btn,
        events="GET_TEXT",
        key="voice_control"
    )
    
    if result and "GET_TEXT" in result:
        comando = str(result.get("GET_TEXT", ""))
        comando_limpio = comando.lower().strip().replace(".", "").replace("!", "").replace("?", "")
        
        st.info(f"🎤 Detectado: '{comando}'")
        
        # Lista de comandos aceptados (en minúsculas y sin puntuación)
        comandos_aceptados = [
            "enciende las luces",
            "apaga las luces",
            "abre la puerta",
            "cierra la puerta"
        ]
        
        if comando_limpio in comandos_aceptados:
            enviar_comando(comando_limpio)
        else:
            st.warning(f"""
            Comando no reconocido. Prueba con:
            - "enciende las luces"
            - "apaga las luces"
            - "abre la puerta"
            - "cierra la puerta"
            """)

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
