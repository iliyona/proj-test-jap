from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import time

placePiece = False
invalidMove = True
endOption = False

welcomeMsg = 'WELCOME TO TIC-TAC-TOE ONLINE GAMEBOARD^^' """
_________________________
|       |       |       |
|   1   |   2   |   3   |
|_______|_______|_______|
|       |       |       |
|   4   |   5   |   6   |
|_______|_______|_______|
|       |       |       |
|   7   |   8   |   9   |
|_______|_______|_______|
""" '\nPLEASE ENTER YOUR NAME AND PRESS ENTER. HAVE FUN AND GOODLUCK!!'
inQueueMsg = 'PLEASE WAIT. WE LOOKING FOR ANOTHER PLAYER TO JOIN.'
invalidMoveError = 'ERROR! INVALID MOVE. CHOOSE A VALID LOCATION. EG: NUM 1-9 ONLY.'
yourTurnMsg = "ITS YOUR TURN. CHOOSE A VALID LOCATION TO PLACE A PIECE. (NUM 1-9)."
endOptionMsg = '\nYOU WANT TO REMATCH? --> ENTER "R" TO REMATCH GAME''\nYOU WANT TO QUIT? --> ENTER "Q" TO QUIT'

# Set up client, connect to host
HOST = input('ENTER SERVER IP:\n--> ')
serverPort = 2019
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST,serverPort))

#Make move
def play():
    global invalidMove
    while True:
        loc = input('... ')
        clientSocket.send(loc.encode())
        time.sleep(0.5)
        if not invalidMove:
            invalidMove = True
            break

def receive():
    global placePiece
    global invalidMove
    global yourTurnMsg
    global invalidMoveError
    global endOption
    while True:
        try:
            msg = clientSocket.recv(1024).decode()
            print(msg)
            if yourTurnMsg in msg:
                placePiece = True
            elif endOptionMsg in msg:
                endOption = True
            elif "ERROR! INVALID MOVE." not in msg:
                invalidMove = False
            elif "Ending game." in msg:
                sys.exit()
        except OSError:
            print("End")
            # Possibly client has left the chat.
            break

def send():
    global placePiece
    global endOption
    while True:
        try:
            if endOption:
                choice = input('... ')
                clientSocket.send(choice.encode())
                endOption = False
            if placePiece:
                play()
                placePiece = False
        except OSError:
            # Possibly client has left the chat.
            break

def main():
    # Handshake steps:
    # 1. Client receives greeting message from chat server, asking for a name
    print(clientSocket.recv(1024).decode())
    # 2. Client enters name and sends it to chat server
    NAME = input('NAME: ')
    clientSocket.send(NAME.encode())

    # Start the receiving thread
    receive_thread = Thread(target=receive)
    receive_thread.start()
    # Start the sending thread
    send_thread = Thread(target=send)
    send_thread.start()

    # Wait for child threads to stop
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    main()
