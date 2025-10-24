import serial
import csv
import time
from pynput import keyboard

reading_toggle = False
end = False

#Keyboard input handler
def on_press(key):
    global reading_toggle
    global end
    if key == keyboard.Key.space:
        reading_toggle = not reading_toggle # start/stop data reading
        print("Reading start!")
    elif key == keyboard.Key.esc:
        end = True

def print_Menu():
    print("-------Menu------")
    print("1. Record data")
    print("2. Plot data")
    print("3. ")
    print("4. Record data")
    print("0. Exit program")
    print("-----------------")

# Starter lytteren
key_watcher = keyboard.Listener(on_press=on_press)
key_watcher.start()

while True:
    print_Menu()
    menu_choice = int(input("What do you want to do?\n"))
    match menu_choice:
        case 1:
            print("choice 1")
        
        case 0:
            print("Quitting program")
            break
        case _:
            print("not a choice")

    while(reading_toggle):
        print("reading data")



    