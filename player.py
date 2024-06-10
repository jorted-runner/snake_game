import pygame
import sys

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = {'x': 1}

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self, win):
        for key in self.vel.keys():
            if key == 'x':
                self.x += self.vel['x']
            elif key == 'y':
                self.y += self.vel['y']

        self.check_col_wall(win)
    
    def update_vel(self, win):
        keys = pygame.key.get_pressed()
        vel = next(iter(self.vel.values()))
        if keys[pygame.K_LEFT]:
            self.vel = {'x': abs(vel) * -1}

        if keys[pygame.K_RIGHT]:
            self.vel = {'x': abs(vel)}

        if keys[pygame.K_UP]:
            self.vel = {'y': abs(vel)  * -1}

        if keys[pygame.K_DOWN]:
            self.vel = {'y': abs(vel)}

        self.move(win)

    def check_col_wall(self, win):
        if 0 < self.x < (win.get_width() - self.width) and 0 <= self.y < (win.get_height() - self.height):
            self.update()
        else:
            print('you hit the edge')
            pygame.quit()
            sys.exit()
    
    def check_col_fruit(self, fruit):
        if self.x + self.width / 2 <= fruit.x - fruit.width/2 and self.y + self.width / 2 <= fruit.y - fruit.height/2:
            print('you hit the fruit')
            pygame.quit()
            sys.exit()
        else:
            self.update()
            

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)