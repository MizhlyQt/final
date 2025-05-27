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
st.set_page_config(page_title="Control de Música", layout="centered")
st.title("🎵 Control de Música")

# Instrucciones mejoradas con coincidencia flexible
st.markdown("""
**🗣️ Comandos de voz disponibles:**
- "enciende las luces" / "prende las luces"
- "apaga las luces"
- "play música" / "reproduce música" / "inicia música"
- "stop música" / "detén música" / "pausa música"

*El sistema reconoce variaciones de estos comandos.*
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
        
        # Diccionario de comandos aceptados con variaciones
        comandos_aceptados = {
            # Comandos de luces
            "enciende las luces": "luces on",
            "prende las luces": "luces on",
            "activa las luces": "luces on",
            "apaga las luces": "luces off",
            "desactiva las luces": "luces off",
            
            # Comandos de música
            "play musica": "play",
            "reproduce musica": "play",
            "inicia musica": "play",
            "comienza musica": "play",
            "stop musica": "stop",
            "deten musica": "stop",
            "pausa musica": "stop",
            "para musica": "stop"
        }
        
        # Buscar coincidencia flexible
        comando_encontrado = None
        for clave in comandos_aceptados:
            if clave in comando_limpio:
                comando_encontrado = comandos_aceptados[clave]
                break
        
        if comando_encontrado:
            enviar_comando(comando_encontrado)
        else:
            st.warning(f"""
            Comando no reconocido. Prueba con:
            - "enciende las luces"
            - "apaga las luces"
            - "play música"
            - "stop música"
            """)

else:
    st.subheader("Control por Botones")
    col1, col2 = st.columns(2)
    
    with col1:
        dispositivo = st.selectbox("Dispositivo:", ["luces", "música"])
    
    with col2:
        if dispositivo == "luces":
            accion = st.radio("Acción:", ["enciende", "apaga"], horizontal=True)
            comando = f"{accion} las luces"
        else:
            accion = st.radio("Acción:", ["play", "stop"], horizontal=True)
            comando = f"{accion} musica"
    
    if st.button("🚀 Enviar Comando", type="primary"):
        enviar_comando(comando)

# Footer
st.markdown("---")
st.caption(f"🔗 Conectado a: {MQTT_BROKER} | 📡 Topic: {MQTT_TOPIC}")
