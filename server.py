import socket
import json
import uuid
from threading import Thread
import time
import sys
import requests


# Get generated port from command-line arguments
generated_port = int(sys.argv[1])
print(f"Generated port: {generated_port}")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname) 

# Check server function
def check_server(local_ip, generated_port):
    """Check if the server is running and can accept connections"""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((local_ip, generated_port))
        server_socket.listen(5)
        client_socket, client_address = server_socket.accept()
        client_socket.close()
        return True
    except Exception as e:
        print(f"Error while checking server: {e}")
        return False

# Server status checking in a separate thread
def server_check_thread(local_ip, generated_port):
    while True:
        if check_server(local_ip, generated_port):
            print(f"Server is running on {local_ip}:{generated_port}")
        else:
            print(f"Failed to start the server on {local_ip}:{generated_port}")
        time.sleep(1)

clients_positions = {}
clients = {}

# Handle client function
def handle_client(client_socket, client_address):
    global clients, clients_positions
    client_id = str(uuid.uuid4())
    clients[client_socket] = client_id
    print(f"[INFO] New connection from {client_address}, assigned ID: {client_id}")
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

    print(f"[INFO] Connection from {client_id} closed")
    del clients_positions[client_id]
    del clients[client_socket]
    client_socket.close()

# Broadcast client positions to all clients
def broadcast_positions():
    while True:
        if clients_positions:
            positions_message = json.dumps({"type": "positions", "data": clients_positions})
            for client_socket in list(clients.keys()):
                try:
                    client_socket.sendall(positions_message.encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Error sending data to client {clients[client_socket]}: {e}")
                    del clients[client_socket]
        time.sleep(0.1)

# Update server time
start_time = time.time()
servertijd = 0

def update_servertijd():
    global servertijd, start_time
    while True:
        # Calculate elapsed time since server "start"
        elapsed_time = int(time.time() - start_time)
        # Keep servertijd in the 0-239 range
        servertijd = elapsed_time % 240
        time.sleep(0.1)  # Frequent updates for precision

# Broadcast server time to all clients
def broadcast_tijd():
    while True:
        try:
            tijd_message = json.dumps({
                "type": "time",
                "data": servertijd,
                "checksum": hash(servertijd)  # Add simple validation
            })
            for client_socket in list(clients.keys()):
                    try:
                        client_socket.sendall(tijd_message.encode('utf-8'))
                    except Exception as e:
                        print(f"[ERROR] Error sending tijd_data to client {clients[client_socket]}: {e}")
                        del clients[client_socket]
        except Exception as e:
            print(f"[ERROR] Error in broadcast loop: {e}")
        time.sleep(0.1)

# Print server status in a separate thread
def print_server_status(local_ip, generated_port):
    while True:
        print(f"Server is listening on ip and port {local_ip}:{generated_port}...")
        time.sleep(1)

# Starting threads for various tasks
Thread(target=print_server_status, args=(local_ip, generated_port), daemon=True).start()
Thread(target=broadcast_positions, daemon=True).start()
Thread(target=update_servertijd, daemon=True).start()
Thread(target=broadcast_tijd, daemon=True).start()

# Start the main server loop
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((local_ip, generated_port))
server_socket.listen(5)
print(f"Server is listening on {local_ip}:{generated_port}...")

clients = {}  # Mapping client_socket -> client_id
clients_positions = {}

while True:
    client_socket, client_address = server_socket.accept()
    Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
