import streamlit as st
import paho.mqtt.publish as mqtt

# Configuración MQTT
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_valor_bar_graph(valor):
    try:
        mqtt.single(MQTT_TOPIC, f"bar {valor}", hostname=MQTT_BROKER)
        st.success(f"📊 Valor enviado: {valor}%")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Interfaz
st.set_page_config(page_title="Control LED Bar Graph", layout="centered")
st.title("📊 Control LED Bar Graph")
st.markdown("Ajusta el slider para controlar los LEDs en Wokwi:")

valor = st.slider(
    "Nivel de intensidad:",
    min_value=0,
    max_value=100,
    value=50,
    step=5,
    format="%d%%"
)

if st.button("Enviar", type="primary"):
    enviar_valor_bar_graph(valor)

# Simulación visual opcional
st.write("---")
st.subheader("Simulación Bar Graph")
st.write(f"🔵 LEDs encendidos: {valor // 12 + 1} de 8")  # 100% ≈ 8 LEDs
