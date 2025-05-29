import streamlit as st
import paho.mqtt.publish as mqtt

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "casa_inteligente"

def enviar_valor_bar_graph(valor):
    try:
        mqtt.single(MQTT_TOPIC, f"bar {valor}", hostname=MQTT_BROKER)
        st.success(f"📊 Valor enviado: {valor}% (LEDs encendidos: {valor // 10})")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.set_page_config(page_title="Control LED Bar Graph", layout="centered")
st.title("aaaa")

page_style = """
<style>
/* Fondo principal */
[data-testid="stAppViewContainer"] {
    background-color: #010f1c;
}

/* Fondo del sidebar */
[data-testid="stSidebar"] {
    background-color: #0a1f30;
}

/* Color de todos los textos */
[data-testid="stMarkdownContainer"] {
    color: #ffffff;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

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

st.write("---")
st.subheader("Simulación")
st.write(f"💡💡 LEDs encendidos: **{valor // 10}** de 10")
