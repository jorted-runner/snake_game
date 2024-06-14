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
        player.game_over()
    if player.segments[0].top < 0 or player.segments[0].bottom > WINDOW_SIZE:
        player.game_over()

def check_food(data, player):
    center_head = player.segments[0].center
    center_food = data.food_rect.center
    distance = math.sqrt((center_food[0] - center_head[0]) ** 2 + (center_food[1] - center_head[1]) ** 2)
    if distance < player.size - 3:
        player.time_step -= player.time_step * .0125
        player.add_segment(player.segments[-1].center)
        return True  # Return True if food is eaten
    return False

def check_self_eating(player):
    head_pos = player.segments[0].center
    for segment in player.segments[1:]:
        if segment.center == head_pos:
            player.game_over()

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

def redrawWindow(screen, p, data):
    screen.fill('black')
    draw_grid()
    time_now = pg.time.get_ticks()
    if time_now - p[0].time > p[0].time_step:
        p[0].time = time_now
        p[0].move()
    for player in p:
        player.draw_portal(screen)
        player.draw(screen)
        # time_now = pg.time.get_ticks()
        # if time_now - player.time > player.time_step:
        #     player.time = time_now
        #     player.move()
        check_borders(player)
        if check_food(data, player):
            player.send_food_update = True  # Mark food update to be sent to server
        check_self_eating(player)
    check_portal(p)
    data.draw_food(screen)
    pg.display.update()

def draw_grid():
    [pg.draw.line(screen, [50] * 3, (x, 0), (x, WINDOW_SIZE)) for x in range(0, WINDOW_SIZE, TILE_SIZE)]
    [pg.draw.line(screen, [50] * 3, (0, y), (WINDOW_SIZE, y)) for y in range(0, WINDOW_SIZE, TILE_SIZE)]

def main():
    run = True
    n = Network()
    data = n.getP()
    p = data.snakes
    clock = pg.time.Clock()
    
    while run:
        clock.tick(60)
        try:
            data = n.send((data))
            p = data.snakes

        except Exception as e:
            run = False
            print(f"Couldn't get game: {e}")
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            for player in p:
                if player.alive:
                    player.control(event)
                    player.place_portal(event)

        for player in p:
            if player.alive:
                check_borders(player)
                check_self_eating(player)

        redrawWindow(screen, p, data)

if __name__ == "__main__":
    main()
