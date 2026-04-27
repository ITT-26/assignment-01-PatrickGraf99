import math
import socket
import time
import json
import random

# Setup socket, copied from demo

IP = '127.0.0.1'
PORT = 5700

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def encode_and_send(data):
    soc.sendto(json.dumps(data).encode(), (IP, PORT))

def main():
    print('starting up')
    # Helper vars
    loop_counter: int = 0
    was_pressed: bool = False

    sine_vars = {
        'x': (random.randint(0, 10)),
        'y': (random.randint(0, 10)),
        'z': (random.randint(0, 10)),
        'offset': (random.randint(0, 10))
    }



    while True:
        if was_pressed:
            print('Button released')
            was_pressed: bool = False
            data: dict = {'button_1' : int(was_pressed)}
            encode_and_send(data)
        elif not was_pressed and random.random() < 0.05:
            print('Button pressed by chance')
            was_pressed: bool = True
            data: dict = {'button_1' : int(was_pressed)}
            encode_and_send(data)

        # Recommendation by chatGPT:
        # Use sin, sin + offset and sin with different amplitude for each kind of data, add random noise to each one

        x = sine_vars['x'] * math.sin(loop_counter)
        y = sine_vars['y'] * math.sin(loop_counter + sine_vars['offset'])
        z = sine_vars['z'] * math.sin(2 * loop_counter)

        accel_data = {'accelerometer': [x, y, z]}
        encode_and_send(accel_data)

        loop_counter += 1
        time.sleep(1)

main()