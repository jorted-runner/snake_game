import pygame as pg

class Player:
    def __init__(self, pos, color, player_index):
        self.player_index = player_index
        self.size = 20
        self.time = 0
        self.time_step = 250
        self.segments = []
        self.color = color
        self.create_snake(pos)
        self.head = self.segments[0]
        self.direction = 'DOWN'
        self.portal = {
                'color': color,
                'pos': [] 
        }
        self.alive = True
        self.send_food_update  = False
        self.last_teleport_time = 0
        self.ready = False

    def draw_circle(self, screen, x, y, radius, color):
        pg.draw.circle(screen, color, (x, y), radius)

    def place_portal(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            position = event.pos
            if event.button == 1:
                self.portal['pos'] = position

    def draw_portal(self, screen):
        if self.portal['pos']:
            x, y = self.portal['pos'][0], self.portal['pos'][1]
            self.draw_circle(screen, x, y, 26 // 2, self.portal['color'])

    def create_snake(self, positions):
        for pos in positions:
            self.add_segment(pos)

    def add_segment(self, pos):
        new_segment = pg.rect.Rect([pos[0], pos[1], self.size, self.size])
        self.segments.append(new_segment)

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP or event.key == pg.K_w) and self.direction != 'DOWN':
                self.direction = 'UP'
            if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.direction != 'UP':
                self.direction = 'DOWN'
            if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.direction != 'LEFT':
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

    def draw(self, screen):
        [pg.draw.rect(screen, self.color, segment) for segment in self.segments]

    def mark_ready(self):
        self.ready = True