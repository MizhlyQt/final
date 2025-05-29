import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json

def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("casa_inteligente56")
client1.on_message = on_message

page_style = """
<style>
/* Fondo principal */
[data-testid="stAppViewContainer"] {
    background-color: #1b3d1e;
}

/* Fondo del sidebar */
[data-testid="stSidebar"] {
    background-color: #38633c;
}

/* Color de todos los textos */
[data-testid="stMarkdownContainer"] {
    color: #ffffff;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# Título principal
st.title("Control por Voz 🔊")


st.markdown("""
**Instrucciones**  
Haz clic en el botón y di alguno de los siguientes comandos:  
- "enciende Las luces"  
- "apaga Las luces"  
- "escuchar La Musica"  
""")


image1 = Image.open("prendidas.png")
st.image(image1, caption="Luces encendidas", width=100)


st.write("Toca el botón y habla:")

stt_button = Button(label="🎤 Inicio", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", { detail: value }));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        comando = result.get("GET_TEXT").strip()
        st.write(f"Comando recibido: {comando}")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": comando})
        ret = client1.publish("casa_inteligente", comando)

    try:
        os.mkdir("temp")
    except:
        pass
