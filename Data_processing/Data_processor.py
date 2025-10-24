import serial
import csv
import time
import webbrowser
from pynput import keyboard
from pathlib import Path
import serial.tools.list_ports

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

#Menu for some graphic interface for user
def print_Menu():
    while True:
        print("----Main Menu-----")
        print("|1. Record data  |")
        print("|2. Plot data    |")
        print("|3.              |")
        print("|4.              |")
        print("|5.              |")
        print("|6.              |")
        print("|7.              |")
        print("|8. Settings     |")
        print("|9. Go to github |")
        print("|0. Exit program |")
        print("-----------------")
        menu_choice = int(input("What do you want to do?\n"))
        match menu_choice:
            case 1:
                data_record(input("What will your file be called?\n"))
            
            case 8:
                settings_menu()
            case 9:
                webbrowser.open("https://github.com/ElektroMannen/Colourophone-challenge")
            case 0:
                print("Quitting program")
                break
            case _:
                print("not a choice")



def settings_menu():
    while True:
        print("--------Settings-------")
        print("|1. Change Serial Port|")
        print("|2. Plot data         |")
        print("|0. Back to main menu |")
        print("-----------------------")
        choice = int(input("What would you like to do?\n"))
        match choice:
            case 1:
                print("Change serial port")
            case 2:
                print("Something")
            case 0:
                break


    
#Manages filecreation and data reading/writing to file
def data_record(filename):
    global end
    #Checking if file exists and creates file if not
    folder = Path("Data")
    folder.mkdir(exist_ok=True)
    filepath = Path(f"{folder}/{filename}.csv")
    if not filepath.exists():
        print(f"creating {filename}.csv")
        with open(filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Value"])
        print(f"File created at {filepath}")
    else:
        print("File allready exists")

    #Data recording can begin
    print("\nTo start and stop data recording use spacebar \nUse Escape key to end data recording")

    
    key_watcher.start()
    if(end):
        key_watcher.stop()



#Starts program
print_Menu()


    