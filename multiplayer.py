import os
import sys
import time
import subprocess
import tty
import termios

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


current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "ttt_server.py")
client_path = os.path.join(current_dir, "ttt_client.py")

print("Launching multiplayer Tic-Tac-Toe...")
wait_for_keypress("Press any key to start server in a new tab.")

if sys.platform.startswith("darwin"):
    os.system(f'osascript -e \'tell application "Terminal" to do script "python3 {server_path}"\'')
else:
    subprocess.Popen(["python3", server_path])

time.sleep(1) 

print("Now launching client in this terminal...")
os.system(f"python3 {client_path}")
