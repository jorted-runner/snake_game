import random
import math
import pygame
from player import Player

class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.score = 0
        self.snakes = [
            Player([(100, 100), (100, 80), (100, 60)], 'green'),
            Player([(500, 100), (500, 80), (500, 60)], 'purple')
        ]
        self.food_size = 20
        self.food_rect = pygame.rect.Rect([0, 0, self.food_size, self.food_size])
        self.food_rect.center = self.get_random_position(600, 600, 20)
        self.food_color = 'red'
        self.food_position = self.get_random_position(600, 600, 20)

    def get_random_position(self, screen_width, screen_height, tile_size):
        x = random.randint(0 + tile_size // 2, screen_width - tile_size // 2)
        y = random.randint(0 + tile_size // 2, screen_height - tile_size // 2)
        return (x, y)

    def check_food(self, data, player):
        center_head = player.segments[0].center
        center_food = data.food_rect.center
        distance = math.sqrt((center_food[0] - center_head[0]) ** 2 + (center_food[1] - center_head[1]) ** 2)
        if distance < player.size - 3:
            player.time_step -= player.time_step * 0.0125
            player.add_segment(player.segments[-1].center)
            return True  # Return True if food is eaten
        return False

    def update_score(self):
        self.score += 1

    def update_alive(self):
        self.alive = False

    def draw_score(self, screen):
        if not pygame.font.get_init():
            pygame.font.init()
        font = pygame.font.Font(pygame.font.match_font('comicsans'), 36)
        text = font.render(f"Score {self.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def draw_food(self, screen):
        pygame.draw.rect(screen, self.food_color, self.food_rect)

    def update_position(self, screen_width, screen_height, tile_size):
        self.food_position = self.get_random_position(screen_width, screen_height, tile_size)

    def connected(self):
        if self.snakes[0].ready and self.snakes[1].ready:
            self.ready = True
            return self.ready
    
    def reset(self):
        print("Resetting game...")
        self.__init__(self.id)

    def game_over(self):
        print("Game over!")
        self.reset()
