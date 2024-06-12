import pygame as pg

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        self.rect.center = self.game.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)