import socket
import json
import uuid
from threading import Thread
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(5)
print("Server is listening on port 12345...")

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

Thread(target=broadcast_positions, daemon=True).start()

while True:
    client_socket, client_address = server_socket.accept()
    Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
