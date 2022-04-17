from socket import *
import random
playerPort = 12002
dealerPort = 12003
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
playerAce = 0
dealerAce = 0
dealerDraws = 0
playerDraws = 0
blackjack = 0
# Infinite Loop Until Game Ends
while True:
    # Get player input and dealer input before starting the game
    playerInput, playerAddress = playerSocket.recvfrom(2048)
    dealerInput, dealerAddress = dealerSocket.recvfrom(2048)

    # Assign the player a card
    playerCard = deck.pop(0)
    playerTotal += int(playerCard[1])
    playerDraws += 1;

    # If ace
    if playerTotal == 1:
        playerAce = 1
        dealerResult = "p:%s:%d/%d" % (playerCard[0], playerTotal, 11)
        playerResult = "p:%s:%d/%d" % (playerCard[0], playerTotal, 11)
    else:
        dealerResult = "p:%s:%d" % (playerCard[0], playerTotal)
        playerResult = "p:%s:%d" % (playerCard[0], playerTotal)

    # Send the results to the dealer and player
    playerSocket.sendto(playerResult.encode(), playerAddress)
    dealerSocket.sendto(dealerResult.encode(), dealerAddress)

    # Draw the dealer's card
    dealerCard = deck.pop(0)
    dealerTotal += int(dealerCard[1])
    dealerDraws += 1;

    if dealerTotal == 1:
        dealerAce = 1;
        dealerResult = "d:%s:%d/%d" % (dealerCard[0], dealerTotal, 11)
        playerResult = "d:%s:%d/%d" % (dealerCard[0], dealerTotal, 11)
    else:
        dealerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)
        playerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)

    # Send the results to the dealer and player
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
        playerDraws += 1
        if "Ace" in playerCard[0]:
            playerAce = 1
        if playerTotal < 11 and playerAce == 1:
            dealerResult = "p:%s:%d/%d" % (playerCard[0], playerTotal, (playerTotal + 10))
            playerResult = "p:%s:%d/%d" % (playerCard[0], playerTotal, (playerTotal + 10))
        elif playerTotal >= 11 and playerAce == 1:
            dealerResult = "p:%s:%d" % (playerCard[0], playerTotal)
            playerResult = "p:%s:%d" % (playerCard[0], playerTotal)
        else:
            dealerResult = "p:%s:%d" % (playerCard[0], playerTotal)
            playerResult = "p:%s:%d" % (playerCard[0], playerTotal)
        playerSocket.sendto(playerResult.encode(), playerAddress)
        dealerSocket.sendto(dealerResult.encode(), dealerAddress)

        # If Blackjack
        if playerTotal == 11 and playerAce == 1 and playerDraws == 2:
            result = "bj:21"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), playerAddress)
            blackjack = 1
            break
        if playerTotal > 21:
            result = "pl"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), playerAddress)
            break
        turn = '1'.encode()
        playerSocket.sendto(turn, playerAddress)
        playerInput, playerAddress = playerSocket.recvfrom(2048)
        decision = playerInput.decode()
    if playerTotal > 21:
        break
    if playerTotal <= 11 and playerAce == 1:
        playerTotal += 10
    turn = '2'.encode()
    dealerSocket.sendto(turn, dealerAddress)
    dealerInput, dealerAddress = dealerSocket.recvfrom(2048)
    dealerDecision = dealerInput.decode()
    while dealerDecision != "2":
        # Draw a card
        dealerCard = deck.pop(0)
        dealerTotal += int(dealerCard[1])
        dealerDraws += 1

        if "Ace" in dealerCard[0]:
            dealerAce = 1
        # Print result of that card
        if dealerTotal < 11 and dealerAce == 1:
            playerResult = "d:%s:%d/%d" % (dealerCard[0], dealerTotal, (dealerTotal + 10))
            dealerResult = "d:%s:%d/%d" % (dealerCard[0], dealerTotal, (dealerTotal + 10))
        elif dealerTotal >= 11 and dealerAce == 1:
            playerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)
            dealerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)
        else:
            playerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)
            dealerResult = "d:%s:%d" % (dealerCard[0], dealerTotal)
        # Send to player and dealer
        playerSocket.sendto(playerResult.encode(), playerAddress)
        dealerSocket.sendto(dealerResult.encode(), dealerAddress)
        # If Blackjack
        if dealerTotal == 11 and dealerAce == 1 and dealerDraws == 2:
            result = "pl"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), dealerAddress)
            if blackjack == 1:
                result = "tie"
                dealerSocket.sendto(result.encode(), dealerAddress)
                playerSocket.sendto(result.encode(), dealerAddress)
                break
        if dealerTotal > 21:
            result = "dl"
            dealerSocket.sendto(result.encode(), dealerAddress)
            playerSocket.sendto(result.encode(), playerAddress)
            break
        turn = '2'.encode()
        dealerSocket.sendto(turn, dealerAddress)
        dealerInput, dealerAddress = dealerSocket.recvfrom(2048)
        dealerDecision = dealerInput.decode()
    if dealerTotal <= 11 and dealerAce == 1:
        dealerTotal += 10
    if dealerTotal > 21:
        break
    if dealerTotal > playerTotal:
        result = "pl"
    elif dealerTotal == playerTotal:
        result = "tie"
    else:
        result = "dl"
    playerSocket.sendto(result.encode(), playerAddress)
    dealerSocket.sendto(result.encode(), dealerAddress)
