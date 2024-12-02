import socket
import json
import uuid
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(5)
print("Server is listening on port 12345...")

clients = []

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    clients.append(client_socket)

    client_id = str(uuid.uuid4())  # Уникальный UUID для каждого клиента
    print(f"New connection from {client_address}, assigned ID: {client_id}")
    client_socket.sendall(json.dumps({"client_id": client_id}).encode())

    while True:
        try:
            # Receive the player's position data (in JSON format)
            data = client_socket.recv(4096)
            if data:
                position_data = json.loads(data.decode('utf-8'))  # Convert back to dictionary
                print(f"Received position from {client_id}: {position_data}")
                # Broadcast the position to other clients if needed
                for c in clients:
                    if c != client_socket:  # Don't send position back to the same client
                        c.send(json.dumps(position_data).encode('utf-8'))
            else:
                break
        except Exception as e:
            print(f"Error receiving data from {client_id}: {e}")
            break

    print(f"Connection from {client_id} closed")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new thread to handle each client
        Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()
