# coding: utf-8
from socket import *
import os
import sys

# using the socket module

# Define connection (socket) parameters
# Address + Port no
# Server would be running on the same host as Client
# change this port number if required

serverPort = int(sys.argv[1])

# serverPort = 1203 # IMPORTANT THIS WILL BE A CMD ARG SO CHANGE ACCORDINGLY

serverSocket = socket(AF_INET, SOCK_STREAM)
# This line creates the server’s socket. The first parameter indicates the address family; in particular,AF_INET indicates that the underlying network is using IPv4.The second parameter indicates that the socket is of type SOCK_STREAM,which means it is a TCP socket (rather than a UDP socket, where we use SOCK_DGRAM).

serverSocket.bind(("localhost", serverPort))
# The above line binds (that is, assigns) the port number 12000 to the server’s socket. In this manner, when anyone sends a packet to port 12000 at the IP address of the server (localhost in this case), that packet will be directed to this socket.

serverSocket.listen(1)
# The serverSocket then goes in the listen state to listen for client connection requests.

print("The server is ready to receive")

keepAlive = True

while keepAlive:
    connectionSocket, addr = serverSocket.accept()
    # When a client knocks on this door, the program invokes the accept( ) method for serverSocket, which creates a new socket in the server, called connectionSocket, dedicated to this particular client. The client and server then complete the handshaking, creating a TCP connection between the client’s clientSocket and the server’s connectionSocket. With the TCP connection established, the client and server can now send bytes to each other over the connection. With TCP, all bytes sent from one side not are not only guaranteed to arrive at the other side but also guaranteed to arrive in order

    sentence = connectionSocket.recv(1024)
    # wait for data to arrive from the client

    if "Connection: close" in sentence.decode("utf-8"):
        keepAlive = False

    capitalizedSentence = sentence.upper()
    # change the case of the message received from client

    # close the connectionSocket. Note that the serverSocket is still alive waiting for new clients to connect, we are only closing the connectionSocket.
    filePath = "index.html"
    filePath = sentence.decode("utf-8").split(" ")[1]

    if filePath == "/favicon.ico":
        header = "HTTP/1.1 204 No Content\n\n".encode()
        connectionSocket.send(header)
    else:
        try:
            with open(filePath.strip("/"), "rb") as fileToSend:
                content = fileToSend.read()
                header = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode()

                # First, send the HTTP header
                connectionSocket.send(header)
                # Then, send the content of the file
                connectionSocket.send(content)
        except FileNotFoundError:
            # If the file is not found, send a 404 response
            header = "HTTP/1.1 404 Not Found\n\n".encode()
            connectionSocket.send(header)
            connectionSocket.send(b"<html><body><h1>404 Not Found</h1></body></html>")

    connectionSocket.close()
