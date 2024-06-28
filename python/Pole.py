import pygame


class Pole:

    x: int
    y: int
    loaded: bool
    sprites: []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loaded = False
        self.sprites = [
            pygame.image.load('images/entities/flagpole/pole.png').convert_alpha()
        ]

    def render(self):
        return

    def get_collision(self):
        return self.sprites[0].get_rect(topleft=(self.x, self.y))

    def get_sprite(self):
        self.loaded = True
        return self.sprites[0]

    def get_position(self):
        return self.x, self.y
