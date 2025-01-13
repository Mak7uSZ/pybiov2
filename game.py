import random
import socket
import time
from PIL import Image, ImageEnhance
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import *
from ursina.lights import DirectionalLight
from threading import Thread
import keyboard
from ursina.texture_importer import load_texture
from ursina import *
import threading
from queue import Queue
import select
from ursina import Vec3, Entity, color
from pathlib import Path
import socket
import threading
import json
import time
from ursina import Vec3
import keyboard
from ursina import *
from part1 import run_part1
# Функция, которая выводит сообщение при наведении на кнопку
from ursina import *
from perlin_noise import PerlinNoise
import random

import time
from PIL import Image, ImageEnhance
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import *
from ursina.lights import DirectionalLight
from threading import Thread
import keyboard
from ursina.texture_importer import load_texture
from ursina import *
from perlin_noise import PerlinNoise

import sys

if __name__ == "__main__":
    # Получаем аргументы командной строки
    if len(sys.argv) != 3:
        print("[ERROR] need to receive ip and the port")
        sys.exit(1)

    ip = sys.argv[1]  # Первый аргумент после имени файла
    port = sys.argv[2]  # Второй аргумент после имени файла

    print(f"[INFO] received ip: {ip}, port: {port}")

time.sleep(1)
server_ip = ip
server_port = int(port)


time.sleep(5)

while True:
        try:
            # Создаем сокет для подключения
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1)  # Устанавливаем таймаут 1 секунду
            client_socket.connect((server_ip, server_port))
            print(f"Успешно подключились к серверу на {ip}:{port}")
            data = client_socket.recv(1024)
            your_client_id = data.decode('utf-8').strip()
            print(f"[INFO] Received client ID: {your_client_id}")
            break  # Если подключение успешно, выходим из цикла
        except (socket.timeout, ConnectionRefusedError):
            print(f"Сервер еще не готов, повторная попытка через 1 секунду...")
            time.sleep(1)  # Пауза перед повторной попыткой

# Receive client ID
app = Ursina()

# Initialize Ursina
# Predefined models for other players
max_players = 10
initial_positions = [Vec3(0, 0, 0) for _ in range(max_players)]
players = {str(i): Entity(
    model='Models/Player.obj',
    scale=(1, 1, 1),
    position=initial_positions[i],
    color=color.random_color(),
    visible=False
) for i in range(max_players)}
assigned_clients = {}

print("[INFO] Predefined player models created.")

# Filter out own position from received data
def filter_own_position(client_id, positions_data):
    return {key: value for key, value in positions_data.items() if key != client_id}

# Receive positions from server
filtered_positions = {}
def receive_positions():
    global filtered_positions
    buffer = ""  # To handle incomplete messages
    while True:
        try:
            data = client_socket.recv(4096)
            if data:
                # Decode and add to buffer
                buffer += data.decode('utf-8')

                # Process complete messages in buffer
                while "\n" in buffer:  # Assuming newline is used as a delimiter
                    message, buffer = buffer.split("\n", 1)
                    try:
                        parsed_message = json.loads(message)
                        
                        # Check if message type is "positions"
                        if parsed_message.get("type") == "positions":
                            positions_data = parsed_message.get("data")
                            if isinstance(positions_data, dict):
                                filtered_positions = filter_own_position(your_client_id, positions_data)
                                print(f"[DEBUG] Filtered positions: {filtered_positions}")
                            else:
                                print(f"[ERROR] Positions data is not a valid dictionary: {positions_data}")
                        else:
                            print(f"[INFO] Received non-positions message: {parsed_message}")
                    except json.JSONDecodeError:
                        print(f"[ERROR] Failed to decode JSON message: {message}")
        except Exception as e:
            print(f"[ERROR] Error receiving data (positions): {e}")



def receive_tijd():
    global servertijd
    while True:
        try:
            # Receive data from the socket
            tijd_data = client_socket.recv(4096)
            if tijd_data:
                # Decode and parse JSON from the received data
                servertijd = json.loads(tijd_data.decode('utf-8'))
                print(f"[DEBUG] received tijd: {servertijd}")
        except Exception as e:
            print(f"[ERROR] Error receiving data(tijd): {e}")


