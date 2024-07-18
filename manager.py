
import os
import time
from pynput import keyboard
import threading
import sys
import subprocess
import ast

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
            if type(self.manager.get_options()[count]) == str:
                if count == self.manager.get_choice():
                    print(self.chcl + self.manager.get_options()[count] + self.defcl)
                else:
                    print(self.manager.get_options()[count])
            elif type(self.manager.get_options()[count]) == list:
                if count == self.manager.get_choice():
                    row = ''
                    for cols in self.manager.get_options()[count]:
                        row += self.chcl + str(cols) + '   '
                    row = row[:-3]
                    row += self.defcl
                    print(row)
                else:
                    row = ''
                    for cols in self.manager.get_options()[count]:
                        row += str(cols) + '    '
                        row = row[:-3]
                    print(row)

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
            elif self.state == 1:
                choice = self.manager.options[self.manager.choice]
                self.state = 555
                subprocess.run(['python', os.path.dirname(os.path.abspath(__file__)) + f'/library/{choice}/{choice}.py'])
                self.state = 1
            elif self.state == 2:
                choice = self.manager.options[self.manager.choice]
                self.state = 20
                settings, values, descriptions = self.parse_config(choice)
                all_options, option = [], []
                for count in range(len(settings)):
                    option.append(settings[count])
                    option.append(values[count])
                    option.append(descriptions[count])
                    all_options.append(option)
                self.manager.set_options(all_options)
            # elif self.state == 20:

    def parse_games(self):
        home_dir = os.path.dirname(os.path.abspath(__file__))
        library = os.listdir(home_dir + '/library')
        return library
    
    def parse_config(self, game):
        path = os.path.dirname(os.path.abspath(__file__)) + f'/library/{game}/config.txt'
        with open(path, 'r') as file:
            contents = file.read()
            config = ast.literal_eval(contents)
        settings, values, descriptions = list(config.keys()), [], []
        for setting in settings:
            values.append(config[setting]['value'])
            descriptions.append(config[setting]['description'])
        return settings, values, descriptions


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
        if manager.state not in [555]:
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