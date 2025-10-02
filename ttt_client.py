import socket
import time
import select
import sys

HOST = '127.0.0.1'
PORT = 12345

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server!")
        break
    except ConnectionRefusedError:
        print("Server not ready, retrying...")
        time.sleep(1)

mark = None
board = [' '] * 9
turn = False
recv_buffer = ""

def print_board(board):
    print()
    for i in range(3):
        print(f"    {board[i*3]} ║ {board[i*3+1]} ║ {board[i*3+2]} ")
        if i < 2:
            print("  ════╬═══╬════")
    print()

def announce_turn():
    if turn:
        print("Your turn!")
    else:
        print("Waiting for opponent...")

while True:
    ready, _, _ = select.select([s, sys.stdin], [], [])

    for source in ready:
        if source == s:
            chunk = s.recv(1024).decode()
            if not chunk:
                print("Server disconnected.")
                sys.exit(0)

            recv_buffer += chunk
            while "\n" in recv_buffer:
                msg, recv_buffer = recv_buffer.split("\n", 1)
                msg = msg.strip()
                if not msg:
                    continue

                if msg.startswith("START:"):
                    mark = msg.split(":")[1]
                    print(f"Game started! You are {mark}")
                    turn = (mark == 'X')
                    print_board(board)
                    announce_turn()

                elif msg == "WAITING":
                    print("Waiting for opponent...")
                    turn = False

                elif msg.startswith("OPPONENT:"):
                    idx = int(msg.split(":")[1])
                    board[idx] = 'X' if mark == 'O' else 'O'
                    print_board(board)
                    turn = True
                    announce_turn()

                elif msg.startswith("OK:"):
                    idx = int(msg.split(":")[1])
                    board[idx] = mark
                    print_board(board)
                    turn = False
                    announce_turn()

                elif msg.startswith("WINNER:"):
                    winner = msg.split(":")[1]
                    print_board(board)
                    if winner == mark:
                        print("You win!!")
                    else:
                        print("You lose")
                    sys.exit(0)

                elif msg == "DRAW":
                    print_board(board)
                    print("It's a draw!")
                    sys.exit(0)

        elif source == sys.stdin and turn:
            move = sys.stdin.readline().strip()
            if move.isdigit() and 1 <= int(move) <= 9 and board[int(move)-1] == ' ':
                s.send(f"MOVE:{int(move)-1}\n".encode())
            else:
                print("Invalid move!")
