import random
import math
import pygame
from player import Player
from food import Food

class Game:
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.snakes = [
            # Player([(100, 100), (100, 80), (100, 60)], 'green'),
            Player([(500, 100), (500, 80), (500, 60)], 'purple')
        ]
        self.win_width = 600
        self.win_height = 600
        self.tile_size = 20
        self.food = Food(
            self.win_width,
            self.win_height,
            self.tile_size
        )
        
    def check_food(self, player):
        center_head = player.segments[0].center
        center_food = self.food_rect.center
        distance = math.sqrt((center_food[0] - center_head[0]) ** 2 + (center_food[1] - center_head[1]) ** 2)
        if distance < player.size - 3:
            player.time_step -= player.time_step * 0.0125
            player.add_segment(player.segments[-1].center)
            self.update_score()
            self.food.update_position()

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

    def connected(self):
        # if self.snakes[0].ready and self.snakes[1].ready:
        #     return True
        return True
        
    
    def reset(self):
        print("Resetting game...")
        self.__init__(self.id)
        for snake in self.snakes:
            snake.ready = False

    def game_over(self):
        print("Game over!")
        self.reset()
