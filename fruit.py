import pygame
import random

class Fruit():
    def __init__(self, width, height, color, win):
        self.width = width
        self.height = height
        self.color = color
        self.x = self.set_x(win)
        self.y = self.set_y(win)
        self.rect = (self.x, self.y, self.width, self.height)


    def set_x(self, win):
        return random.randrange(self.width, win.get_width())

    def set_y(self, win):
        return random.randrange(self.height, win.get_height())

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)