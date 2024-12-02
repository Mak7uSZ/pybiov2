import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.102.39', 12345))  # Replace with your server's local IP

try:
    message = input("Enter a message (or 'exit' to quit): ")
    while message.lower() != 'exit':
        client.send(message.encode())  # Send message to server

        response = client.recv(1024)
        print(f"Server response: {response.decode()}")

        message = input("Enter a message (or 'exit' to quit): ")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()  # Ensure the connection is closed properly
