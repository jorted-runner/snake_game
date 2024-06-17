import pygame as pg
from network import Network
import math
import time

COOL_DOWN_PERIOD = 1.0

WINDOW_SIZE = 600
TILE_SIZE = 20

screen = pg.display.set_mode([WINDOW_SIZE] * 2)
clock = pg.time.Clock()
pg.display.set_caption('client')

def check_borders(player):
    if player.segments[0].left < 0 or player.segments[0].right > WINDOW_SIZE:
        return True
    if player.segments[0].top < 0 or player.segments[0].bottom > WINDOW_SIZE:
        return True

def check_self_eating(players):
    p1_head_pos = players[0].segments[0].center
    p2_head_pos = players[1].segments[0].center
    for player in players:
        for segment in player.segments[1:]:
            if segment.center == p1_head_pos or segment.center == p2_head_pos or p2_head_pos == p1_head_pos:
                return True
                
def check_portal(players):
    current_time = time.time()
    if players[0].portal['pos'] and players[1].portal['pos']:
        for player in players:
            center_head = player.segments[0].center
            portal_0 = players[0].portal['pos']
            portal_1 = players[1].portal['pos']
            
            portal_0_dist = math.sqrt((portal_0[0] - center_head[0]) ** 2 + (portal_0[1] - center_head[1]) ** 2)
            portal_1_dist = math.sqrt((portal_1[0] - center_head[0]) ** 2 + (portal_1[1] - center_head[1]) ** 2)
            
            if portal_0_dist < player.size - 3 and (not hasattr(player, 'last_teleport_time') or current_time - player.last_teleport_time >= COOL_DOWN_PERIOD):
                player.segments[0].center = portal_1  # Teleport to the other portal
                player.last_teleport_time = current_time  # Record the current time as the last teleport time
            elif portal_1_dist < player.size - 3 and (not hasattr(player, 'last_teleport_time') or current_time - player.last_teleport_time >= COOL_DOWN_PERIOD):
                player.segments[0].center = portal_0  # Teleport to the other portal
                player.last_teleport_time = current_time # Record the current time as the last teleport time

def redrawWindow(screen, data):
    screen.fill('black')
    if not(data.connected()):
        font = pg.font.SysFont('comicsans', 80)
        text = font.render('Waiting for player', 1, (255,0,0), True)
        screen.blit(text, (WINDOW_SIZE/2 - text.get_width()/2, WINDOW_SIZE/2 - text.get_height()/2))
    data.draw_score(screen)
    for player in data.snakes:
        player.draw_portal(screen)
        player.draw(screen)
        time_now = pg.time.get_ticks()
        if time_now - player.time > player.time_step:
            player.time = time_now
            player.move()
        if data.check_food(data, player):
            player.send_food_update = True  # Mark food update to be sent to server
    check_portal(data.snakes)
    data.draw_food(screen)
    pg.display.update()

def menu_screen():
    if not pg.font.get_init():
        pg.font.init()
    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(60)
        screen.fill((128,128,128))

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
    print(data)
    game = data[0]
    p_index = data[1]
    clock = pg.time.Clock()
    game.snakes[p_index].ready = True
    while run:
        clock.tick(60)
        try:
            data = n.send((data))

        except Exception as e:
            run = False
            print(f"Couldn't get game: {e}")
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            for player in data.snakes:
                if player.alive:
                    player.control(event)
                    player.place_portal(event)

        for player in data.snakes:
            if player.alive:
                if check_borders(player):
                    player.alive = False

        if check_self_eating(game.snakes):
            for player in game.snakes:
                player.alive = False

        redrawWindow(screen, data)

if __name__ == "__main__":
    while True:
        menu_screen()
