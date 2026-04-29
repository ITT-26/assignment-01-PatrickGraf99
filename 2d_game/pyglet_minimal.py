import time
from enum import Enum

import pyglet
from pyglet import window, shapes
from pyglet.window import key

from DIPPID import SensorUDP
# Copied from DIPPID_receiver
# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    NONE = 2

class GameState(Enum):
    PAUSED = 0
    RUNNING = 1

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SQUARE_SIZE = 20

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
player_squares = []

movement_update = (0, 0)
curr_direction = Direction.NONE
waiting_for_update = False
game_state = GameState.RUNNING

head = shapes.Rectangle(
    WINDOW_WIDTH / 2 - SQUARE_SIZE / 2,
    WINDOW_HEIGHT / 2 - SQUARE_SIZE / 2,
    SQUARE_SIZE,
    SQUARE_SIZE,
    (255, 0, 0)
)

player_squares.append(head)

def handle_button_1_data(data):
    if data == 0:
        return
    global curr_direction, movement_update, game_state, waiting_for_update
    if waiting_for_update:
        print('Input was ignored since the game has not been updated since last change')
        return
    if curr_direction != Direction.HORIZONTAL:
        print('Moving left')
        curr_direction = Direction.HORIZONTAL
        movement_update = (-SQUARE_SIZE, 0)
    waiting_for_update = True

def handle_button_2_data(data):
    if data == 0:
        return
    global curr_direction, movement_update, game_state, waiting_for_update
    if waiting_for_update:
        print('Input was ignored since the game has not been updated since last change')
        return
    if curr_direction != Direction.HORIZONTAL:
        print('Moving right')
        curr_direction = Direction.HORIZONTAL
        movement_update = (SQUARE_SIZE, 0)
    waiting_for_update = True

def handle_button_3_data(data):
    if data == 0:
        return
    global curr_direction, movement_update, game_state, waiting_for_update
    if waiting_for_update:
        print('Input was ignored since the game has not been updated since last change')
        return
    if curr_direction != Direction.VERTICAL:
        print('Moving up')
        curr_direction = Direction.VERTICAL
        movement_update = (0, SQUARE_SIZE)
    waiting_for_update = True

def handle_button_4_data(data):
    if data == 0:
        return
    global curr_direction, movement_update, game_state, waiting_for_update
    if waiting_for_update:
        print('Input was ignored since the game has not been updated since last change')
        return
    if curr_direction != Direction.VERTICAL:
        print('Moving down')
        curr_direction = Direction.VERTICAL
        movement_update = (0, -SQUARE_SIZE)
    waiting_for_update = True

sensor.register_callback('button_1', handle_button_1_data)
sensor.register_callback('button_2', handle_button_2_data)
sensor.register_callback('button_3', handle_button_3_data)
sensor.register_callback('button_4', handle_button_4_data)


def update_movement(movement, direction):
    global movement_update, curr_direction

    movement_update = (movement[0], movement[1])
    curr_direction = direction

def draw_player_squares():
    for square in player_squares:
        square.draw()


def update_player_squares(dt):
    global game_state, waiting_for_update
    waiting_for_update = False
    if game_state == GameState.PAUSED:
        return
    head_square = True
    next_position = None
    for square in player_squares:
        if head_square:
            next_position = square.position
            square.position = square.position[0] + movement_update[0], square.position[1] + movement_update[1]
            head_square = False
        else:
            tmp = square.position
            square.position = next_position
            next_position = tmp

@win.event
def on_draw():
    win.clear()
    draw_player_squares()

@win.event
def on_key_press(symbol, modifiers):
    global curr_direction, movement_update, game_state, waiting_for_update
    if waiting_for_update:
        print('Input was ignored since the game has not been updated since last change')
        return
    if symbol == key.LEFT and curr_direction != Direction.HORIZONTAL:
        print('Moving left')
        curr_direction = Direction.HORIZONTAL
        movement_update = (-SQUARE_SIZE, 0)
    elif symbol == key.RIGHT and curr_direction != Direction.HORIZONTAL:
        print('Moving right')
        curr_direction = Direction.HORIZONTAL
        movement_update = (SQUARE_SIZE, 0)
    elif symbol == key.UP and curr_direction != Direction.VERTICAL:
        print('Moving up')
        curr_direction = Direction.VERTICAL
        movement_update = (0, SQUARE_SIZE)
    elif symbol == key.DOWN and curr_direction != Direction.VERTICAL:
        print('Moving down')
        curr_direction = Direction.VERTICAL
        movement_update = (0, -SQUARE_SIZE)
    waiting_for_update = True


pyglet.clock.schedule_interval(update_player_squares, .5)
pyglet.app.run()
