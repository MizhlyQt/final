import paho.mqtt.client as mqtt
import json

broker = "broker.hivemq.com"
port = 1883
topic = "cami/centro/entretenimiento"

def enviar_estado_a_wokwi(estado):
    client = mqtt.Client()
    client.connect(broker, port)
    mensaje = json.dumps(estado)
    client.publish(topic, mensaje)
    client.disconnect()
