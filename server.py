import socket
import pickle
from tic_tac_toe import init_board, is_winner, is_full, insert_letter
import threading


HOST = "0.0.0.0"
PORT = 12345
rooms = {}
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)
print("Server listening on port", PORT)
