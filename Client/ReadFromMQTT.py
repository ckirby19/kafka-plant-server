from paho.mqtt import client as mqtt_client
import random
from SignalHandler import SignalHandler
import asyncio
import websockets

broker = '192.168.0.101'
mqtt_port = 1883 #1883
topic = "moistureData"
client_id = f'python-mqtt-{random.randint(0,1000)}'
websocket_url = "ws://localhost:8765"

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

# Global variable to hold the websocket connection
ws = None
    
async def main():
    signal_handler = SignalHandler()
    await serve_websocket()
    client = connect_mqtt()
    client.loop_start()
    while signal_handler.can_run():
        await asyncio.sleep(1)
    client.loop_stop()
    
async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        print(message)
        
# Function to connect to WebSocket
async def serve_websocket():
    async with websockets.serve(handler, "", 8001):
        print("WebSocket server started on ws://0.0.0.0:8001")
        await asyncio.get_running_loop().create_future()  # run forever
    
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message from MQTT: {message}")
    asyncio.run(send_message(message))
        
# Function to send message over WebSocket
async def send_message(message):
    try:
        await websockets.send(message)
        print(f"Sent message over WebSocket: {message}")
    except Exception as e:
        print(f"Failed to send message over WebSocket: {e}")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, mqtt_port)
    client.subscribe(topic)
    return client


if __name__ == "__main__":
    print("RUNNING")
    asyncio.run(main())