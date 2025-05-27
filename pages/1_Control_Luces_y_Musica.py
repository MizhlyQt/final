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
        # Conversión robusta a minúsculas y limpieza
        mensaje = str(mensaje).lower().strip()
        # Eliminar puntos, signos de exclamación, etc.
        mensaje = ''.join(c for c in mensaje if c.isalpha() or c.isspace())
        mqtt.single(MQTT_TOPIC, mensaje, hostname=MQTT_BROKER)
        st.success(f"✅ Comando enviado: {mensaje}")
    except Exception as e:
        st.error(f"❌ Error al enviar: {str(e)}")

# Configuración de la página
st.set_page_config(page_title="Control de Música", layout="centered")
st.title("🎵 Control de Música")

# Instrucciones mejoradas
st.markdown("""
**🗣️ Comandos de voz que funcionan:**
- "play musica" (o "reproduce música")
- "stop musica" (o "pausa música")
- "enciende luces"
- "apaga luces"

*Di el comando naturalmente, el sistema entenderá aunque uses mayúsculas.*
""")

# Modo de control
modo = st.radio("Modo de control:", ["🎤 Voz", "⌨️ Botones"], horizontal=True, key="modo_control")

if modo == "🎤 Voz":
    st.subheader("Control por Voz")
    st.write("Presiona el botón y di el comando:")
    
    voice_btn = Button(label=" 🎤 HABLAR AHORA ", width=300, button_type="success")
    voice_btn.js_on_event("button_click", CustomJS(code="""
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.onresult = function(e) {
            const value = String(e.results[0][0].transcript || '').toLowerCase();
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
        comando_recibido = str(result.get("GET_TEXT", ""))
        # Limpieza adicional
        comando = comando_recibido.lower().strip()
        comando = ' '.join(comando.split())  # Elimina espacios múltiples
        
        st.info(f"🎤 Detectado: '{comando_recibido}'")
        
        # Diccionario de coincidencias flexibles
        comandos = {
            # Comandos de música
            "play musica": "play",
            "reproduce musica": "play",
            "inicia musica": "play",
            "para musica": "stop",
            "stop musica": "stop",
            "pausa musica": "stop",
            
            # Comandos de luces
            "enciende luces": "luces on",
            "prende luces": "luces on",
            "apaga luces": "luces off"
        }
        
        # Buscar la mejor coincidencia
        comando_enviar = None
        for clave in comandos:
            if clave in comando:
                comando_enviar = comandos[clave]
                break
        
        if comando_enviar:
            enviar_comando(comando_enviar)
        else:
            st.warning("""
            Comando no reconocido. Prueba con:
            - "play musica" o "reproduce música"
            - "stop musica" o "pausa música"
            - "enciende luces"
            - "apaga luces"
            """)

else:
    st.subheader("Control por Botones")
    col1, col2 = st.columns(2)
    
    with col1:
        dispositivo = st.selectbox("Controlar:", ["música", "luces"])
    
    with col2:
        if dispositivo == "música":
            accion = st.radio("Acción música:", ["play", "stop"], horizontal=True)
            comando = f"{accion} musica"
        else:
            accion = st.radio("Acción luces:", ["enciende", "apaga"], horizontal=True)
            comando = f"{accion} luces"
    
    if st.button("🚀 Enviar Comando", type="primary"):
        enviar_comando(comando)

# Footer
st.markdown("---")
st.caption(f"🔗 Conectado a: {MQTT_BROKER} | 📡 Topic: {MQTT_TOPIC}")
# Footer
st.markdown("---")
st.caption(f"🔗 Conectado a: {MQTT_BROKER} | 📡 Topic: {MQTT_TOPIC}")
