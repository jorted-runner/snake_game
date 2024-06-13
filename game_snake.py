import pygame as pg
import math

class Snake:
    def __init__(self, pos, color):
        self.size = 20
        self.segments = []
        self.color = color
        self.create_snake(pos)
        self.head = self.segments[0]
        self.direction = 'DOWN'

    def create_snake(self, positions):
        for pos in positions:
            self.add_segment(pos)
    
    # will need to fix this logic
    def check_borders(self):
        if self.segments[0].left < 0 or self.segments[0].right > 800:
            pass
        if self.segments[0].top < 0 or self.segments[0].bottom > 800:
            pass

    def check_food(self, food):
        center_head = self.segments[0].center
        center_food = food.rect.center
        distance = math.sqrt((center_food[0] - center_head[0]) **2 + (center_food[1] - center_head[1]) **2)
        if distance < self.size - 3:
            # This needs to be done more dynamically
            self.food.rect.center = food.get_random_position(800, 800, 20)
            # self.game.fps *= 1.01
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
        new_segment = pg.rect.Rect([pos[0], pos[1], self.size, self.size])
        self.segments.append(new_segment)

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == pg.K_w:
                self.direction = 'UP'
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.direction = 'DOWN'
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.direction = 'LEFT'
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
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
        
    def update(self, screen):
        self.check_self_eating()
        self.check_borders()
        # self.check_food(food)
        # self.check_portal()
        self.move()

    def draw(self, screen):
        [pg.draw.rect(screen, self.color, segment) for segment in self.segments]