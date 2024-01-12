import serial
import time

# Motor and Pulley Specifications
motorStepsPerRevolution = 800
pulleyRatio = 32.0 / 20.0
outputStepsPerRevolution = motorStepsPerRevolution * pulleyRatio
degreesPerStep = 360.0 / outputStepsPerRevolution

# Function to send a command to the motor and wait for confirmation
def move_motor_and_wait(arduino, degrees):
    arduino.write(f"GO{degrees}\n".encode())
    print(f"GO{degrees}\n".encode())
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"Received from Arduino: {response}")  # Debugging line
            if response.startswith("AT"):
                break
    time.sleep(0.2)  # Reduced settling time for testing


# Function to read the gauge
def read_gauge(gauge):
    gauge.write(b"R4\r")
    time.sleep(0.1)  # Short delay for gauge to respond
    return gauge.readline().decode().strip()

# Configurable angle increment
angle_increment = 60  # Degrees to move per step

# Open serial ports
arduino = serial.Serial('COM19', 115200, timeout=2)
gauge = serial.Serial('COM10', 38400, timeout=1)

arduino.write(f"GO60\n".encode())


try:
    current_angle = 0
    while current_angle < 360:
        move_motor_and_wait(arduino, angle_increment)
        measurement = read_gauge(gauge)
        print(f"{current_angle},{measurement}")
        current_angle += angle_increment
        time.sleep(0.5)  # Additional delay if needed

finally:
    # Close serial ports
    arduino.close()
    gauge.close()
