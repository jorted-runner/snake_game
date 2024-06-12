import pygame as pg
import random

class Food:
    def __init__(self, screen_width, screen_height, tile_size):
        self.size = tile_size
        self.rect = pg.rect.Rect([0, 0, tile_size, tile_size])
        self.rect.center = self.get_random_position(screen_width, screen_height, tile_size)
        self.color = 'red'
        self.position = self.get_random_position(screen_width, screen_height, tile_size)

    def get_random_position(self, screen_width, screen_height, tile_size):
        x = random.randint(0, (screen_width // tile_size) - 1) * tile_size
        y = random.randint(0, (screen_height // tile_size) - 1) * tile_size
        return (x, y)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

    def update_position(self, screen_width, screen_height, tile_size):
        self.position = self.get_random_position(screen_width, screen_height, tile_size)
