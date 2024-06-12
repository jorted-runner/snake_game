import pygame
from network import Network
import math
from COPY_game import Game
from game_snake import Snake

WINDOW_SIZE = 800
TILE_SIZE = 20

screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
clock = pygame.time.Clock()
pygame.display.set_caption('client')

def check_borders(player):
        if player.segments[0].left < 0 or player.segments[0].right > 800:
            pygame.quit()
        if player.segments[0].top < 0 or player.segments[0].bottom > 800:
            pygame.quit()

def check_food(food, player, FPS):
    center_head = player.segments[0].center
    center_food = food.rect.center
    distance = math.sqrt((center_food[0] - center_head[0]) **2 + (center_food[1] - center_head[1]) **2)
    if distance < player.size - 3:
        # This needs to be done more dynamically
        food.rect.center = food.get_random_position(800, 800, 20)
        FPS *= 1.01
        player.add_segment(player.segments[-1].center)

def check_self_eating(self):
    if len(self.segments) != len(set(segment.center for segment in self.segments)):
        self.game.new_game()

def check_portal(self):
    if self.game.portal.circles['orange']['pos'] and self.game.portal.circles['blue']['pos']:
        center_head = self.segments[0].center
        orange_portal = self.game.portal.circles['orange']['pos']
        orange_distance = math.sqrt((orange_portal[0] - center_head[0]) **2 + (orange_portal[1] - center_head[1]) **2)
        blue_portal = self.game.portal.circles['blue']['pos']
        blue_distance = math.sqrt((blue_portal[0] - center_head[0]) **2 + (blue_portal[1] - center_head[1]) **2)
        if orange_distance < self.size - 5:
            self.segments[0].center = blue_portal
        if blue_distance < self.size -5:
            self.segments[0].center = orange_portal


def redrawWindow(screen, p, food, FPS):
    screen.fill('black')
    draw_grid()
    for player in p:
        player.draw(screen)
        player.move()
        check_borders(player)
        check_food(food, player, FPS)
    food.draw(screen)
    pygame.display.update()

def draw_grid():
    [pygame.draw.line(screen, [50] * 3, (x, 0), (x, WINDOW_SIZE)) for x in range(0, WINDOW_SIZE, TILE_SIZE)]
    [pygame.draw.line(screen, [50] * 3, (0, y), (WINDOW_SIZE, y)) for y in range(0, WINDOW_SIZE, TILE_SIZE)]

def main():
    run = True
    n = Network()
    data = n.getP()
    p = data[0]
    food = data[1]
    FPS = data[2]
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FPS)
        try:
            data = n.send((p, food, FPS))
            p = data[0]
            food = data[1]
            FPS = data[2]

        except Exception as e:
            run = False
            print(f"Couldn't get game: {e}")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            for player in p:
                player.control(event)

        redrawWindow(screen, p, food, FPS)

main()
