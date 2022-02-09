from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 3653

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    client_socket.send('cube,color.red'.encode())
except:
    print('not online')

app = Ursina()

player = FirstPersonController()

online_players = []
new_player_data = ''

def new_player(New_player_data):
    player_data = New_player_data.split(',')
    model, Color = player_data[0], player_data[1]
    New_player = Entity(model=model, collider='box', color=eval(Color))
    online_players.append(New_player)

def recving():
    global new_player_data, player
    while True:
        client_socket.send('{}*{}'.format(player.position, camera.world_rotation).encode())
        data = client_socket.recv(1024).decode()
        if data == 'new_player':
            new_player_data = client_socket.recv(1024).decode()
            new_player(new_player_data)
        else:
            players_movements = data.split('/')
            for a, i in enumerate(players_movements):
                try:
                    if i != '':
                        position, rotation = i.split('*')
                        position, rotation = eval(position), eval(rotation)
                        online_players[a].position = position
                        online_players[a].rotation = rotation
                except:
                    pass

recving_thread = Thread(target=recving)
recving_thread.start()

floor_texture = load_texture('floor.png')
target_texture = load_texture('target.png')
sky_texture = load_texture('sky.jpg')

floor = Entity(model='cube', scale_x=100, scale_z=100, collider='box', color=color.brown, texture=floor_texture)
wall1 = Entity(model='cube', scale_x=100, scale_y=100, collider='box', color=color.green, position=(0, 0, 50))
wall2 = Entity(model='cube', scale_x=100, scale_y=100, collider='box', color=color.blue, position=(0, 0, -50))
wall3 = Entity(model='cube', scale_z=100, scale_y=100, collider='box', color=color.red, position=(50, 0, 0))
wall4 = Entity(model='cube', scale_z=100, scale_y=100, collider='box', color=color.yellow, position=(-50, 0, 0))

sky = Entity(model='sphere', scale=200, double_sided=True, texture=sky_texture)

app.run()