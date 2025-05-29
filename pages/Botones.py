import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
from PIL import Image  # Para manejar imágenes

# Configuración de la página
st.set_page_config(
    page_title="Control Casa Inteligente",
    page_icon="🏠",
    layout="centered"
)

# Mostrar versión de Python
st.sidebar.write(f"🧑‍💻 Versión de Python: {platform.python_version()}")

# Logo o imagen (puedes reemplazar la URL por una imagen local)
st.image("https://cdn-icons-png.flaticon.com/512/3094/3094843.png", width=100)

# Título principal con emojis
st.title("🏠 Control Casa Inteligente 🎛️")
st.subheader("Controla tus dispositivos IoT mediante MQTT")

# División visual
st.markdown("---")

# Variables (manteniendo tu código original)
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Sección de controles
st.header("🛠️ Controles Principales")

# Botones con estilo mejorado
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('💡 Encender Luces', key='encender', help="Activa las luces de la casa"):
        act1 = "ON"
        client1 = paho.Client("casa_inteligente56")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("casa_inteligente", "enciende Las luces")
        st.toast('¡Luces encendidas!', icon='💡')

with col2:
    if st.button('🌙 Apagar Luces', key='apagar', help="Desactiva las luces de la casa"):
        act1 = "OFF"
        client1 = paho.Client("casa_inteligente56")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("casa_inteligente", "apaga Las luces")
        st.toast('Luces apagadas', icon='🌙')

with col3:
    if st.button('🎵 Escuchar Música', key='musica', help="Reproduce una melodía"):
        act1 = "OFF"
        client1 = paho.Client("casa_inteligente56")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("casa_inteligente", "escuchar La Musica")
        st.toast('Reproduciendo música...', icon='🎵')

# Sección de control de intensidad
st.markdown("---")
st.header("🎚️ Control de Intensidad")
values = st.slider('Ajusta la intensidad de las luces', 0.0, 100.0, 50.0, help="Controla el nivel de brillo")
st.write(f'Valor seleccionado: {values}%')

if st.button('⚡ Enviar Intensidad', key='intensidad'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
    st.toast(f'Intensidad ajustada al {values}%', icon='⚡')

# Pie de página
st.markdown("---")
st.caption("Sistema de control MQTT para casa inteligente | © 2023")
