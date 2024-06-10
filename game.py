import pygame

from player import Player
from fruit import Fruit

width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('client')


def redrawWindow(win, player, fruit):
    win.fill((255,255,255))
    player.draw(win)
    fruit.draw(win)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    p = Player(100, 100, 40, 40, (255,0,0))
    fruit = Fruit(30, 30, (0,255,0), win)
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.update_vel(win)
        p.check_col_fruit(fruit)
        redrawWindow(win, p, fruit)

main()