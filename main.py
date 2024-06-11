import pygame as pg
from game_objects import Snake, Food, Portal
import sys
from random import randrange

class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 20
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.starting_pos = [[(100,100), (100,75), (100,50)], [(550,100),(550,75),(550,50)]]
        self.fps = 8
        self.range = (self.TILE_SIZE // 2, self.WINDOW_SIZE - self.TILE_SIZE // 2, self.TILE_SIZE)
        self.new_game()

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]

    def draw_grid(self):
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.WINDOW_SIZE))
                                             for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y))
                                             for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
    
    def new_game(self):
        self.fps = 8
        self.snake_1 = Snake(self, self.starting_pos[0])
        self.snake_2 = Snake(self, self.starting_pos[1])
        self.food = Food(self)
        self.portal = Portal(self)

    def update(self):
        self.snake_1.update()
        pg.display.flip()
        self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake_1.draw()
        self.portal.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake_1.control(event)
            self.portal.place(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()