import os
import sys
import tty
import termios
import time
import signal

best_snake_time = 0
best_tetris_time = 0
tic_wins = 0
class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

in_game_menu = False

def signal_handler(signum, frame):
    print(bcolors.WARNING + "\nUse 'exit' to quit the shell or Option 5 to exit the game menu" + bcolors.ENDC)
    if in_game_menu:
        print("\nWelcome to my Mini-Shell Mini-Game Menu!")
        print("1. Snake")
        print("2. Tetris")
        print("3. Tic-Tac-Toe")
        print("4. Multiplayer Tic-Tac-Toe with Client/Server")
        print("5. Exit menu")
        print()
    else:
        print("Type 'exit' or 'games' to continue...")
        print("mini-shell> ", end="", flush=True)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)  

def execute_command(cmd):
    args = cmd.split()
    if not args:
        return
    
    stdout_file = None
    stdin_file = None
    append_mode = False
    ##implementing I/O redirection for future use / logging
    if '>>' in args:
        idx = args.index('>>')
        stdout_file = args[idx + 1]
        append_mode = True
        args = args[:idx]
    elif '>' in args:
        idx = args.index('>')
        stdout_file = args[idx + 1]
        args = args[:idx]
    
    if '<' in args:
        idx = args.index('<')
        stdin_file = args[idx + 1]
        args = args[:idx]
    
    pid = os.fork()
    if pid == 0: 
        if stdout_file:
            flags = os.O_WRONLY | os.O_CREAT
            flags |= os.O_APPEND if append_mode else os.O_TRUNC
            fd = os.open(stdout_file, flags, 0o644)
            os.dup2(fd, 1)
            os.close(fd)
        
        if stdin_file:
            try:
                fd = os.open(stdin_file, os.O_RDONLY)
                os.dup2(fd, 0)
                os.close(fd)
            except FileNotFoundError:
                print(f"Input file not found: {stdin_file}")
                sys.exit(1)
        
        try:
            os.execvp(args[0], args)
        except FileNotFoundError:
            print(f"Command not found: {args[0]}")
            sys.exit(1)
    else: 
        os.waitpid(pid, 0)

def launch_game():
    global best_snake_time
    global best_tetris_time
    global tic_wins
    global in_game_menu
    in_game_menu = True

    while True:
        print("\nWelcome to my Mini-Shell Mini-Game Menu!")
        print("1. Snake")
        print("2. Tetris")
        print("3. Tic-Tac-Toe")
        print("4. Multiplayer Tic-Tac-Toe with Client/Server")
        print("5. Exit menu")
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
            print_tic_banner()
            os.system("python3 multiplayer.py") 

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
    in_game_menu = False

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
            execute_command(cmd)
    except Exception as e:
        print(f"Error: {e}")