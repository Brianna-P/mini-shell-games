import os
import random
import time

def print_board(board):
    print("\n")
    for i in range(3):
        print(f"   {board[i*3]} ║ {board[i*3+1]} ║ {board[i*3+2]}")
        if i < 2:
            print(" ════╬═══╬════")


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def is_board_full(board):
    return ' ' not in board

def minimax(board, depth, is_maximizing):
   
    winner = check_winner(board)
    
    if winner == 'X':  
        return 10 - depth
    elif winner == 'O': 
        return depth - 10
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        # computer turn.  maximize score
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        # human turn. minimize score
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def get_computer_move(board):
    best_score = float('-inf')
    best_move = None
    
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ' '
            
            if score > best_score:
                best_score = score
                best_move = i
    
    return best_move

def get_player_move(board):
    while True:
        try:
            move = input(f"\nHuman player, enter position (1-9): ")
            check_quit_input(move)
            move = int(move)
            if 1 <= move <= 9 and board[move-1] == ' ':
                return move - 1
            else:
                print("Invalid move! Choose an empty position (1-9).")
        except ValueError:
            print("Please enter a number between 1-9.")

def check_quit_input(input_str):
    if input_str.lower() == 'q':
        print("\nThanks for playing!")
        exit()

def play_tic_tac_toe():
    board = [' '] * 9
    
    print("WELCOME TO TIC TAC TOE!")
    print("Press 'q' (during your turn) to quit at any time.")
    print("Positions are numbered as follows:")
    print("   1 ║ 2 ║ 3 ")
    print("═════╬═══╬═════")
    print("   4 ║ 5 ║ 6 ")
    print("═════╬═══╬═════")
    print("   7 ║ 8 ║ 9 ")
    
    while True:
        print_board(board)
        human_move = get_player_move(board)
        board[human_move] = 'O'
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'X':
                print(f"\nBeep boop... Computer wins! Better luck next time!")
            else:
                print(f"\nYou win! (Beep boop.. that shouldn't be possible...)")
            break
        
        if is_board_full(board):
            print_board(board)
            print("\nBeep boop... It's a tie!")
            break
        
        print_board(board)
        computer_responses = [
            "Beep boop... Computing optimal move...",
            "Beep boop... Analyzing all possibilities...",
            "Beep boop... Running minimax algorithm...",
            "Beep boop... Calculating perfect strategy...",
            "Beep boop... Processing game tree..."
        ]
        print(random.choice(computer_responses))
        time.sleep(1)
        
        computer_move = get_computer_move(board)
        board[computer_move] = 'X'
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'X':
                print(f"\nBeep boop... Computer wins! Better luck next time!")
            else:
                print(f"\nYou win!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("\nBeep boop... It's a tie!")
            break
    
    play_again = input("\nPlay again? (y/n): ").lower()
    check_quit_input(play_again)
    if play_again == 'y':
        play_tic_tac_toe()
    else:
        print("\nThanks for playing!")

if __name__ == "__main__":
    play_tic_tac_toe()