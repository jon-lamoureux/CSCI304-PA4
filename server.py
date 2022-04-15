from socket import *
import random
playerPort = 12000
dealerPort = 12001
playerSocket, dealerSocket = socket(AF_INET, SOCK_DGRAM), socket(AF_INET, SOCK_DGRAM)
playerSocket.bind(('', playerPort))
dealerSocket.bind(('', dealerPort))
d = {
        'Ace of Spades': '1', '2 of Spades': '2', '3 of Spades': '3', '4 of Spades': '4', '5 of Spades': '5',
        '6 of Spades': '6', '7 of Spades': '7', '8 of Spades': '8', '9 of Spades': '9', '10 of Spades': '10',
        'Jack of Spades': '10', 'Queen of Spades': '10', 'King of Spades': '10',
        'Ace of Hearts': '1', '2 of Hearts': '2', '3 of Hearts': '3', '4 of Hearts': '4', '5 of Hearts': '5',
        '6 of Hearts': '6', '7 of Hearts': '7', '8 of Hearts': '8', '9 of Hearts': '9', '10 of Hearts': '10',
        'Jack of Hearts': '10', 'Queen of Hearts': '10', 'King of Hearts': '10',
        'Ace of Clubs': '1', '2 of Clubs': '2', '3 of Clubs': '3', '4 of Clubs': '4', '5 of Clubs': '5',
        '6 of Clubs': '6', '7 of Clubs': '7', '8 of Clubs': '8', '9 of Clubs': '9', '10 of Clubs': '10',
        'Jack of Clubs': '10', 'Queen of Clubs': '10', 'King of Clubs': '10',
        'Ace of Diamonds': '1', '2 of Diamonds': '2', '3 of Diamonds': '3', '4 of Diamonds': '4', '5 of Diamonds': '5',
        '6 of Diamonds': '6', '7 of Diamonds': '7', '8 of Diamonds': '8', '9 of Diamonds': '9', '10 of Diamonds': '10',
        'Jack of Diamonds': '10', 'Queen of Diamonds': '10', 'King of Diamonds': '10'
    }
deck = list(d.items())
random.shuffle(deck)
playerTotal, dealerTotal = 0, 0
print("Welcome to Blackjack!")
turn = 1

# Infinite Loop Until Game Ends
while True:
    # Get player input and dealer input before starting the game
    playerInput, playerAddress = playerSocket.recvfrom(2048)
    dealerInput, dealerAddress = dealerSocket.recvfrom(2048)

    # Assign the player a card
    playerCard = deck.pop(0)
    playerTotal += int(playerCard[1])

    # Send teh results to the dealer and player
    dealerResult = "The player drew the %s, for a total of %d" % (playerCard[0], playerTotal)
    playerResult = "You drew the %s, for a total of %d" % (playerCard[0], playerTotal)
    playerSocket.sendto(playerResult.encode(), playerAddress)
    dealerSocket.sendto(dealerResult.encode(), dealerAddress)

    # Draw the dealer's card
    dealerCard = deck.pop(0)
    dealerTotal += int(dealerCard[1])

    # Send the results to the dealer and player
    dealerResult = "You drew the %s, for a total of %d" % (dealerCard[0], dealerTotal)
    playerResult = "The dealer drew the %s, for a total of %d" % (dealerCard[0], dealerTotal)
    dealerSocket.sendto(dealerResult.encode(), dealerAddress)
    playerSocket.sendto(playerResult.encode(), playerAddress)

    # Get player input
    turn = '1'.encode()
    playerSocket.sendto(turn, playerAddress)
    playerInput, playerAddress = playerSocket.recvfrom(2048)
    decision = playerInput.decode()

    # Get player input until the player is done
    while decision != "2":
        playerCard = deck.pop(0)
        playerTotal += int(playerCard[1])
        dealerResult = "The player drew the %s, for a total of %d" % (playerCard[0], playerTotal)
        playerResult = "You drew the %s, for a total of %d" % (playerCard[0], playerTotal)
        playerSocket.sendto(playerResult.encode(), playerAddress)
        dealerSocket.sendto(dealerResult.encode(), dealerAddress)
        if playerTotal > 21:
            result = "The player busted, so the dealer won!"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), playerAddress)
            break
        turn = '1'.encode()
        playerSocket.sendto(turn, playerAddress)
        playerInput, playerAddress = playerSocket.recvfrom(2048)
        decision = playerInput.decode()
    if playerTotal > 21:
        break
    turn = '2'.encode()
    dealerSocket.sendto(turn, dealerAddress)
    dealerInput, dealerAddress = dealerSocket.recvfrom(2048)
    dealerDecision = dealerInput.decode()
    while dealerDecision != 2:
        dealerCard = deck.pop(0)
        dealerTotal += int(dealerCard[1])
        playerResult = "The dealer drew the %s, for a total of %d" % (dealerCard[0], dealerTotal)
        playerSocket.sendto(playerResult.encode(), playerAddress)
        dealerResult = "You drew the %s, for a total of %d" % (dealerCard[0], dealerTotal)
        dealerSocket.sendto(dealerResult.encode(), dealerAddress)
        if dealerTotal > 21:
            result = "The dealer busted, so the player won!"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), dealerAddress)
            break
        turn = '2'.encode()
        dealerSocket.sendto(turn, dealerAddress)
        dealerInput, dealerAddress = dealerSocket.recvfrom(2048)
        dealerDecision = dealerInput.decode()
    if dealerTotal > 21:
        break
    if dealerTotal > playerTotal:
        result = "The dealer won!"
    elif dealerTotal == playerTotal:
        result = "It was a draw!"
    else:
        result = "The player won!"
    playerSocket.sendto(result.encode(), playerAddress)
    dealerSocket.sendto(result.encode(), dealerAddress)
    break