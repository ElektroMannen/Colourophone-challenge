import serial
import csv
import time
import webbrowser
from pynput import keyboard
from pathlib import Path

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

def print_Menu():
    print("-------Menu------")
    print("|1. Record data  |")
    print("|2. Plot data    |")
    print("|3.              |")
    print("|9. Go to github |")
    print("|0. Exit program |")
    print("-----------------")

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



while True:
    print_Menu()
    menu_choice = int(input("What do you want to do?\n"))
    match menu_choice:
        case 1:
            data_record(input("What will your file be called?\n"))

        case 9:
            webbrowser.open("https://github.com/ElektroMannen/Colourophone-challenge")
        case 0:
            print("Quitting program")
            break
        case _:
            print("not a choice")

    while(reading_toggle):
        print("reading data")



    