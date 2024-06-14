from player import Player
import pygame
import random
class Game:
    def __init__(self, id) -> None:
        self.id = id
        self.score = 0
        self.snakes = [Player([(100, 100), (100, 75), (100, 50)], 'green'), Player([(500, 100), (500, 75), (500, 50)], 'purple')]
        self.food_size = 20
        self.food_rect = pygame.rect.Rect([0, 0, self.food_size, self.food_size])
        self.food_rect.center = self.get_random_position(600, 600, 20)
        self.food_color = 'red'
        self.food_position = self.get_random_position(600, 600, 20)

    def get_random_position(self, screen_width, screen_height, tile_size):
        x = random.randint(0+tile_size/2, screen_width - tile_size/2)
        y = random.randint(0+tile_size/2, screen_width - tile_size/2)
        return (x, y)

    def draw_food(self, screen):
        pygame.draw.rect(screen, self.food_color, self.food_rect)

    def update_position(self, screen_width, screen_height, tile_size):
        self.food_position = self.get_random_position(screen_width, screen_height, tile_size)

# These two methods still need to be implemented
    def reset(self):
        self.__init__()

    def game_over(self):
        self.alive = False
        self.reset()