import pygame as pg

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