# ## Imports

# from curses import wrapper
from random import randint, choice
import time

import threading
from pynput import keyboard


# ## Classes

class GameManager():
    def __init__(self):
        self.map = False
        self.snake = False
        self.apple = False

    def get_gamefield(self):
        return self.map.get_grid()
    
    def initialise(self):
        size = int(input("Input Preferred Size: "))
        self.map = Map(size)
        self.map.create_grid()
        self.snake = Snake(self.map)
        self.apple = Apple(self.map)

        if self.apple:
            self.apple.generate_apple_coordinates(self.map)

        self.draw_objects()
    
    def re_initialise(self):
        self.map.create_grid()

        if self.map.get_grid():
            if not self.apple:
                self.reset_apple()
            # self.map.draw_snake(self.snake)
            # self.map.draw_apple(self.apple)

    def draw_objects(self):
        self.map.draw_snake(self.snake)
        self.map.draw_apple(self.apple)

    def step(self):
        if self.map and self.snake and self.apple:
            if self.snake.get_next_point() != self.apple.get_coords():
                self.re_initialise()
                self.snake.crawl()
                self.draw_objects()
            elif self.snake.get_next_point() == self.apple.get_coords():
                self.reset_apple()
                self.re_initialise()
                self.snake.evolve()
                self.draw_objects()

    def reset_apple(self):
        self.apple.generate_apple_coordinates(self.map)

    def snake_direction(self, direction):
        if direction in [keyboard.Key.up, keyboard.Key.right, keyboard.Key.down, keyboard.Key.left]:
            self.snake.set_head_points(direction)


class Map():
    def __init__(self, size = 16):
        self.size = size
        self.apple = False
        self.grid = []

    def set_apple(self, apple):
        self.apple = apple

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def get_apple(self):
        return self.apple


    ### Functionality
    
    def create_grid(self):
        self.grid = [[' ' for count in range(self.size)] for _ in range(self.size)]

    def draw_snake(self, snake):
        snake_coords = snake.get_body_coords()
        for coords in snake_coords:
            
            for coord in coords:
                if coord < 0 or coord > self.size:
                    return 'Game Over'
                    
            self.grid[coords[0]][coords[1]] = '*'

    def draw_apple(self, apple):
        y, x = apple.get_coords()
        if not y:
            return 'Game Won!'
        self.grid[y][x] = '*'


class Snake():
    def __init__(self, map):
        self.init_y = int(len(map.get_grid())/2)
        self.init_x = self.init_y
        self.length = 2
        self.head_points = 'up'
        self.body_coords = [[self.init_y+1, self.init_x], [self.init_y, self.init_x]]

    def set_length(self, length):
        self.length = length

    def set_body_coords(self, coords):
        self.body_coords = coords

    def set_head_points(self, direction):
        if direction == keyboard.Key.up:
            direction = 'up'
        elif direction == keyboard.Key.right:
            direction = 'right'
        elif direction == keyboard.Key.down:
            direction = 'down'
        elif direction == keyboard.Key.left:
            direction = 'left'

        if direction:
            self.head_points = direction

    def get_length(self):
        return self.length

    def get_body_coords(self):
        return self.body_coords

    def get_head_points(self):
        return self.head_points

    def get_next_point(self):
        if self.head_points == 'up':
            return [self.body_coords[-1][0]-1, self.body_coords[-1][1]]
        elif self.head_points == 'right':
            return [self.body_coords[-1][0], self.body_coords[-1][1]+1]
        elif self.head_points == 'down':
            return [self.body_coords[-1][0]+1, self.body_coords[-1][1]]
        elif self.head_points == 'left':
            return [self.body_coords[-1][0], self.body_coords[-1][1]-1]


    ### Functionality

    def evolve(self):
        self.length += 1
        self.crawl()

    def crawl(self):
        if self.length == len(self.body_coords):
            self.body_coords.pop(0)

        self.body_coords.append(self.get_next_point())


class Apple():
    def __init__(self, map):
        self.coords = []
        self.map = map

    def set_coords(self, coords):
        self.coords = coords

    def get_coords(self):
        return self.coords


    ### Functionality
    
    def generate_apple_coordinates(self, map):
        ### Setup
        map = self.map.get_grid()
        size = len(map)
        row_numbers = []
        
        for rows in range(size):
            row_numbers.append(rows)
        
        ### Execution
        for attempts in range(size):
            y = choice(row_numbers)
            available_slots = []
            
            for x in range(len(map[y])):
                if map[y][x] == ' ':
                    available_slots.append(x)
    
            if len(available_slots) != 0:
                break
            else:
                row_numbers.pop(row_numbers.index(y))
                
        if len(available_slots) == 0:
            return False, 0
            
        x = available_slots[randint(0, len(available_slots)-1)]
        self.coords = [y, x]


# ### Refreshrate function

def update_game():
    while True:
        print("\033[H\033[J", end="")
        # clear_output(wait=True)
        for row in game.get_gamefield():
            print(row)
        time.sleep(1)
        game.step()




# ## Application

if __name__ == "__main__":
    game = GameManager()
    game.initialise()

    listener = keyboard.Listener(on_press=game.snake_direction)
    listener.start()

    game_thread = threading.Thread(target=update_game)
    game_thread.start()

    game_thread.join()
    listener.join()