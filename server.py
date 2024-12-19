import socket
import json
import uuid
from threading import Thread
import time
import part1
from part1 import MainMenu
import random


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
import hashlib
def generate_port(key: str) -> int:
    # Генерируем порт, используя хеш-значение от ключа
    hash_value = hashlib.sha256(key.encode()).hexdigest()
    port = int(hash_value[:5], 16) % 65535  # Берем первые 5 символов хеша и приводим к диапазону портов
    if port < 1024:  # Избегаем системных портов
        port += 1024
    return port

# Пример использования
key = "unique-server-key"
random_port = generate_port(key)
print(f"Generated port: {random_port}")

server_socket.bind(("0.0.0.0", random_port))
server_socket.listen(5)
print(f"Server is listening on port {random_port}...")

clients = {}  # Сопоставление client_socket -> client_id
clients_positions = {}

def handle_client(client_socket, client_address):
    global clients, clients_positions

    # Генерируем уникальный ID клиента
    client_id = str(uuid.uuid4())
    clients[client_socket] = client_id
    print(f"[INFO] New connection from {client_address}, assigned ID: {client_id}")

    # Отправляем клиенту его ID
    client_socket.send(json.dumps(client_id).encode('utf-8'))

    while True:
        try:
            data = client_socket.recv(4096)
            if data:
                position_data = json.loads(data.decode('utf-8'))
                clients_positions[client_id] = position_data
                print(f"[DEBUG] Received position from {client_id}: {position_data}")
            else:
                break
        except Exception as e:
            print(f"[ERROR] Error with client {client_id}: {e}")
            break

    # Удаляем клиента при отключении
    print(f"[INFO] Connection from {client_id} closed")
    del clients_positions[client_id]
    del clients[client_socket]
    client_socket.close()

def broadcast_positions():
    while True:
        if clients_positions:
            positions_data = json.dumps(clients_positions)
            for client_socket in list(clients.keys()):
                try:
                    client_socket.sendall(positions_data.encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Error sending data to client {clients[client_socket]}: {e}")
                    del clients[client_socket]
        time.sleep(0.1)

servertijd = 0

def update_servertijd():
    global servertijd
    while True:
        servertijd += 1

        if servertijd > 239:
            servertijd = 0

        time.sleep(1)

def broadcast_tijd():
    while True:
        try:
            # Check if servertijd has a valid value
            if servertijd is not None:
                # Convert servertijd to JSON
                tijd_data = json.dumps(servertijd)
                
                # Broadcast to all connected clients
                for client_socket in list(clients.keys()):
                    try:
                        client_socket.sendall(tijd_data.encode('utf-8'))
                    except Exception as e:
                        print(f"[ERROR] Error sending tijd_data to client {clients[client_socket]}: {e}")
                        # Optionally remove the problematic client
                        del clients[client_socket]
        except Exception as e:
            print(f"[ERROR] Error in broadcast loop: {e}")
        
        # Wait a short period before the next broadcast
        time.sleep(0.1)

Thread(target=broadcast_positions, daemon=True).start()
Thread(target=update_servertijd, daemon=True).start()
Thread(target=broadcast_tijd, daemon=True).start()

while True:
    client_socket, client_address = server_socket.accept()
    Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


