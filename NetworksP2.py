from socket import * #imports socket module
import sys  # In order to terminate the program

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverPort = 6789  # Port number
serverSocket.bind(('', serverPort))  # Bind to any available address on port 6789
serverSocket.listen(1)  # Listen for incoming connections (backlog of 1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()  # Receive message from client

        filename = message.split()[1]  # Extract the second part of HTTP request (file name)
        print("Filename:", filename)
        
        # Check if the requested file exists
        try:
            with open(filename[1:], 'rb') as f:
                outputdata = f.read()
            
            # Send HTTP headers into socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

            # Send the content of the requested file to the client
            connectionSocket.sendall(outputdata)
            connectionSocket.send("\r\n".encode())
        
        except IOError:
            # Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        
        # Close client socket
        connectionSocket.close()

    except Exception as e:
        print("Error:", e)

serverSocket.close()  # Close the server socket
sys.exit()  # Terminate the program after sending the corresponding data
