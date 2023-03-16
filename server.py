import socket

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 2000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

while True:
    # Wait for a client to connect
    print("Waiting for a client to connect...")
    client_socket, client_address = server_socket.accept()

    try:
        # Receive user choice
        choice = client_socket.recv(1024).decode()

        # Receive user input
        if choice == '1':
            print("Client has selected first option\n")
            num1 = client_socket.recv(1024).decode()
            num2 = client_socket.recv(1024).decode()
            result = str(int(num1) + int(num2))
        elif choice == '2':
            print("Client has selected second option\n")
            num = int(client_socket.recv(1024).decode())
            result = 1
            for i in range(1, num+1):
                result *= i
            result = str(result)
        elif choice == '3':
            print("Client has selected third option\n")
            num = int(client_socket.recv(1024).decode())
            result = bin(num)
        else:
            result = "Invalid choice"

        # Send the result back to the client
        client_socket.sendall(result.encode())
    finally:
        # Close the client socket
        print("Server Disconnet")
        client_socket.close()