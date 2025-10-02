import selectors
import socket
import types
import random

HOST = '127.0.0.1'
PORT = 12345

sel = selectors.DefaultSelector()
waiting_player = None
games = {}  

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Client connected: {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=types.SimpleNamespace(addr=addr, inb=b"", outb=b""))
    global waiting_player
    if waiting_player:
        games[(waiting_player, conn)] = [' ']*9
        waiting_player.send(b"START:X\n")  
        conn.send(b"START:O\n")
        print("Game started!")
        waiting_player = None
    else:
        waiting_player = conn
        conn.send(b"WAITING\n")

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            handle_message(sock, recv_data.decode().strip())
        else:
            sel.unregister(sock)
            sock.close()
            print(f"Client disconnected: {data.addr}")

def handle_message(sock, msg):
    for (p1, p2), board in list(games.items()):
        if sock not in (p1, p2):
            continue
        other = p2 if sock == p1 else p1
        if msg.startswith("MOVE:"):
            idx = int(msg.split(":")[1])
            mark = 'X' if sock == p1 else 'O'
            if board[idx] == ' ':
                board[idx] = mark
                sock.send(f"OK:{idx}\n".encode())
                other.send(f"OPPONENT:{idx}\n".encode())

                winner = check_winner(board)
                if winner:
                    sock.send(f"WINNER:{winner}\n".encode())
                    other.send(f"WINNER:{winner}\n".encode())
                    del games[(p1, p2)]
                elif ' ' not in board:  
                    sock.send(b"DRAW\n")
                    other.send(b"DRAW\n")
                    del games[(p1, p2)]
        break


def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in wins:
        if board[combo[0]]==board[combo[1]]==board[combo[2]] != ' ':
            return board[combo[0]]
    return None


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
lsock.listen()
print("THIS IS THE SERVER!")
print(f"Server listening on {HOST}:{PORT}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sel.close()
