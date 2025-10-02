import socket
import random
import signal
import sys

def print_board(board):
    print("\n")
    for i in range(3):
        print(f"    {board[i*3]} ║ {board[i*3+1]} ║ {board[i*3+2]}")
        if i < 2:
            print("  ════╬═══╬════")
    print("\nPositions:\n")
    print("    1 ║ 2 ║ 3  ")
    print("  ════╬═══╬════")
    print("    4 ║ 5 ║ 6  ")
    print("  ════╬═══╬════")
    print("    7 ║ 8 ║ 9  \n")

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def is_board_full(board):
    return ' ' not in board

def get_player_move(board):
    while True:
        try:
            move = input("\nYour turn! Enter position (1-9) or 'q' to quit: ")
            if move.lower() == 'q':
                print("\nThanks for playing!")
                sys.exit(0)
            move = int(move)
            if 1 <= move <= 9 and board[move-1] == ' ':
                return move-1
            else:
                print("Invalid move! Choose an empty position (1-9).")
        except ValueError:
            print("Please enter a number between 1-9.")

def main():
    board = [' '] * 9
    role = input("Do you want to be server or client? (s/c): ").strip().lower()
    host = '127.0.0.1'
    port = 12345
    s = None
    conn = None

    def cleanup(sig=None, frame=None):
        print("\nSomeone quit!")
        print("\nClosing sockets...")
        if conn:
            conn.close()
        if s:
            s.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)

    try:
        if role == 's':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            print("Waiting for opponent to join...")
            conn, addr = s.accept()
            print(f"Opponent joined from {addr}")
            my_turn = True
        else:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((host, port))
            my_turn = False

        while True:
            print_board(board)
            winner = check_winner(board)
            if winner:
                if (winner == 'X' and role=='s') or (winner == 'O' and role=='c'):
                    print("\nYou win!")
                else:
                    print("\nOpponent wins!")
                break
            if is_board_full(board):
                print("\nIt's a tie!")
                break

            if my_turn:
                move = get_player_move(board)
                board[move] = 'X' if role=='s' else 'O'
                conn.send(str(move).encode())
                my_turn = False
            else:
                print("\nWaiting for opponent to make a move...")
                data = conn.recv(1024).decode()
                move = int(data)
                board[move] = 'O' if role=='s' else 'X'
                my_turn = True
    finally:
        cleanup()

if __name__ == "__main__":
    main()
