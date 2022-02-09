import socket
from threading import Thread
from time import sleep
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

HOST = open('ip.txt', 'r').read()
PORT = 3653

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

users = []
cycle = 0

app = Ursina()

player = FirstPersonController()

floor_texture = load_texture('floor.png')
floor = Entity(model='cube', scale_x=100, scale_z=100, color=color.white, collider='box', position=Vec3(0, -5, 0), texture = floor_texture)
wall1 = Entity(model='cube', scale_x=100, scale_y=100, collider='box', color=color.green, position=(0, 0, 50))
wall2 = Entity(model='cube', scale_x=100, scale_y=100, collider='box', color=color.blue, position=(0, 0, -50))
wall3 = Entity(model='cube', scale_z=100, scale_y=100, collider='box', color=color.red, position=(50, 0, 0))
wall4 = Entity(model='cube', scale_z=100, scale_y=100, collider='box', color=color.yellow, position=(-50, 0, 0))

sky_texture = load_texture('sky.jpg')
sky = Entity(model='sphere', scale=200, double_sided=True, texture=sky_texture)


def update():
    if held_keys['left shift']:
        player.speed = 10
    else:
        player.speed = 5

index_rel = client_socket.recv(1024).decode()
my_index = eval(index_rel.split('=')[1].split(':')[1])
print(my_index)

if 'new_player' in index_rel:
    new_player = Entity(model='cube', collider='box', color=color.violet)
    if my_index == len(users):
        users.append(player)
        print('True')
    users.append(new_player)

def listener():
    global users, cycle, my_index
    while True:
        data = client_socket.recv(1024).decode()
        sleep(0.01)
        if 'new_player' in data:
            new_player = Entity(model='cube', collider='box', color=color.violet)
            if my_index == len(users):
                users.append(player)
                print('True')
            users.append(new_player)
        else:
            try:
                if my_index == 1:
                    to_index = 0
                else:
                    to_index = 1
                motions = data.split('/')[to_index]
                position, rotation = motions.split('*')
                position, rotation = eval(position), eval(rotation)
                users[to_index].position = position
                users[to_index].rotation = rotation
            except Exception as e:
                #print(e)
                pass

def speaker():
    while True:
        client_socket.send('{}*{}'.format(player.world_position, camera.world_rotation).encode())
        sleep(0.03)

listener_thread = Thread(target=listener)
speaker_thread = Thread(target=speaker)

listener_thread.start()
speaker_thread.start()

app.run()