from map import Map
from camera import Camera

WIDTH, HEIGHT = 800, 600

CAMERA = Camera(WIDTH, HEIGHT)
MAP = Map(1)

for tile in MAP.grid.values():
    tile.terrain = Actor("grassland")


def draw():
    screen.clear()
    MAP.draw(CAMERA)


def update():

    

    if keyboard.left:
        CAMERA.pos.x -= 15
    if keyboard.right:
        CAMERA.pos.x += 15
    if keyboard.up:
        CAMERA.pos.y -= 13
    if keyboard.down:
        CAMERA.pos.y += 13
