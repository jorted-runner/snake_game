import pygame
from util import Util

class Food:
    def __init__(self, screen_width, screen_height, tile_size):
        self.utils = Util(screen_width, screen_height, tile_size)
        self.size = 20
        self.rect = pygame.rect.Rect([0, 0, self.size, self.size])
        self.rect.center = self.utils.get_random_position()
        self.color = 'red'
        self.position = self.utils.get_random_position()
    
    def draw_food(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update_position(self):
        self.rect.center = self.utils.get_random_position()