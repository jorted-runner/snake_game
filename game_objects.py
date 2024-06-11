import pygame as pg
from random import randrange

class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        self.range = (self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)
        self.rect.center = self.get_random_position()
        self.length = 1
        self.segments = []
        self.direction = 'DOWN'
        self.speed = 1

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.direction = 'UP'
            if event.key == pg.K_DOWN:
                self.direction = 'DOWN'
            if event.key == pg.K_LEFT:
                self.direction = 'LEFT'
            if event.key == pg.K_RIGHT:
                self.direction = 'RIGHT'
    
    def move(self):
        print(self.rect.centerx, self.rect.centery)
        if self.direction == 'RIGHT':
            self.rect.centerx = self.rect.centerx + abs(self.speed)
        if self.direction == 'LEFT':
            self.rect.centerx = self.rect.centerx + (abs(self.speed) * -1)
        if self.direction == 'UP':
            self.rect.centery = self.rect.centery + (abs(self.speed) * -1)
        if self.direction == 'DOWN':
            self.rect.centery = self.rect.centery + (abs(self.speed))

    def update(self):
        self.move()

    def draw(self):
        pg.draw.rect(self.game.screen, 'green', self.rect)


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)