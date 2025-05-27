import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import paho.mqtt.publish as mqtt

# 1. Configuración MQTT segura
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_comando_simple(comando):
    """Versión simplificada y robusta para Wokwi"""
    try:
        comando = str(comando).strip().lower()
        if comando in ["enciende las luces", "apaga las luces", 
                      "abre la puerta", "cierra la puerta"]:
            mqtt.single(MQTT_TOPIC, comando, hostname=MQTT_BROKER)
            st.success(f"✅ Enviado: {comando}")
        else:
            st.warning(f"⚠️ Comando no reconocido: '{comando}'")
    except Exception as e:
        st.error(f"❌ Error MQTT: {str(e)}")

# 2. Configuración de página minimalista
st.set_page_config(page_title="Control Voz", layout="centered")
st.title("🎤 Control por Voz")
st.write("Presiona el botón y di un comando:")

# 3. Implementación alternativa segura
try:
    # Botón de voz ultra-simplificado
    voice_btn = Button(label=" 🎤 HABLAR ", width=200, button_type="success")
    voice_btn.js_on_event("button_click", CustomJS(code="""
        try {
            const rec = new webkitSpeechRecognition();
            rec.lang = 'es-ES';
            rec.onresult = e => {
                const text = e.results[0][0].transcript;
                document.dispatchEvent(new CustomEvent("VOICE_TEXT", {detail: text}));
            };
            rec.start();
        } catch(err) {
            console.error("Voice error:", err);
        }
    """))

    # Manejo de eventos con verificación extrema
    event_result = streamlit_bokeh_events(
        voice_btn,
        events="VOICE_TEXT",
        key="voice_control",
        refresh_on_update=True,
        override_height=75,
        debounce_time=100
    )

    if event_result and "VOICE_TEXT" in event_result:
        texto = str(event_result.get("VOICE_TEXT", "")).strip()
        if texto:
            enviar_comando_simple(texto)

except Exception as e:
    st.error(f"Error inicializando control de voz: {str(e)}")
    st.info("Como alternativa, escribe el comando:")
    comando_manual = st.text_input("Comando:")
    if comando_manual:
        enviar_comando_simple(comando_manual)

# 4. Comandos de ejemplo
st.markdown("""
**Comandos válidos:**
- `Enciende las luces`
- `Apaga las luces`
- `Abre la puerta`
- `Cierra la puerta`
""")
