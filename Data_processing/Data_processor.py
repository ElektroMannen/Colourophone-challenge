import serial
import csv
import time
import webbrowser
from pynput import keyboard
from pathlib import Path
import serial.tools.list_ports


serial_port = ""
serial_baudrate = 9600
reading_toggle = False
end = False

#Keyboard input handler
def on_press(key):
    global reading_toggle
    global end
    if key == keyboard.Key.space:
        reading_toggle = not reading_toggle # start/stop data reading
        if(reading_toggle):
            print("Reading start!")
        else:
            print("Reading stop!")
    elif key == keyboard.Key.esc:
        end = True

#Init keyboard listner
key_watcher = keyboard.Listener(on_press=on_press)

def list_data_files():
    folder = Path("Data")
    print("All data files are shown below:")
    for file in folder.glob("*.csv"):
        print(file.name)

#Manages filecreation and data reading/writing to file
def data_record(filename):
    global end, serial_port,serial_baudrate
    #Checking if file exists and creates file if not
    folder = Path("Data")
    folder.mkdir(exist_ok=True)
    filepath = Path(f"{folder}/{filename}.csv")
    if not filepath.exists():
        print(f"Creating {filepath}")
        with open(filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Temperature"])  # Write header once
    else:
        print(f"Appending data to existing file: {filepath}")

    #Data recording can begin
    ser = serial.Serial(serial_port, serial_baudrate)
    print("\nTo start and stop data recording use spacebar \nUse Escape key to end data recording")
    key_watcher.start()
     # Open file in append mode
    with open(filepath, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        while True:
            if ((ser.in_waiting > 0) and (reading_toggle)):  # Only log when active
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                csv_writer.writerow([time.strftime("%H:%M:%S"), line])
                csvfile.flush()
            if (end):
                print("Stopping recording...")
                ser.close()
                key_watcher.stop()
                break

#Menu for some graphic interface for user
def print_Menu():
    while True:
        print("-----Main Menu-----")
        print("|1. Record data    |")
        print("|2. Plot data      |")
        print("|3.                |")
        print("|4.                |")
        print("|5.                |")
        print("|6.                |")
        print("|7. List data files|")
        print("|8. Settings       |")
        print("|9. Go to github   |")
        print("|0. Exit program   |")
        print("-------------------")
        menu_choice = int(input("What do you want to do?\n"))
        match menu_choice:
            case 1:
                data_record(input("What will your file be called?\n"))
            case 7:
                list_data_files()
            case 8:
                settings_menu()
            case 9:
                webbrowser.open("https://github.com/ElektroMannen/Colourophone-challenge")
            case 0:
                print("Quitting program")
                break
            case _:
                pass


#Menu for handling serial changes
def settings_menu():
    global serial_port, serial_baudrate
    while True:
        print("--------Settings-------")
        print("|1. Change Serial Port|")
        print("|2. Change Baud rate  |")
        print("|3. Show Serial info  |")
        print("|0. Back to main menu |")
        print("-----------------------")
        choice = int(input("What would you like to do?\n"))
        match choice:
            case 1: #Changing seral port
                print("Available serial ports:")
                ports = serial.tools.list_ports.comports()
                for i, port in enumerate(ports, start=1):
                    if((port.description != "n/a") and (port.hwid != "n/a")):
                        print(f"{i}:\nDevice: {port.device}")
                        print(f"Description: {port.description}")
                        print(f"Hardware ID: {port.hwid}")
                        print("-" * 20)

                port_num = int(input("Which device is your device?\n"))
                serial_port = ports[port_num-1].device
                print(f"New device is {serial_port}")

            case 2:#Changing baudrate
                print("-" * 20)
                serial_baudrate = int(input("Please write the new baudrate\n(Standards are 9600 or 115200)\n"))
                print(f"New baud rate is {serial_baudrate}")
            case 3:
                print("-" * 20)
                print("Serial info:")
                print(f"Serial port: {serial_port}\nBaudrate: {serial_baudrate}")
            case 0:#Back to main menu
                break
            case _: #Not a choice
                pass
            


#Starts program
print_Menu()