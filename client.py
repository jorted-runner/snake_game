import pygame
from network import Network
from COPY_game import Game
from game_snake import Snake

WINDOW_SIZE = 800
TILE_SIZE = 20
screen = pygame.display.set_mode([WINDOW_SIZE] * 2)
clock = pygame.time.Clock()
starting_pos = [[(100,100), (100,75), (100,50)], [(550,100),(550,75),(550,50)]]
fps = 8
grid_range = (TILE_SIZE // 2, WINDOW_SIZE - TILE_SIZE // 2, TILE_SIZE)  # Renamed 'range' to 'grid_range'
pygame.display.set_caption('client')

clientNumber = 0

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

def redrawWindow(screen):
    screen.fill('black')
    draw_grid()
    pygame.display.update()

def draw_grid():
    [pygame.draw.line(screen, [50] * 3, (x, 0), (x, WINDOW_SIZE)) for x in range(0, WINDOW_SIZE, TILE_SIZE)]
    [pygame.draw.line(screen, [50] * 3, (0, y), (WINDOW_SIZE, y)) for y in range(0, WINDOW_SIZE, TILE_SIZE)]


def main():
    redrawWindow(screen)
    run = True
    n = Network()
    # p = n.getP()
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        # p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

main()
