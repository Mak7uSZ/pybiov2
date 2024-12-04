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
app = Ursina()

# Initialize player (FirstPersonController)
player = FirstPersonController()

server_ip = "127.0.0.1"
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the server
try:
    client_socket.connect((server_ip, server_port))
    print("Connected to server")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

# Receive the client ID from the server
# Receive the client ID from the server
data = client_socket.recv(1024)  # Receive initial client ID
your_client_id = data.decode('utf-8').strip().strip('"')
print(f"Received client ID: {repr(your_client_id)}")  # Выводим для проверки

def filter_own_position(client_id, positions_data):
    filtered = {key: value for key, value in positions_data.items() if key != client_id}
    return filtered

# Function to continuously receive position data from the server
filtered_positions = {}

def receive_positions():
    global filtered_positions
    while True:
        try:
            # Receive position data from the server
            data = client_socket.recv(4096)  # Buffer size of 4096 bytes
            if data:
                try:
                    # Try decoding and parsing the data
                    positions_data = json.loads(data.decode('utf-8'))  # Convert from JSON to dictionary
                    print(f"Received positions data: {positions_data}")

                    # Filter out own position using filter() function
                    print(f"Your client ID: {repr(your_client_id)}")
                    print(f"Available keys: {repr(positions_data.keys())}")

                    filtered_positions = filter_own_position(your_client_id, positions_data)

                    print(f"Filtered positions: {filtered_positions}")

                    # Handle the filtered data (e.g., update game state, display positions)
                    for client_id, position in filtered_positions.items():
                        print(f"Client ID: {client_id}, Position: {position}")
                except json.JSONDecodeError as e:
                    # Handle JSON decode error and retry immediately
                    print(f"Error decoding JSON: {e}. Retrying...")
                except KeyError as e:
                    # Handle missing keys in the data and retry immediately
                    print(f"Error: Missing key {e} in the received data. Retrying...")
                except Exception as e:
                    # Handle any other unexpected exceptions and retry immediately
                    print(f"Unexpected error: {e}. Retrying...")
            else:
                # If no data is received, retry immediately
                print("No data received from server. Retrying...")

        except Exception as e:
            # Catch errors when receiving data and retry immediately
            print(f"Error receiving data: {e}. Retrying...")


# Assuming `your_client_id` is the ID of your own client, which you already have

# Dictionary to store existing player models (if not already created

# Update loop to check filtered_positions and create model

# Store created player models
player_entities = {}  # Ключ: client_id, Значение: Entity


def create_player_model(client_id):
    """Creates or updates a player model based on the given coordinates."""
    position = filtered_positions[client_id]

    # If the entity already exists, remove it
    if client_id in player_entities:
        print(f"Removing old entity for client {client_id}")
        player_entities[client_id].disable()
        del player_entities[client_id]

    # Create a new entity
    print(f"Creating a new entity for client {client_id} at coordinates {position}")
    entity = Entity(
        model='cube',
        color=color.random_color(),
        scale=2,
        position=(position['x'], position['y'], position['z']),
    )
    player_entities[client_id] = entity  # Save the entity in the dictionary


def update_player_positions():
    """Updates player entities based on data in filtered_positions."""
    while True:
        for client_id in filtered_positions.keys():
            create_player_model(client_id)

        if not filtered_positions:
            print("No new entities created and positions not updated.")  # Message if dictionary is empty
        time.sleep(0.1)  # Minimal delay


# Start a thread to update positions


# Запускаем поток для обновления позиций

def generate_models_from_positions():
    """Создаёт новые модели для всех клиентов из filtered_positions."""
    while True:
        for client_id, position in filtered_positions.items():
            if client_id not in known_clients:
                create_player_model(position)  # Создаём модель
                known_clients.add(client_id)  # Помечаем клиента как обработанного
        time.sleep(0.1)  # Минимальная задержка, чтобы не загружать процессор

# Function to send position data
def send_position_data():
    while True:
        # Prepare position data
        position_data = {'x': player.x, 'y': player.y, 'z': player.z}
        # Convert position data to JSON format
        data = json.dumps(position_data)
        # Send position data to the server
        try:
            client_socket.send(data.encode('utf-8'))
            print(f"Sent position data: {position_data}")
        except Exception as e:
            print(f"Error sending data to server: {e}")
        time.sleep(0.1)  # Sending position data every 100ms


Thread(target=update_player_positions, daemon=True).start()
# Start the receiving data thread
Thread(target=receive_positions, daemon=True).start()

# Start the networking thread to send position data
Thread(target=send_position_data, daemon=True).start()

# Run the Ursina app

random.seed(5598838209432810483439819859573091790609162098376087326875287218593720980732109328532575197859732905798327967438960256076943109874198759843)
Entity.default_shader = unlit_shader
sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))

# 4096 x 1024 JPG
# sky = Sky(texture="Textures/skybox.jpg")

