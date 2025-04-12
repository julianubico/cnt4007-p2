import socket
import threading
import os

PORT = 5106

def accept_connection(client, address):
    with client:
        print(f"Connection from {address}")
        data = client.recv(1024)
        if not data: 
            print(f"Exiting thread for {address}")
            client.close()
            return
        command = data.decode()
        filename = command.split()[1]
        if command.startswith("get"):
            print(f"Sending file: {filename}")
            with open(filename, 'rb') as file:
                size = os.path.getsize(filename)
                chunks = (size + 1023) // 1024
                client.sendall(str(chunks).encode())
                client.recv(1024)

                data = file.read(1024)
                while data:
                    client.sendall(data)
                    data = file.read(1024)
            print(f"File sent {filename} successfully")
        elif command.startswith("upload"):
            print(f"Receiving file: {filename}")
            chunks = int(client.recv(1024).decode())
            client.sendall('ACK'.encode())

            with open('new' + filename, 'wb') as file:
                received = 0
                while received < chunks:
                    data = client.recv(1024)
                    if not data: break
                    file.write(data)
                    received += 1
            print(f"File new{filename} received")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', PORT))
    # For now just 2 connections
    server_socket.listen(2)
    print(f"Server socket bound on port {PORT}")
    while True:
        client, address = server_socket.accept()
        thread = threading.Thread(target=accept_connection, args=(client, address))
        thread.start()
        print(f"Started thread for {address}")