# Update player positions
def update_player_positions():
    global filtered_positions, players, assigned_clients
    while True:
        # Assign or update models for connected clients
        for client_id, position in filtered_positions.items():
            if client_id not in assigned_clients:
                # Assign an available model
                available_model = next((p for p_id, p in players.items() if p_id.isdigit() and not p.visible), None)
                if available_model:
                    available_model.visible = True
                    available_model.position = Vec3(position['x'], position['y'], position['z'])
                    assigned_clients[client_id] = available_model
                    print(f"[DEBUG] Assigned model to client {client_id}")
                else:
                    print(f"[ERROR] No available model for client {client_id}")
            else:
                # Update the assigned model's position
                assigned_clients[client_id].position = Vec3(position['x'], position['y'], position['z'])
                print(f"[DEBUG] Updated position for client {client_id} to {position}")

        # Return unassigned models to their initial positions
        for client_id in list(assigned_clients.keys()):
            if client_id not in filtered_positions:
                model = assigned_clients.pop(client_id)
                model.position = Vec3(0, 0, 0)
                model.visible = False
                print(f"[DEBUG] Returned model for client {client_id} to initial position.")

        time.sleep(0.1)  # Задержка перед следующим обновлением



# Send player position to the server
def send_position_data():
    while True:
        try:
            player_position = {'x': player.x, 'y': player.y, 'z': player.z}
            client_socket.send(json.dumps(player_position).encode('utf-8'))
            print(f"[INFO] Sent position data: {player_position}")
        except Exception as e:
            print(f"[ERROR] Error sending position data: {e}")
        time.sleep(0.1)

# Start threads
Thread(target=receive_tijd, daemon=True).start()
Thread(target=receive_positions, daemon=True).start()
Thread(target=update_player_positions, daemon=True).start()
Thread(target=send_position_data, daemon=True).start()


random.seed(port)
Entity.default_shader = unlit_shader
sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))

# 4096 x 1024 JPG
# sky = Sky(texture="Textures/skybox.jpg")

noise = PerlinNoise(octaves=3, seed=random.randint(0, 1000))
level_parent = Entity(model=Mesh(vertices=[], uvs=[]), color=color.white)

amp = 3
freq = 24
width = 2

for x in range(1, width):
    for z in range(1, width):
        # add two triangles for each new point
        y00 = noise([x/freq, z/freq]) * amp
        y10 = noise([(x-1)/freq, z/freq]) * amp
        y11 = noise([(x-1)/freq, (z-1)/freq]) * amp
        y01 = noise([x/freq, (z-1)/freq]) * amp
        level_parent.model.vertices += (
            # first triangle
            (x, y00, z),
            (x-1, y10, z),
            (x-1, y11, z-1),
            # second triangle
            (x, y00, z),
            (x-1, y11, z-1),
            (x, y01, z-1)
        )

level_parent.model.generate()
level_parent.model.project_uvs() # for texture
level_parent.model.generate_normals() # for lighting
level_parent.collider = 'mesh'
level_parent.world_scale = 50  # for collision
#ground = Entity(model='Models/Newterrain.obj', collider='mesh', scale=4, texture='Textures/TerrainTexture.png')
# murren = Entity(model='Models/skyrealtrustme.obj', collider='mesh', scale=4, texture='Textures/homo.nl.png',texture_scale=(1,1))
water = Entity(model='Models/Water.obj', scale=4, texture='Textures/Daunload.jpg', texture_scale=(128,128), collider='box')
# water.collision = True
human_cacher = Entity(model="Models/Human catcher.obj", collider='mesh', scale=4, texture_scale=(128,128))
human_cacher.position_y = 100

infiniter = Mesh(vertices=[[0,0,0], [10,0,0], [0,0,10], [10,0,10]],
                 triangles=[[0,1,2]])

ground = Entity(model=infiniter)


editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='Models/Player.obj', scale=(1,1,1), z=-10, color="27DCA3", origin_y=-.9, speed=20, collider='box')

player._collider = BoxCollider(player, (0,0,0), (0.5, 1, 0.5))
player.position = Vec3(0, 200, 0)
camera.fov = 90
gun = Entity(model='Models/hand.obj', parent=camera, position=(.5,-.25,1.8), scale=(.3,.2,.2), origin_z=-.5, texture="Textures/handtexture.png")
gun.world_rotation_y=70
gun.world_rotation_x=-20


gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
text_entity = Text(f"Food:", world_scale=48)
text_entity.world_position = (-17.5, 9.5)
text_entity.always_on_top = True
ip_port = Text(f"{ip}: {port}", scale=1)
ip_port.world_position = (10, 9.9)




wp = Panel(
    title='',
    content=(
        ),
    popup=False
    )

watertex = Panel(
    title='',
    content=(
        ),
    popup=False
    )
watertex.texture = "Textures/underwater.png"
watertex.position = window.center
watertex.scale = (2, 2)
watertex.color = color.blue
watertex.scale = (0,0)

sleeptex = Panel(
    title='',
    content=(
        ),
    popup=False
    )
sleeptex.position = window.center
sleeptex.scale = (2, 2)
sleeptex.color = color.black
sleeptex.scale = (0,0)


wp.scale = (0.6,0.2)
wp.position = window.top_left    # center the window panel

