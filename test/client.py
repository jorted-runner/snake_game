# client.py

from network import Network
from player import Player
import pygame as pg

WINDOW_SIZE = 600
TILE_SIZE = 20

screen = pg.display.set_mode([WINDOW_SIZE] * 2)
clock = pg.time.Clock()
pg.display.set_caption('client')
                
def redrawWindow(screen, game, player, n):
    screen.fill('black')
    game.update(screen)
    game.check_food(player)
    n.send((game, player))
    pg.display.update()

def menu_screen(n):
    if not pg.font.get_init():
        pg.font.init()
    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(60)
        screen.fill('black')

        font = pg.font.SysFont('comicsans', 60)
        text = font.render('Click to Play!', 1, (255, 0, 0))
        screen.blit(text, (100, 200))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                run = False
    main(n)

def main(n):
    run = True
    game_data = n.getP()
    print(f'1st Receive: {game_data[0]}, {game_data[1]}')

    game = game_data[0]  # Extract the game object
    p_index = game_data[1]  # Extract the player index
    if p_index > 0:
        player = Player([(100, 100), (100, 80), (100, 60)], 'green', p_index)
    else:
        player = Player([(500, 100), (500, 80), (500, 60)], 'purple', p_index)
    clock = pg.time.Clock()
    print(f'Sending: {game}, {player}')
    n.send((game, player))  # Notify the server that this player is ready
    while run:
        updated_data = n.getP()
        print(f'2nd Receive: {updated_data} | {updated_data[0]}, {updated_data[1]}')
        run = False



if __name__ == "__main__":
    n = Network()
    menu_screen(n)
