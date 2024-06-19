import math
import pygame
import time
from player import Player
from food import Food

class Game:
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.snakes = [
            Player([(100, 100), (100, 80), (100, 60)], 'green'),
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
        self.cool_down_period = 1.0

    def check_food(self, player):
        current_time = time.time()
        center_head = player.segments[0].center
        center_food = self.food.rect.center
        distance = math.sqrt((center_food[0] - center_head[0]) ** 2 + (center_food[1] - center_head[1]) ** 2)
        if distance < player.size - 3 and (not hasattr(player, 'last_teleport_time') or current_time - player.last_teleport_time >= self.cool_down_period):
            self.food.update_position()
            player.last_teleport_time = current_time
            player.time_step -= player.time_step * 0.0125
            player.add_segment(player.segments[-1].center)
            self.update_score()

    def check_portal(self):
        current_time = time.time()
        if self.snakes[0].portal['pos'] and self.snakes[1].portal['pos']:
            for player in self.snakes:
                center_head = player.segments[0].center
                portal_0 = self.snakes[0].portal['pos']
                portal_1 = self.snakes[1].portal['pos']

                portal_0_dist = math.sqrt((portal_0[0] - center_head[0]) ** 2 + (portal_0[1] - center_head[1]) ** 2)
                portal_1_dist = math.sqrt((portal_1[0] - center_head[0]) ** 2 + (portal_1[1] - center_head[1]) ** 2)

                if portal_0_dist < player.size - 3 and (not hasattr(player, 'last_teleport_time') or current_time - player.last_teleport_time >= self.cool_down_period):
                    player.segments[0].center = portal_1  # Teleport to the other portal
                    player.last_teleport_time = current_time  # Record the current time as the last teleport time
                elif portal_1_dist < player.size - 3 and (not hasattr(player, 'last_teleport_time') or current_time - player.last_teleport_time >= self.cool_down_period):
                    player.segments[0].center = portal_0  # Teleport to the other portal
                    player.last_teleport_time = current_time # Record the current time as the last teleport time

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
        return self.snakes[0].ready and self.snakes[1].ready

    def check_borders(self):
        # Checks if players head is hitting either side of the window then either top or bottom
        for snake in self.snakes:
            if (snake.segments[0].left < 0 or snake.segments[0].right > self.win_width) or (snake.segments[0].top < 0 or snake.segments[0].bottom > self.win_width):
                self.game_over()

    def check_self_eating(self):
        p1_head_pos = self.snakes[0].segments[0].center
        p2_head_pos = self.snakes[1].segments[0].center
        for snake in self.snakes:
            for segment in snake.segments[1:]:
                if segment.center == p1_head_pos or segment.center == p2_head_pos or p2_head_pos == p1_head_pos:
                    self.game_over()

    def mark_ready(self, p_index):
        print(p_index)
        self.snakes[p_index].mark_ready()

    def reset(self):
        print("Resetting game...")
        self.__init__(self.id)
        for snake in self.snakes:
            snake.ready = False

    def game_over(self):
        print("Game over!")
        self.reset()
