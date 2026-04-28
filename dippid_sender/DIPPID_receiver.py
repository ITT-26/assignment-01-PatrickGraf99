from DIPPID import SensorUDP
# Copied from demo
# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

# Handler for accelerometer data
def handle_accel_data(data):
    print(f'Received accel data: {data}')

# Handler for button data
def handle_button_data(data):
    state = 'ON' if data == 1 else 'OFF'
    print(f'Received button data, new state: {state}')

sensor.register_callback('button_1', handle_button_data)
sensor.register_callback('accelerometer', handle_accel_data)
