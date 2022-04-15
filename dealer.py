from socket import *

serverName = '127.0.0.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Welcome to Blackjack! Press 1 when are you ready to begin: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))

while 1:
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    received = modifiedMessage.decode()
    if received == "2":
        message = input('Player is done, press 1 to draw or 2 to stand:')
        clientSocket.sendto(message.encode(), (serverName, serverPort))
    if received != "1":
        print(received)

clientSocket.close()