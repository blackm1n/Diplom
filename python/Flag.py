import pygame


class Flag:

    x: int
    y: int
    loaded: bool
    activate: bool
    sprites: []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activate = False
        self.loaded = False
        self.sprites = [
            pygame.image.load('images/entities/flagpole/flag.png').convert_alpha()
        ]

    def render(self):
        return

    def get_collision(self):
        return

    def get_sprite(self):
        self.loaded = True
        return self.sprites[0]

    def get_position(self):
        return self.x - 24, self.y
