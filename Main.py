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
app = Ursina()

random.seed(4326)
Entity.default_shader = unlit_shader
sun = DirectionalLight(shadow_map_resolution=(2048,2048))
sun.look_at(Vec3(-1,-1,-10))
sky = Sky(texture="Textures/skybox.jpg")

ground = Entity(model='Models/Newterrain.obj', collider='mesh', scale=4, texture='Textures/TerrainTexture.png')
#murren = Entity(model='Models/skyrealtrustme.obj', collider='mesh', scale=4, texture='Textures/homo.nl.png',texture_scale=(1,1))
water = Entity(model='Models/Water.obj', scale=4, texture='Textures/Daunload.jpg', texture_scale=(128,128), collider='box')
water.collision = True
human_cacher = Entity(model="Models/Human catcher.obj", collider='mesh', scale=4, texture_scale=(128,128))
human_cacher.position_y = 100

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='Models/Player.obj', scale=(1,1,1), z=-10, color="27DCA3", origin_y=-.9, speed=20, collider='box')

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


def skyboxManager():
    skybox_path = '3D enigne/Textures/skybox.jpg'
    enhanced_skybox_path = '3D enigne/Textures/enhanced_skybox.jpg'
    global kwit
    if kwit:
        app.closeWindow()
        quit()
    
    global localtime 
    skybox1 = Image.open(skybox_path)
    while kwit == False:
        # Текущее время в 24-секундном цикле
        localtime = int(time.time() % 24)  # Оставляем только секунды в пределах 24 секунд
        print(f"\r24-seconden tijd: {localtime:02d}", end="")
        time.sleep(0.1)  # Обновляем каждые 100 мс для плавности
        # total_seconds = int(time.time()) % (24 * 60) 
        # localtime = total_seconds // 60
        # seconds = total_seconds % 60
        enchanche_percent = 1 + localtime / 10
        for localtime in range(1, 24):
            enhancer = ImageEnhance.Contrast(skybox1)
            contrast_skybox = enhancer.enhance(enchanche_percent)
            # co                                                                                                                                                                                                                                                                                                                                                            m,ntrast_skybox.save(enhanced_skybox_path, format='JPEG')
            
        skybox1_image = load_texture("3D enigne/Textures/enhanced_skybox.jpg")
        Sky(texture=skybox1_image)
        
    
def HungerManager():
    global kwit
    global katerpilaarlist
    food = 3
    foodcounter = 0
    katerpilaarcounter = 0
    while True:
        if foodcounter == 30:
            food -= 1
            foodcounter = 0
            r = random.randint(0, len(katerpilaarlist) - 1)
            destroy(katerpilaarlist[r])
            katerpilaarlist.pop(r)
        if katerpilaarcounter == 60:
            
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



def update():
    if kwit:
        quit()
    touchingland = False

    if player.intersects(ground).hit:
        touchingland = True
        # watertex.scale = (0,0)
    # elif player.intersects(water).hit:
        
        
    else:
        touchingland = False
        

    print(touchingland, player.intersects(water).hit)
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