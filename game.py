import pygame

from player import Player

width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('client')


def redrawWindow(win, player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    p = Player(200, 200, 64, 64, (255,0,0))
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.update_vel(win)
        redrawWindow(win, p)

main()