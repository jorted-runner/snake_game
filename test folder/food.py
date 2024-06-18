import pygame
from util import Util

class Food:
    def __init__(self, screen_width, screen_height, tile_size):
        self.size = 20
        self.rect = pygame.rect.Rect([0, 0, self.size, self.size])
        self.rect.center = self.get_random_position(600, 600, 20)
        self.color = 'red'
        self.position = self.get_random_position(600, 600, 20)
        self.utils = Util(screen_width, screen_height, tile_size)
    
    def draw_food(self, screen):
        pygame.draw.rect(screen, self.food_color, self.food_rect)

    def update_position(self):
        self.food_position = self.utils.get_random_position()