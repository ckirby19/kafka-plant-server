import serial
from paho.mqtt import client as mqtt_client
import random
import time
from SignalHandler import SignalHandler

arduino_port = "/dev/ttyACM0"
broker = '192.168.0.106'
mqtt_port = 1883 #1883
topic = "moistureData"
client_id = f'python-mqtt-{random.randint(0,1000)}'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def run():
    signal_handler = SignalHandler()
    client = connect_mqtt()
    client.loop_start()
    ser = serial.Serial(arduino_port, 9600, timeout=3)
    while signal_handler.can_run():
        line = ser.readline()
        publish(client, topic, line)
    client.loop_stop()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.tls_set(ca_certs="./certs/ca.crt", certfile="./certs/server.crt", keyfile="./certs/server.key")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect


    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.connect(broker, mqtt_port)
    return client



def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        print("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as err:
            print("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print("Reconnect failed after %s attempts. Exiting...", reconnect_count)

def publish(client, topic, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Sent `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


if __name__ == "__main__":
    run()