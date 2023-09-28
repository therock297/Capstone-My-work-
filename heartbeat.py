import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Settings
mqtt_broker = "mqtt.example.com"  # Replace with your MQTT broker address
mqtt_port = 1883  # Replace with your MQTT broker port
mqtt_topic = "bike/000001/heartrate"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    if msg.topic == mqtt_topic:
        heart_payload = msg.payload.decode('utf-8')
        dict_of_heart_payload = json.loads(heart_payload)
        heart = dict_of_heart_payload["value"]
        print("Received " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        heartbeat_rate_var.set(f"{heart} BPM")

# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Heartbeat Monitor")
root.geometry("400x400")

# Heartbeat Rate Label and Entry
heartbeat_rate_label = tk.Label(root, text="Heartbeat Rate:", font=("Helvetica", 16))
heartbeat_rate_label.place(x=30, y=280)
heartbeat_rate_var = tk.StringVar()
heartbeat_rate_var.set(0)  # Default value for heartbeat rate as zero
heartbeat_rate_entry = ttk.Entry(root, textvariable=heartbeat_rate_var, font=("Helvetica", 16))
heartbeat_rate_entry.place(x=210, y=280)

def generate_and_publish_heartbeat():
    while True:
        # Simulate a random heartbeat value
        heartbeat_value = random.randint(60, 120)

        # Publish the heartbeat value to MQTT
        payload = json.dumps({"value": heartbeat_value})
        mqtt_client.publish(mqtt_topic, payload)

        # Update the GUI
        heartbeat_rate_var.set(f"{heartbeat_value} BPM")

        # Sleep for a few seconds before generating the next heartbeat
        time.sleep(5)

# Start the MQTT client loop in a separate thread
mqtt_client.loop_start()

# Start generating and publishing heartbeats
generate_and_publish_heartbeat_thread = threading.Thread(target=generate_and_publish_heartbeat)
generate_and_publish_heartbeat_thread.daemon = True
generate_and_publish_heartbeat_thread.start()

root.mainloop()
