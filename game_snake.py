import pygame as pg
import math

class Snake:
    def __init__(self, pos, color):
        self.size = 20
        self.time = 0
        self.time_step = 150
        self.segments = []
        self.color = color
        self.create_snake(pos)
        self.head = self.segments[0]
        self.direction = 'DOWN'

    def create_snake(self, positions):
        for pos in positions:
            self.add_segment(pos)

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

    def draw(self, screen):
        [pg.draw.rect(screen, self.color, segment) for segment in self.segments]