import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 2000)
client_socket.connect(server_address)

# Get user choice
choice = input("Enter 1 for addition, 2 for factorial, 3 for binary: ")

# Send user choice to the server
client_socket.sendall(choice.encode())

# Get user input
if choice == '1':
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")
    client_socket.sendall(num1.encode())
    client_socket.sendall(num2.encode())
elif choice == '2':
    num = input("Enter number for factorial: ")
    client_socket.sendall(num.encode())
elif choice == '3':
    num = input("Enter decimal number for binary: ")
    client_socket.sendall(num.encode())
else:
    print("Invalid choice")
    client_socket.close()

# Receive the result from the server
result = client_socket.recv(1024).decode()
print("Result from server: ", result)

# Close the socket
print("Client Disconnect")
client_socket.close()