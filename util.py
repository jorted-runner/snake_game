import random

class Util:
    def __init__(self, screen_width, screen_height, tile_size) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size

    def get_random_position(self):
        x = random.randint(0 + self.tile_size // 2, self.screen_width - self.tile_size // 2)
        y = random.randint(0 + self.tile_size // 2, self.screen_height - self.tile_size // 2)
        return (x, y)