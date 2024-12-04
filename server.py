import socket
import json
import uuid
from threading import Thread
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(5)
print("Server is listening on port 12345...")

clients = []  # List to keep track of connected clients
clients_positions = {}

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")

    # Generate a unique client ID
    client_id = str(uuid.uuid4())
    clients.append(client_socket)
    print(f"New connection from {client_address}, assigned ID: {client_id}")
    
    
        # Send the client ID to the client
    response = json.dumps(client_id)
    print(f"Sending client ID to client: {client_id}")
    client_socket.send(response.encode('utf-8'))
    

    while True:
        try:
            # Receive the player's position data (in JSON format)
            data = client_socket.recv(4096)
            if data:
                position_data = json.loads(data.decode('utf-8'))  # Convert back to dictionary
                print(f"Received position from {position_data}")
                clients_positions[client_id] = position_data
                print('test_print', clients_positions)
            else:
                break
        except Exception as e:
            print(f"Error receiving data from {client_id}: {e}")
            break

    print(f"Connection from {client_id} closed")
    clients.remove(client_socket)
    client_socket.close()
def send_positions_to_clients():
    while True:
        if clients_positions:
            positions_data = json.dumps(clients_positions)
            print(f"Sending positions data: {positions_data}")  # Debug line
            for client_socket in clients:
                try:
                    client_socket.sendall(positions_data.encode('utf-8'))
                    print("Sent positions data to client.")
                except Exception as e:
                    print(f"Error sending data to client: {e}")
        time.sleep(1)

def start_server():
    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new thread to handle each client
        Thread(target=send_positions_to_clients, daemon=True).start()
        Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()
