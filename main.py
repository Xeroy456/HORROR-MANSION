from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# =========================
# AUDIO
# =========================
musique = Audio('sounds/musique/horror.mp3', loop=True, autoplay=True)
musique.volume = 0.5

# =========================
# MENU
# =========================
main_menu = Entity(parent=camera.ui)
main_menu.enabled = True

background = Entity(
    parent=main_menu,
    model='quad',
    texture='assets/background.png',
    scale=(3, 2),
    color=color.gray,
    z=1
)

title = Text(
    parent=main_menu,
    text='HORROR MANSION',
    font='assets/creepster.ttf',
    scale=3,
    color=color.rgb(90, 0, 0),
    origin=(0, 0),
    y=0.35
)

# =========================
# GLOBALS
# =========================
player = None
door = None
door_open = False


direction = 1
timer = 0

fog_intensity = 1
fog_target = 0.25

fog_sphere = None

# =========================
# ENVIRONMENT
# =========================
ground = Entity(
    model='plane',
    scale=(200, 1, 200),
    texture='grass',
    texture_scale=(200, 200),
    color=color.gray,
    collider='box'
)
ground.enabled = False

# =========================
# FOG SYSTEM
# =========================
def create_fog_volume():
    global fog_sphere

    fog_sphere = Entity(
        model='sphere',
        scale=1200,
        color=color.dark_gray,
        double_sided=True,
        unlit=True
    )

def update_fog():
    global fog_intensity

    if main_menu.enabled:
        return

    fog_intensity = lerp(fog_intensity, fog_target, time.dt * 4)

    scene.fog_color = color.gray
    scene.fog_density = fog_intensity * 3
    scene.fog_start = 0
    scene.fog_end = 12

    if fog_sphere and player:
        fog_sphere.position = player.position + Vec3(0, 1, 0)
        fog_sphere.rotation_y += time.dt * 2

# =========================
# BUTTONS
# =========================
def create_button(parent, txt, y, action):
    btn = Button(
        text=txt,
        parent=parent,
        y=y,
        scale=(0.4, 0.1),
        color=color.black,
        highlight_color=color.red,
        pressed_color=color.black,
        text_color=color.red,
        on_click=action
    )

    base_scale = btn.scale
    base_y = btn.y

    def on_enter():
        btn.animate_scale(base_scale * 1.1, duration=0.1)
        btn.animate_y(base_y + 0.01, duration=0.1)

    def on_exit():
        btn.animate_scale(base_scale, duration=0.1)
        btn.animate_y(base_y, duration=0.1)

    def on_click():
        btn.animate_scale(base_scale * 0.95, duration=0.05)
        invoke(lambda: btn.animate_scale(base_scale * 1.1, duration=0.05), delay=0.05)
        invoke(lambda: btn.animate_scale(base_scale, duration=0.1), delay=0.1)
        action()

    btn.on_mouse_enter = on_enter
    btn.on_mouse_exit = on_exit
    btn.on_click = on_click

    return btn

# =========================
# GAME
# =========================
def start_game():
    global player

    main_menu.enabled = False
    Sky(color=color.dark_gray)

    ground.enabled = True

    player = FirstPersonController()
    player.position = (0, 1, -5)
    player.speed = 5
    player.cursor.visible = True

    create_fog_volume()

    window.color = color.rgb(20, 20, 20)

def quit_game():
    application.quit()

def update():

    if held_keys["g"]:
        player.position = (0, 0.5, -5)

# =========================
# UI BUTTONS
# =========================
create_button(main_menu, 'NEW GAME', 0.1, start_game)
create_button(main_menu, 'OPTIONS', -0.1, lambda: print('Options'))
create_button(main_menu, 'QUIT', -0.3, quit_game)

# =========================
# UPDATE LOOP
# =========================
def update():
    global direction, timer

    update_fog()

    if not main_menu.enabled:
        return

    timer += time.dt

    if timer >= 5:
        direction *= -1
        timer = 0

    background.rotation_z += time.dt * 0.7 * direction


app.run()