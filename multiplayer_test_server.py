import socket
from threading import Thread
from time import sleep

HOST = ''
PORT = 3653

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

motions = []
sockets = []

server_socket.listen()

def main():
    while True:
        client_socket, addr = server_socket.accept()
        print('connected by ', addr)

        for i in sockets:
            i.send('new_player'.encode())
        for i in range(len(sockets)):
            client_socket.send('new_player'.encode())
        sockets.append(client_socket)
        client_socket.send('=urindex:{}='.format(int(len(sockets)-1)).encode())

        def listener():
            first_data = client_socket.recv(1024).decode()
            motions.append(first_data)
            my_index = int(len(sockets)-1)
            while True:
                data = sockets[my_index].recv(1024).decode()
                sleep(0.02)
                motions[my_index] = data

        def speaker():
            my_index = int(len(sockets) - 1)
            while True:
                tosend = ''
                for i in motions:
                    tosend += i+'/'
                sockets[my_index].send(tosend.encode())
                sleep(0.01)

        listener_thread = Thread(target=listener)
        speaker_thread = Thread(target=speaker)

        listener_thread.start()
        speaker_thread.start()

main_thread = Thread(target=main)
main_thread.start()