hungertex = Panel(
    title='',
    content=(),
    popup=False,
    scale = (0.05,0.18),
    enabled = True,
    position = window.top_left,
    color = color.yellow
)
    # center the window panel


#text_entity.food = 59
# text_entity.screen_position = window.top_right
katerpilaarlist = []
shootables_parent = Entity()
mouse.traverse_target = shootables_parent
kwit = False
localtime = 0
food = 5
skybox = Sky()
text_entity2 = Text("sigma", world_position = (-20, -20))
def skyboxManager():
    global food
    #text_entity2.text = Text("g", world_scale=48)
    global kwit
    if kwit:
        app.closeWindow()
        quit()
    
    global localtime
    image_list = ["sky_night.jpg", "sky_morning.jpg", "Middag.jpg", "sky_sunset.jpg"]
    skybox_images = [load_texture(tex) for tex in image_list]
    
    while kwit == False:
        
        time.sleep(1)
        if localtime > 0 and localtime < 60:
            skybox.texture = skybox_images[0]
            text_entity2.world_position = (-5, -5)
            text_entity2.world_scale = (48, 48) 
        if localtime > 59 and localtime < 120:
            skybox.texture = skybox_images[1]
        if localtime > 119 and localtime < 180:
            skybox.texture = skybox_images[2]
        if localtime > 179 and localtime < 240:
            text_entity2.text = f" " 
            text_entity2.world_position = (-5, -5)
            text_entity2.world_scale = (48, 48)
            skybox.texture = skybox_images[3]
        if localtime > 239:
            localtime = 0
        if localtime > 180 or localtime < 60:
            if keyboard.is_pressed("f") and player.intersects(ground).hit == True and player.intersects(water).hit == False:
                sleeptex.scale = (2,2)
                time.sleep(2)
                sleeptex.scale = (0,0)
                text_entity2.world_scale = (0,0)
                localtime = 70
                food -= 2
            
        localtime += 1
        

        
          
def HungerManager():
    global localtime
    global kwit
    global katerpilaarlist
    global food
    foodcounter = 0
    katerpilaarcounter = 0
    while True:
        if foodcounter == 30:
            food -= 1
            foodcounter = 0
            r = random.randint(0, len(katerpilaarlist) - 1)
            destroy(katerpilaarlist[r])
            katerpilaarlist.pop(r)
        
        # if held_keys["f"] and player.intersects(ground).hit == True and player.intersects(water).hit == False:
        #     food -= 2
        #     time.sleep(5)
            
        if katerpilaarcounter == 60 and localtime > 59 and localtime < 180:
            
            enemys = ["Models/mug.obj", "Models/vlinder.obj", "Models/zijdeplant.obj", "Models/kever.obj", "Models/lag vrije katerpilaar.obj"]

            spawnposses = [Vec3(-165.8, -4.33329, 43.9855), Vec3(-108.996, 0.744841, 40.3109),
                           Vec3(-97.5293, -16.0675, 54.1008), Vec3(-54.0972, -7.16099, 41.828),
                           Vec3(-7.40389, 3.42633, 28.4597),
                           Vec3(65.6728, -34.1341, 44.3059), Vec3(49.0393, -14.6137, -5.87056),
                           Vec3(43.6286, -9.30014, -48.3134), Vec3(32.8666, -0.409023, -99.8582),
                           Vec3(45.8275, -9.80014, -167.249), Vec3(62.0548, -18.1419, -190.311),
                           Vec3(96.6821, -2.47574, -125.344), Vec3(89.6741, -10.3001, -88.6823),
                           Vec3(88.3617, -15.8764, -33.4703), Vec3(113.022, -6.81619, 41.7727),
                           Vec3(120.526, -34.995, 75.1187), Vec3(175.884, -18.2383, 71.6165)]
            
            randomnumber = random.randint(0, 16)
            sigma_vector = spawnposses[randomnumber]
            randomnubmer2 = random.randint(0, 5)
            sigma_enemy = enemys[randomnubmer2]
            enemy = Entity(model=sigma_enemy, origin_y=-.5, scale=1, texture='Textures/kakkerpilaar.png',
                           texture_scale=(1, 2), collider="box")
            enemy.world_position = sigma_vector
            katerpilaarlist.append(enemy)
            
            randomnumber = random.randint(0, 16)
            sigma_vector = spawnposses[randomnumber]
            randomnubmer2 = random.randint(0, 5)
            sigma_enemy = enemys[randomnubmer2]
            enemy = Entity(model=sigma_enemy, origin_y=-.5, scale=1, texture='Textures/kakkerpilaar.png',
                           texture_scale=(1, 2), collider="box")
            enemy.world_position = sigma_vector
            katerpilaarlist.append(enemy)

            randomnubmer2 = random.randint(0, 5)
            sigma_enemy = enemys[randomnubmer2]
            
            randomnumber = random.randint(0, 16)
            sigma_vector = spawnposses[randomnumber]
            enemy = Entity(model=sigma_enemy, origin_y=-.5, scale=1, texture='Textures/kakkerpilaar.png',
                           texture_scale=(1, 2), collider="box")
            enemy.world_position = sigma_vector
            katerpilaarlist.append(enemy)

        hungertex.scale = ((0.6 * food / 10), 0.18)
        
        foodcounter += 1
        katerpilaarcounter += 1

        time.sleep(1)
        if food == 0:
            text_entity.text = f"you starved to death"
            text_entity.world_scale = 144

            time.sleep(5)
            kwit = True
            
        if food > 10:
            text_entity.text = f"you died to diabetes"
            text_entity.world_scale = 144
        
        if kwit:
            break
        runForLoop = True
        for e in range(len(katerpilaarlist) - 1):
            if runForLoop:
                #print(distance(player, katerpilaarlist[e]))
                if distance(player, katerpilaarlist[e]) < 20:
                    katerpilaarlist[e].scale = 0
                    destroy(katerpilaarlist[e])
                    katerpilaarlist.pop(e)
                    food += 2
                    runForLoop = False

        text_entity.text = f"Food: {food}"

        if keyboard.is_pressed("tab"):
            break


