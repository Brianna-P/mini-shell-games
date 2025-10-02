import os
import sys
import tty
import termios
import time

best_snake_time = 0
best_tetris_time = 0
tic_wins = 0
def launch_game():
    global best_snake_time
    global best_tetris_time
    while True:
        print("\nWelcome to my Mini-Shell Mini-Game Menu!")
        print("1. Snake")
        print("2. Tetris")
        print("3. Tic-Tac-Toe")
        print("4. Exit menu")
        choice = input("Choose a game: ").strip()
        
        if choice == "1":
            print_snake_banner()
            wait_for_keypress()
            start = time.time()
            os.system("python3 snake.py") 
            end = time.time()
            print("\nYou played Snake for {:.2f} seconds.".format(end - start))
            if end - start > best_snake_time:
                best_snake_time = end - start
                print("New best time for Snake: {:.2f} seconds!".format(best_snake_time))
            else:
                print("Best time for Snake remains: {:.2f} seconds.".format(best_snake_time))
        elif choice == "2":
            print_tetris_banner()
            wait_for_keypress()
            start = time.time()
            os.system("python3 tetris.py") 
            end = time.time()
            print("\nYou played Tetris for {:.2f} seconds.".format(end - start))
            if end - start > best_tetris_time:
                best_tetris_time = end - start
                print("New best time for Tetris: {:.2f} seconds!".format(best_tetris_time))
            else:
                print("Best time for Tetris remains: {:.2f} seconds.".format(best_tetris_time))
        elif choice == "3":
            print_tic_banner()
            wait_for_keypress()
            os.system("python3 tic_tac_toe.py") 
            tic_wins += 1
            print(f"You have won Tic Tac Toe {tic_wins} times!")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def print_snake_banner():
    snake = r"""
             /^\/^\
           _|__|  O|
  \/     /~     \_/ \
   \____|__________/  \
          \_______      \
                  `\     \                 \
                    |     |                  \
                   /      /                    \
                  /     /                       \\
                 /      /                         \ \
                /     /                            \  \
              /     /             _----_            \   \
             /     /           _-~      ~-_         |   |
            (      (        _-~    _--_    ~-_     _/   |
             \      ~-____-~    _-~    ~-_    ~-_-~    /
               ~-_           _-~          ~-_       _-~
                  ~--______-~                ~-___-~
    """
    print(snake)
    print("Welcome to Snake!\n")


def wait_for_keypress(prompt="Press any key to start..."):
    print(prompt, end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        sys.stdin.read(1) 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()  

def print_tetris_banner():
    tetris = r"""
╔═════════════════════════════════════════════════╗
║ ████████╗███████╗████████╗██████╗  ██╗ ███████╗ ║
║ ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗ ██║ ██╔════╝ ║
║    ██║   ███████╗   ██║   ██████╔╝ ██║ ███████╗ ║
║    ██║   ██╔════╝   ██║   ██╔══██╗ ██║      ██║ ║
║    ██║   ███████║   ██║   ██║  ██║ ██║ ███████║ ║
║    ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═╝ ╚══════╝ ║
╚═════════════════════════════════════════════════╝                                    
    """
    print(tetris)
    print("Welcome to Tetris!\n")

def print_tic_banner():
    tic = r"""
╔════════════════════════════════╗
║  ╔═══╦═══╦═══╗  ╔═══╦═══╦═══╗  ║
║  ║ X ║ O ║ X ║  ║ O ║ X ║ O ║  ║
║  ╠═══╬═══╬═══╣  ╠═══╬═══╬═══╣  ║
║  ║ O ║ X ║ O ║  ║ X ║ O ║ X ║  ║
║  ╠═══╬═══╬═══╣  ╠═══╬═══╬═══╣  ║
║  ║ X ║ O ║ X ║  ║ O ║ X ║ O ║  ║
║  ╚═══╩═══╩═══╝  ╚═══╩═══╩═══╝  ║
║                                ║
║         TIC  TAC  TOE          ║
╚════════════════════════════════╝
"""
    print(tic)
    print("Welcome to Tic Tac Toe!!\n")


while True:
    try:
        print("Type \'exit\' or \'games\' to continue...")
        cmd = input("mini-shell> ").strip()
        
        if cmd == "exit":
            break
        elif cmd == "games":
            launch_game() 
        else:
            args = cmd.split()
            if args:
                pid = os.fork()
                if pid == 0:
       
                    os.execvp(args[0], args)
                else:
                    os.wait()
    except Exception as e:
        print(f"Error: {e}")
