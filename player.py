from socket import *
from tkinter import *
from threading import Thread
import time
choice = 0
card = {
        'Ace of Spades': 'A♠', '2 of Spades': '2♠', '3 of Spades': '3♠', '4 of Spades': '4♠', '5 of Spades': '5♠',
        '6 of Spades': '6♠', '7 of Spades': '7♠', '8 of Spades': '8♠', '9 of Spades': '9♠', '10 of Spades': '10♠',
        'Jack of Spades': 'J♠', 'Queen of Spades': 'Q♠', 'King of Spades': 'K♠',
        'Ace of Hearts': 'A♥', '2 of Hearts': '2♥', '3 of Hearts': '3♥', '4 of Hearts': '4♥', '5 of Hearts': '5♥',
        '6 of Hearts': '6♥', '7 of Hearts': '7♥', '8 of Hearts': '8♥', '9 of Hearts': '9♥', '10 of Hearts': '10♥',
        'Jack of Hearts': 'J♥', 'Queen of Hearts': 'Q♥', 'King of Hearts': 'K♥',
        'Ace of Clubs': 'A♣', '2 of Clubs': '2♣', '3 of Clubs': '3♣', '4 of Clubs': '4♣', '5 of Clubs': '5♣',
        '6 of Clubs': '6♣', '7 of Clubs': '7♣', '8 of Clubs': '8♣', '9 of Clubs': '9♣', '10 of Clubs': '10♣',
        'Jack of Clubs': 'J♣', 'Queen of Clubs': 'Q♣', 'King of Clubs': 'K♣',
        'Ace of Diamonds': 'A♦', '2 of Diamonds': '2♦', '3 of Diamonds': '3♦', '4 of Diamonds': '4♦', '5 of Diamonds': '5♦',
        '6 of Diamonds': '6♦', '7 of Diamonds': '7♦', '8 of Diamonds': '8♦', '9 of Diamonds': '9♦', '10 of Diamonds': '10♦',
        'Jack of Diamonds': 'J♦', 'Queen of Diamonds': 'Q♦', 'King of Diamonds': 'K♦'
    }
currCards, dealCards, resulttxt = "", "", ""
currTotal, dealTotal = 0, 0
def createGUI():
    global choice, text1, text2, text3, text4, textResult, canvas1
    # Create GUI
    root = Tk()
    root.title('Blackjack - Player')
    root.geometry('1000x500+20+20')

    # Set choice to 0
    choice = '0'

    def drawCard():
        global choice
        choice = '1'
    def stand():
        global choice
        choice = '2'

    bg = PhotoImage(file = "background.png")
    canvas1 = Canvas(root, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    text1 = canvas1.create_text(520,440,text=currTotal, font=('Helvetica','20','bold'))
    text2 = canvas1.create_text(520,380,text=currCards, font=('Helvetica','20','bold'))
    text3 = canvas1.create_text(520,50,text=dealTotal, font=('Helvetica','20','bold',), fill='red')
    text4 = canvas1.create_text(520,110,text=dealCards, font=('Helvetica','20','bold'), fill='red')
    textResult = canvas1.create_text(520,240,text=resulttxt, font=('Helvetica','25','bold'))
    button1 = Button( root, text = "Draw", command=drawCard)
    button2 = Button( root, text = "Stand", command=stand)
    button1_canvas = canvas1.create_window(475, 460, anchor = "nw", window = button1)
    button2_canvas = canvas1.create_window(525, 460, anchor = "nw", window = button2)
    root.mainloop()


def serverConn():
    global choice, currCards, currTotal, dealCards, dealTotal
    serverName = '127.0.0.1'
    serverPort = 12002
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    time.sleep(1)
    message = '1'
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    while 1:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        received = modifiedMessage.decode()
        if received == "1":
            while choice == '0':
                if choice != '0':
                    break # this well never execute because of logic, but I put it here anyway
            message = choice
            clientSocket.sendto(message.encode(), (serverName, serverPort))
            choice = '0'
        else:
            spliced = received.split(':')
            if spliced[0] == "p":
                currTotal = spliced[2]
                currCards = currCards + " " + card[spliced[1]]
                canvas1.itemconfigure(text1, text=currTotal)
                canvas1.itemconfigure(text2, text=currCards)
            elif spliced[0] == "pl":
                canvas1.itemconfigure(textResult, text="You lose!")
            elif spliced[0] == "tie":
                canvas1.itemconfigure(textResult, text="It was a tie!")
            elif spliced[0] == "dl":
                canvas1.itemconfigure(textResult, text="You win!")
            elif spliced[0] == "bj":
                canvas1.itemconfigure(text1, text="Blackjack!")
            else:
                dealTotal = spliced[2]
                dealCards = dealCards + " " + card[spliced[1]]
                canvas1.itemconfigure(text3, text=dealTotal)
                canvas1.itemconfigure(text4, text=dealCards)
    clientSocket.close()


t1 = Thread(target = createGUI)
t2 = Thread(target = serverConn)

t1.start()
t2.start()

t1.join()
t2.join()