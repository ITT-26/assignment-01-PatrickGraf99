from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_accel_data(data):
    print(f'Received accel data: {data}')

def handle_button_data(data):
    state = 'ON' if data == 1 else 'OFF'
    print(f'Received button data, new state: {state}')

sensor.register_callback('button_1', handle_button_data)
sensor.register_callback('accelerometer', handle_accel_data)
