import serial
import time
import subprocess
import os
from shutil import copyfile

SKETCH_NAME = "passw_input_working.ino"
PASSWD_TEMPLATE = "./passwords_def_template.h"
#TODO: allow update of an existing passwd file
PASSWD_TMP_FILE = "./passwords_def.h"

def main():

    ports = find_arduino_serial_port()
    port = select_port(ports)

    use_existing_file = input("Do you want to use an existing password file? (yes/no): ").strip().lower()
    
    if use_existing_file in ('yes', 'y'):
        # Ask the user to provide the file path
        existing_file_path = input("Enter the path to the existing password file: ").strip()
        if os.path.isfile(existing_file_path):
            passwd_file = existing_file_path
        else:
            print(f"File {existing_file_path} does not exist. Exiting.")
            return
    else:

        print(f'Selected port: {port}')

        passwds = gather_passwds()

        passwd_file = create_passwd_file(passwds)
        

    # Open serial port (replace 'COM3' with your Arduino's port)
    #ser = serial.Serial("{selected_port}", 9600)
    #time.sleep(2)  # Wait for the connection to initialize
    flash_sketch(port, 'SparkFun:avr:promicro', SKETCH_NAME)
    safe_delete_passwd_file (PASSWD_TMP_FILE)

def gather_passwds():
    enter = 'PasswordElement(PASS_KEY_ENTER),'
    tab = 'PasswordElement(PASS_KEY_TAB),'
    passwds = []
    for i in range(0,3):
       cont = True
       password_def = []
       while cont:
         print(f"Enter password {i+1} (value, tab, enter, done):")
         inp = input()
         if inp == 'tab':
            password_def.append(tab)
         elif inp == 'enter':
            password_def.append(enter)
         elif inp == 'done':
            cont = False
            passwds.append(password_def)
         else:
            password_def.append(f'PasswordElement("{inp}"),')
    return passwds

def create_passwd_file(passwd):
    copyfile(PASSWD_TEMPLATE, PASSWD_TMP_FILE)

    with open(PASSWD_TMP_FILE, "r") as file:
        lines = file.readlines()
        
    with open(PASSWD_TMP_FILE, "w") as file:
        for line in lines:
            if line.startswith('//PASSWD1'):
                for e in passwd[0]:
                  file.write(f'{e}\n')
            elif line.startswith('//PASSWD2'):
                for e in passwd[1]:
                  file.write(f'{e}\n')
            elif line.startswith('//PASSWD3'):
                for e in passwd[2]:
                  file.write(f'{e}\n')
            else:
                file.write(line)
    return PASSWD_TMP_FILE

def flash_sketch(port, fqbn, sketch_path):
    try:
        # Compile the sketch
        compile_command = ["arduino-cli", "compile", "--fqbn", fqbn, sketch_path]
        subprocess.run(compile_command, check=True)

        # Upload the sketch
        upload_command = ["arduino-cli", "upload", "--port", port, "--fqbn", fqbn, sketch_path]
        subprocess.run(upload_command, check=True)
        print("Sketch uploaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def find_arduino_serial_port():
    try:
        result = subprocess.check_output(
            "ls /dev/serial/by-id/ | xargs -I {} file /dev/serial/by-id/{} | grep -o 'ttyACM[0-9]*'", 
            shell=True
        )
        ports = result.decode('utf-8').strip().split('\n')
        return ports if ports else None
    except subprocess.CalledProcessError as e:
        print(f"Could not find mcu. Error: {e}")
        exit()

def select_port(ports):
    if ports == None:
        print("No Arduino found")
        exit()
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

def safe_delete_passwd_file(filepath):
    user_response = input(f"Do you want to delete the file {filepath}? (yes/no): ").strip().lower()
    if user_response in ('yes', 'y'):
        try:
            os.remove(filepath)
            print(f"Successfully deleted {filepath}")
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")
    else:
        print(f"File {filepath} was not deleted.")

main()
