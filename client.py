from network import Network
import pygame as pg

WINDOW_SIZE = 600
TILE_SIZE = 20

screen = pg.display.set_mode([WINDOW_SIZE] * 2)
clock = pg.time.Clock()
pg.display.set_caption('client')
                
def redrawWindow(screen, game):
    screen.fill('black')
    # if not(game.connected()):
    #     font = pg.font.SysFont('comicsans', 60)
    #     text = font.render('Waiting for player', 1, (255,0,0), True)
    #     screen.blit(text, (WINDOW_SIZE/2 - text.get_width()/2, WINDOW_SIZE/2 - text.get_height()/2))
    # else:
    game.draw_score(screen)
    for player in game.snakes:
        player.draw_portal(screen)
        player.draw(screen)
        time_now = pg.time.get_ticks()
        if time_now - player.time > player.time_step:
            player.time = time_now
            player.move()
        game.check_food(player)
    game.check_portal()
    game.food.draw_food(screen)
    pg.display.update()

def menu_screen():
    if not pg.font.get_init():
        pg.font.init()
    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(60)
        screen.fill('black')

        font = pg.font.SysFont('comicsans', 60)
        text = font.render('Click to Play!', 1, (255,0,0))
        screen.blit(text, (100,200))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                run = False
    main()

def main():
    run = True
    n = Network()
    data = n.getP()
    game = data[0]
    p_index = data[1]
    clock = pg.time.Clock()
    game.snakes[p_index].ready = True
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            game.snakes[p_index].control(event)
            game.snakes[p_index].place_portal(event)

        game.check_borders()
        game.check_self_eating()
        redrawWindow(screen, game)

if __name__ == "__main__":
    while True:
        menu_screen()