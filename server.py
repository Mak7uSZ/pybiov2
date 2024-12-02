import socket
import threading
import random
import socket
import time
from PIL import Image, ImageEnhance
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import *
from ursina.lights import DirectionalLight
from threading import Thread
import keyboard
from ursina.texture_importer import load_texture
from ursina import *

# Broadcast the position of each player to all other clients

# Handle a single client connection
import socket
import json

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(5)
print("Server is listening on port 12345...")

clients = []

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    clients.append(client_socket)

    while True:
        try:
            # Receive the player's position data (in JSON format)
            data = client_socket.recv(4096)
            if data:
                position_data = json.loads(data.decode('utf-8'))  # Convert back to dictionary
                print(f"Received position from {addr}: {position_data}")
                # Broadcast the position to other clients if needed
                for c in clients:
                    if c != client_socket:  # Don't send position back to the same client
                        c.send(json.dumps(position_data).encode('utf-8'))
            else:
                break
        except:
            break

    print(f"Connection from {addr} closed")

def start_server():
    while True:
        client_socket, addr = server_socket.accept()
        handle_client(client_socket, addr)

if __name__ == "__main__":
    start_server()
