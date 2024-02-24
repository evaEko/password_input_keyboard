import serial
import time
import subprocess

SKETCH_NAME = "passw_input_working.ino"

def main():
    ports = find_arduino_serial_port()
    if ports:
        for port in ports:
            print(f"Arduino found at: {port}")
    else:
        print("No Arduino found")
        exit()
    
    citrix_value = input("Enter the new CITRIX password: ")
    win_value = input("Enter the new WIN password: ")

    ports = find_arduino_serial_port()
    if ports:
        if len(ports) > 1:
            selected_port = select_port(ports)
            print(f"{selected_port}")
            print(f"Selected port: {selected_port}")
        elif len(ports) == 1:
            selected_port = ports[0]
            print(f"Selected port out of one: {selected_port}")
        else:
            print(f"could not select port")
    else:
        print("No ports with Arduino detected. Exiting.")
        exit()

    print(f"starting serial on {selected_port}")
    # Open serial port (replace 'COM3' with your Arduino's port)
    ser = serial.Serial("/dev/{selected_port}", 9600)
    time.sleep(2)  # Wait for the connection to initialize

    if citrix_value:
        ser.write(f'UPDATE CITRIX {citrix_value}\n'.encode())
    if win_value:
        ser.write(f'UPDATE WIN {win_value}\n'.encode())
    ser.close()
    print("Closing Serial")
    print("Updating Sketch")

    update_sketch(citrix_value, win_value)

def update_sketch(new_citrix, new_win):
    with open(SKETCH_NAME, "r") as file:
        lines = file.readlines()

    with open(SKETCH_NAME, "w") as file:
        for line in lines:
            if new_citrix and line.startswith("String CITRIX="):
                file.write(f'String CITRIX="{new_citrix}";\n')
            elif new_win and line.startswith("String WIN="):
                file.write(f'String WIN="{new_win}";\n')
            else:
                file.write(line)

def find_arduino_serial_port():
    try:
        result = subprocess.check_output(
            "ls /dev/serial/by-id/ | xargs -I {} file /dev/serial/by-id/{} | grep -o 'ttyACM[0-9]*'", 
            shell=True
        )
        ports = result.decode('utf-8').strip().split('\n')
        return ports if ports else None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def select_port(ports):
    print("Available Ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port}")

    while True:
        try:
            choice = int(input("Select the port number (e.g., 0, 1, ...): "))
            if 0 <= choice < len(ports):
                return f"/dev/{ports[choice]}"
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

main()