ground = Entity(model='Models/Newterrain.obj', collider='mesh', scale=4, texture='Textures/TerrainTexture.png')
#murren = Entity(model='Models/skyrealtrustme.obj', collider='mesh', scale=4, texture='Textures/homo.nl.png',texture_scale=(1,1))
water = Entity(model='Models/Water.obj', scale=4, texture='Textures/Daunload.jpg', texture_scale=(128,128), collider='box')
water.collision = True
human_cacher = Entity(model="Models/Human catcher.obj", collider='mesh', scale=4, texture_scale=(128,128))
human_cacher.position_y = 100

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='Models/Player.obj', scale=(1,1,1), z=-10, color="27DCA3", origin_y=-.9, speed=20, collider='box')

# Assuming player models are already created for each client and stored in a dictionary
# The player_models dictionary holds the model reference using the client_id as the key
# We only need to update their positions

# Dictionary to store existing player models (if not already created)
# Assuming `your_client_id` is the ID of your own client, which you already have

# Dictionary to store existing player models (if not already created)
# Assuming `your_client_id` is the ID of your own client, which you already have

# Dictionary to store existing player models (if not already created)




player._collider = BoxCollider(player, (0,0,0), (0.5, 1, 0.5))
player.position = Vec3(0, 60, 0)
camera.fov = 100
gun = Entity(model='Models/hand.obj', parent=camera, position=(.5,-.25,1.8), scale=(.3,.2,.2), origin_z=-.5, texture="Textures/handtexture.png")
gun.world_rotation_y=70
gun.world_rotation_x=-20


gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
text_entity = Text(f"Food:", world_scale=48)
text_entity.world_position = (-17.5, 9.5)
text_entity.always_on_top = True



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

hunger = Panel(
    title='',
    content=(
        ),
    popup=False
    )

hunger.scale = (0.05,0.18)
hunger.position = window.top_left    # center the window panel
hunger.color = color.yellow

hunger.enabled = True
#text_entity.food = 59
# text_entity.screen_position = window.top_right
katerpilaarlist = []
shootables_parent = Entity()
mouse.traverse_target = shootables_parent
kwit = False
localtime = 0
food = 5

text_entity2 = Text("sigma", world_position = (-20, -20))
def skyboxManager():
    global food
    #text_entity2.text = Text("g", world_scale=48)
    global kwit
    if kwit:
        app.closeWindow()
        quit()
    
    global localtime
    print("1")
    skybox_image1 = load_texture("sky_night.jpg")
    print("1")
    skybox_image2 = load_texture("sky_morning.jpg")
    print("1")
    skybox_image3 = load_texture("Middag.jpg")
    print("1")
    skybox_image4 = load_texture("sky_sunset.jpg")
    
    while kwit == False:
        
        time.sleep(1)
        if localtime > 0 and localtime < 60:
            Sky(texture=skybox_image1)
            text_entity2.world_position = (-5, -5)
            text_entity2.world_scale = (48, 48)
            text_entity2.text = f"Press F to sleep" 
        if localtime > 59 and localtime < 120:
            Sky(texture=skybox_image2)
        if localtime > 119 and localtime < 180:
            Sky(texture=skybox_image3)
        if localtime > 179 and localtime < 240:
            text_entity2.text = f"Press F to sleep" 
            text_entity2.world_position = (-5, -5)
            text_entity2.world_scale = (48, 48)
            Sky(texture=skybox_image4)
        if localtime > 239:
            localtime = 0
        if localtime > 180 or localtime < 60:
            if held_keys["f"] and player.intersects(ground).hit == True and player.intersects(water).hit == False:
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

        hunger.scale = ((0.6 * food / 10), 0.18)
        
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
    if player.intersects(water).hit == True and touchingland == False:
        if held_keys['space']:
            
            player.y += 1.2
            player.gravity = 0
        else:
            
            player.y -= 1
            player.gravity = 0
        #print("toucher water")
    else:
        pass
        #pass
    #    player.gravity = 1

    if player.intersects(human_cacher).hit:
        player.y = 20
        player.z = -10
        player.x = 0



    if held_keys['left mouse']:
       player.y += 10
       player.speed = 500
       player.y = 60
       player.z = -10
       player.x = 0
    elif held_keys['right mouse']:
       player.y -= 10
       player.speed = 500
    elif held_keys['middle mouse']:
       # player.y -= 10
       player.speed = 500
       player.gravity = 0
    else:
       player.speed = 20
       player.gravity = 1

from ursina.prefabs.health_bar import HealthBar
def pause_input(key):
    if key == 'escape':    # press tab to toggle edit/play mode
        global kwit
        kwit = True
        quit()
        #editor_camera.enabled = not editor_camera.enabled

        #player.visible_self = editor_camera.enabled
        #player.cursor.enabled = not editor_camera.enabled
        #gun.enabled = not editor_camera.enabled
        #mouse.locked = not editor_camera.enabled
        #editor_camera.position = player.position
        
        #application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)



sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
app.run()
