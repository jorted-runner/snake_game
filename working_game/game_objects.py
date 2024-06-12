import pygame as pg
import math

class Snake:
    def __init__(self, game, pos, color):
        self.game = game
        self.size = game.TILE_SIZE
        self.segments = []
        self.color = color
        self.create_snake(pos)
        self.head = self.segments[0]
        self.direction = 'DOWN'

    def create_snake(self, positions):
        for pos in positions:
            self.add_segment(pos)
    
    def check_borders(self):
        if self.segments[0].left < 0 or self.segments[0].right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.segments[0].top < 0 or self.segments[0].bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_food(self):
        center_head = self.segments[0].center
        center_food = self.game.food.rect.center
        distance = math.sqrt((center_food[0] - center_head[0]) **2 + (center_food[1] - center_head[1]) **2)
        if distance < self.size - 3:
            self.game.food.rect.center = self.game.get_random_position()
            self.game.fps *= 1.01
            self.add_segment(self.segments[-1].center)

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

    def add_segment(self, pos):
        new_segment = pg.rect.Rect([pos[0], pos[1], self.game.TILE_SIZE, self.game.TILE_SIZE])
        self.segments.append(new_segment)

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.direction = 'UP'
            if event.key == pg.K_DOWN:
                self.direction = 'DOWN'
            if event.key == pg.K_LEFT:
                self.direction = 'LEFT'
            if event.key == pg.K_RIGHT:
                self.direction = 'RIGHT'
    
    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i - 1].x
            self.segments[i].y = self.segments[i - 1].y

        if self.direction == 'RIGHT':
            self.segments[0].centerx = self.segments[0].centerx + self.size
        if self.direction == 'LEFT':
            self.segments[0].centerx = self.segments[0].centerx + -self.size
        if self.direction == 'UP':
            self.segments[0].centery = self.segments[0].centery + -self.size
        if self.direction == 'DOWN':
            self.segments[0].centery = self.segments[0].centery + self.size
        
    def update(self):
        self.check_self_eating()
        self.check_borders()
        self.check_food()
        self.check_portal()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, self.color, segment) for segment in self.segments]


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        self.rect.center = self.game.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)

class Portal:
    def __init__(self, game):
        self.game = game
        self.circles = {
            'orange': {
                'color': (255, 165, 0),
                'pos': [] 
            },
            'blue': {
                'color': (0, 0, 255),
                'pos': [] 
            }
        }

    def draw_circle(self, x, y, radius, color):
        pg.draw.circle(self.game.screen, color, (x, y), radius)

    def place(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            position = event.pos
            if event.button == 1:  # Left mouse button
                self.circles['blue']['pos'] = position
                self.draw_circle(position[0], position[1], self.game.TILE_SIZE // 2, self.circles['blue']['color'])
            elif event.button == 3:  # Right mouse button
                self.circles['orange']['pos'] = position
                self.draw_circle(position[0], position[1], self.game.TILE_SIZE // 2, self.circles['orange']['color'])

    def draw(self):
        for color, circle in self.circles.items():
            if circle['pos']:
                x, y = circle['pos'][0], circle['pos'][1]
                self.draw_circle(x, y, self.game.TILE_SIZE // 2, circle['color'])
                



