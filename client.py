import socket
import os
import sys

if (len(sys.argv) != 2):
    raise Exception("client.py <port>")

PORT = sys.argv[1]
if (not PORT.isdigit()):
    raise Exception("Port must be a number")
PORT = int(PORT)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', PORT))
        command = input("""Options:
    1. get <filename>
    2. upload <filename>
    3. exit
Please enter a command: """)

        if command.startswith("exit"):
            break
        elif command.startswith("upload"):
            client_socket.sendall(command.encode())
            filename = command.split()[1]
            with open (filename, 'rb') as file:
                size = os.path.getsize(filename)
                chunks = (size + 1023) // 1024
                client_socket.sendall(str(chunks).encode())
                client_socket.recv(1024)
                
                data = file.read(1024)
                while data: 
                    client_socket.sendall(data)
                    data = file.read(1024)
            print(f"File sent {filename} successfully")
        elif command.startswith("get"):
            client_socket.sendall(command.encode())
            filename = 'new' + command.split()[1]

            chunks = int(client_socket.recv(1024).decode())
            client_socket.sendall('ACK'.encode())

            with open(filename, 'wb') as file:
                received = 0
                while received < chunks:
                    data = client_socket.recv(1024)
                    if not data: break
                    file.write(data)
                    received += 1

            print(f"File received {filename} successfully")
        else:
            print("Invalid command")
            continue