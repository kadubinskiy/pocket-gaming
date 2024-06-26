
        # print("\033[H\033[J", end="")

import os
import time
from pynput import keyboard
import threading
import sys
import subprocess

class Screen():
    def __init__(self):
        self.manager = Menu()
        self.state = 0
        self.chcl = '\033[43m'
        self.defcl = '\033[0m'
        self.pghist = []

    def get_state(self):
        return self.state

    def plot(self):
        for count in range(len(self.manager.get_options())):
            if count == self.manager.get_choice():
                print(self.chcl+self.manager.get_options()[count]+self.defcl)
            else:
                print(self.manager.get_options()[count])

    def cycle_choice(self, direction):
        if direction == keyboard.Key.up:
            self.manager.choice = (self.manager.choice - 1) % len(self.manager.options)
        elif direction == keyboard.Key.down:
            self.manager.choice = (self.manager.choice + 1) % len(self.manager.options)
        elif direction == keyboard.Key.right or direction == keyboard.Key.enter:
            self.set_manager_options()
        elif direction == keyboard.Key.left or direction == keyboard.Key.backspace:
            self.set_manager_options(self.pghist.pop())
            
    def set_manager_options(self, option=False):
        if option:
            self.manager.set_options(option)
        else:
            self.pghist.append(self.manager.get_options())
            if self.manager.options[self.manager.choice] == 'Choose Game':
                self.state = 1
                self.manager.set_options(self.parse_games())
            elif self.manager.options[self.manager.choice] == 'Settings':
                self.state = 2
                self.manager.set_options(self.parse_games())
            elif self.manager.options[self.manager.choice] == 'Exit':
                sys.exit()
            elif self.state == 1 and self.manager.options[self.manager.choice] == 'snake':
                self.state = 555
                subprocess.run(['python', os.path.dirname(os.path.abspath(__file__)) + '/library/snake/snake.py'])
                self.state = 1

    def parse_games(self):
        home_dir = os.path.dirname(os.path.abspath(__file__))
        library = os.listdir(home_dir + '/library')
        return library


class Menu():
    def __init__(self):
        self.options = ['Choose Game', 'Settings', 'Exit']
        self.choice = 0

    def set_options(self, options):
        self.options = options

    def set_choice(self, choice):
        self.choice = choice

    def get_options(self):
        return self.options
    
    def get_choice(self):
        return self.choice


manager = Screen()

def update_screen():
    while True:
        if manager.state == 0:
            print("\033[H\033[J", end="")
            manager.plot()
            time.sleep(.1)
        else:
            pass



if __name__ == "__main__":
    listener = keyboard.Listener(on_press=manager.cycle_choice)
    listener.start()

    main_thread = threading.Thread(target=update_screen)
    main_thread.start()

    main_thread.join()
    listener.join()