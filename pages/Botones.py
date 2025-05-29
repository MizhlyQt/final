import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
from PIL import Image

st.set_page_config(page_title="Control MQTT", page_icon="💡", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Panel de Control del centro multimedial 🎭 </h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 16px;'>"
    "En esta parte puedes controlar a través de botones las interacciones del centro multimedia."
    "</p>",
    unsafe_allow_html=True
)
st.markdown("---")

page_style = """
<style>
/* Fondo principal */
[data-testid="stAppViewContainer"] {
    background-color: #5697d5;
}

/* Fondo del sidebar */
[data-testid="stSidebar"] {
    background-color: #9fcefb;
}

/* Color de todos los textos */
[data-testid="stMarkdownContainer"] {
    color: #121314;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)
# Variables
values = 0.0
act1 = "OFF"

# Callbacks MQTT
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.success(f"Mensaje recibido: {message_received}")

# Configuración del broker
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# Contenedor de botones
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('💡 Encender luces'):
            act1 = "ON"
            client1 = paho.Client("casa_inteligente56")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"Act1": act1})
            ret = client1.publish("casa_inteligente", "enciende Las luces")
            st.success("Comando enviado: Encender luces")
        else:
            st.write("")

        image1 = Image.open("prendidas.png")
        st.image(image1, caption="Luces encendidas", width=100)

    with col2:
        if st.button('🔌 Apagar luces'):
            act1 = "OFF"
            client1 = paho.Client("casa_inteligente56")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"Act1": act1})
            ret = client1.publish("casa_inteligente", "apaga Las luces")
            st.success("Comando enviado: Apagar luces")
        else:
            st.write("")

        image2 = Image.open("Apagadas.png")
        st.image(image2, caption="Luces apagadas", width=100)

    with col3:
        if st.button('🎵 Escuchar música'):
            act1 = "OFF"
            client1 = paho.Client("casa_inteligente56")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)  
            message = json.dumps({"Act1": act1})
            ret = client1.publish("casa_inteligente", "escuchar La Musica")
            st.success("Comando enviado: Reproducir música")
        else:
            st.write("")

        image3 = Image.open("musica.png")
        st.image(image3, caption="Reproducir música", width=100)
