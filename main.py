import random
import threading
from paho.mqtt import client as mqtt_client
from colorama import Fore, Style, init

init(autoreset=True)  # Mengatur otomatis untuk mereset warna setelah penggunaan

broker = 'broker.emqx.io'
port = 1883
topic = "chat/82812181"
client_id = input("Enter your name: ")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"{Fore.GREEN}{client_id} connected to MQTT Broker!")
        else:
            print(f"{Fore.RED}Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        sender = message.split(":")[0]  # Ambil nama pengirim dari pesan
        if sender == client_id:
            # Jika pengirim adalah Anda sendiri, cetak dengan warna biru
            print(f"{Fore.BLUE}{message}")
        else:
            # Jika pengirim orang lain, cetak dengan warna kuning
            print(f"{Fore.YELLOW}{message}")

    client.subscribe(topic)
    client.on_message = on_message

def publish(client: mqtt_client):
    while True:
        msg = input()
        formatted_msg = f"{client_id}: {msg}"
        client.publish(topic, formatted_msg, retain=True)  # Tambahkan retain=True

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    publish(client)
    client.loop_stop()

if __name__ == '__main__':
    run()