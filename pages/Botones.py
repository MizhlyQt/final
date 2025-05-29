import paho.mqtt.client as paho
import streamlit as st
import platform
from PIL import Image  # Para manejar imágenes

# Configuración básica de la página
st.set_page_config(
    page_title="Control Casa Inteligente",
    page_icon="🏠",
    layout="centered"
)

# Logo o imagen (puedes reemplazar por una imagen local)
st.image("https://cdn-icons-png.flaticon.com/512/3094/3094843.png", width=100)

# Título principal
st.title("🏠 Control Casa Inteligente")
st.markdown("Controla tus dispositivos IoT mediante **MQTT**")
st.markdown("---")

# Variables (manteniendo tu código original)
def on_publish(client, userdata, result):
    print("El dato ha sido publicado")

broker = "broker.mqttdashboard.com"
port = 1883

# Controles principales
st.header("Controles de Dispositivos")

# Botón para encender luces
if st.button('💡 ENCENDER LUCES', help="Activa las luces de la casa"):
    client1 = paho.Client("casa_inteligente56")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    client1.publish("casa_inteligente", "enciende Las luces")
    st.success("Comando enviado: Encender luces")

# Botón para apagar luces
if st.button('🌙 APAGAR LUCES', help="Desactiva las luces de la casa"):
    client1 = paho.Client("casa_inteligente56")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    client1.publish("casa_inteligente", "apaga Las luces")
    st.success("Comando enviado: Apagar luces")

# Botón para reproducir música
if st.button('🎵 REPRODUCIR MÚSICA', help="Activa el reproductor de música"):
    client1 = paho.Client("casa_inteligente56")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    client1.publish("casa_inteligente", "escuchar La Musica")
    st.success("Comando enviado: Reproducir música")

# Información adicional
st.markdown("---")
st.markdown("**Configuración:**")
st.caption(f"📌 Broker MQTT: {broker}")
st.caption(f"📌 Tópico: casa_inteligente")
st.caption(f"🐍 Python v{platform.python_version()}")

# Estilo CSS adicional para mejorar los botones
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        padding: 10px !important;
        margin: 5px 0;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)
