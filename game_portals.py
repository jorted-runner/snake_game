import pygame as pg

class Portal:
    def __init__(self):
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

    def draw_circle(self, screen, x, y, radius, color):
        pg.draw.circle(screen, color, (x, y), radius)

    def place(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            position = event.pos
            if event.button == 1:  # Left mouse button
                self.circles['blue']['pos'] = position
            elif event.button == 3:  # Right mouse button
                self.circles['orange']['pos'] = position

    def draw(self, screen):
        for circle in self.circles.values():
            if circle['pos']:
                x, y = circle['pos'][0], circle['pos'][1]
                self.draw_circle(screen, x, y, 20 // 2, circle['color'])
