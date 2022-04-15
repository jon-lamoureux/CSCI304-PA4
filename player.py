from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Welcome to Blackjack! Press 1 when are you ready to begin: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))

while 1:
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    received = modifiedMessage.decode()
    if received == "1":
        message = input('Press 1 to draw another card, or 2 to stand:')
        clientSocket.sendto(message.encode(), (serverName, serverPort))
    else:
        print(received)
clientSocket.close()