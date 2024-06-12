import pygame as pg
from game_snake import Snake
from game_food import Food
from game_portals import Portal
import sys
from random import randrange

class Game:
    def __init__(self):
        pg.init()

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]
    
    def new_game(self):
        self.fps = 8
        # self.snake_1 = Snake(self, self.starting_pos[0], 'green')
        # self.snake_2 = Snake(self, self.starting_pos[1], 'purple')
        self.food = Food(self)
        self.portal = Portal(self)

    def update(self):
        # self.snake_1.update()
        # self.snake_2.update()
        pg.display.flip()

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        # self.snake_1.draw()
        # self.snake_2.draw()
        self.portal.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # self.snake_1.control(event)
            # self.snake_2.control(event)
            self.portal.place(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()