stop_threads = False
Thread(target=HungerManager).start()
Thread(target=skyboxManager).start()

for i in range(2):
    spawnposses = [Vec3(-165.8, -4.33329, 43.9855), Vec3(-108.996, 0.744841, 40.3109), Vec3(-97.5293, -16.0675, 54.1008), Vec3(-54.0972, -7.16099, 41.828), Vec3(-7.40389, 3.42633, 28.4597),
               Vec3(65.6728, -34.1341, 44.3059), Vec3(49.0393, -14.6137, -5.87056), Vec3(43.6286, -9.30014, -48.3134), Vec3(32.8666, -0.409023, -99.8582),Vec3(45.8275, -9.80014, -167.249), Vec3(62.0548, -18.1419, -190.311),
               Vec3(96.6821, -2.47574, -125.344), Vec3(89.6741, -10.3001, -88.6823), Vec3(88.3617, -15.8764, -33.4703), Vec3(113.022, -6.81619, 41.7727), Vec3(120.526, -34.995, 75.1187), Vec3(175.884, -18.2383, 71.6165)]

    enemys = ["Models/mug.obj", "Models/vlinder.obj", "Models/zijdeplant.obj", "Models/kever.obj", "Models/lag vrije katerpilaar.obj"]

    randomnumber = random.randint(0, 16)
    sigma_vector = spawnposses[randomnumber]
    randomnubmer2 = random.randint(0, 5)
    sigma_enemy = enemys[randomnubmer2]
    enemy = Entity(model=sigma_enemy, origin_y=-.5, scale=1, texture='Textures/kakkerpilaar.png',
                           texture_scale=(1, 2), collider="box")
    katerpilaarlist.append(enemy)
    enemy.world_position = sigma_vector
    randomnumber = random.randint(0, 16)
    sigma_vector = spawnposses[randomnumber]
    enemy = Entity(model=sigma_enemy, origin_y=-.5, scale=1, texture='Textures/kakkerpilaar.png',
                           texture_scale=(1, 2), collider="box")
    enemy.world_position = sigma_vector
    katerpilaarlist.append(enemy)
    print(f"katterpillar {i}")

currenseed = 1

def update():
    
    global currenseed
    currenseed += 1
    random.seed(currenseed)
    if kwit:
        quit()
    touchingland = False

    if player.intersects(ground).hit:
        touchingland = True     
    else:
        touchingland = False
    
    if player.intersects(water).hit == True:
        watertex.scale = (2, 2)
    else:
        watertex.scale = (0, 0)
    if player.intersects(water).hit:
        if keyboard.is_pressed('space'):
            print(player.gravity)
        # if held_keys['space']:
            
            # player.y += 1
            player.gravity = -5
            print(player.gravity)
        else:
            if touchingland == False:
                player.y -= 1
                player.gravity = 0
        #print("toucher water")
    else:
        player.gravity = 1
        #pass
    #    player.gravity = 1




from ursina.prefabs.health_bar import HealthBar
def pause_input(key):
    if key == 'escape':    # press tab to toggle edit/play mode
        global kwit
        kwit = True
        quit()
        # editor_camera.enabled = not editor_camera.enabled

        # player.visible_self = editor_camera.enabled
        # player.cursor.enabled = not editor_camera.enabled
        # gun.enabled = not editor_camera.enabled
        # mouse.locked = not editor_camera.enabled
        # editor_camera.position = player.position
        
        #application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)



sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
app.run()
