import pygame


class Pipe:

    type: int
    sprites: []
    disguise: int
    state: int

    def __init__(self, type):
        self.type = type
        self.sprites = [
            pygame.image.load('images/objects/pipe/head.png').convert_alpha(),
            pygame.image.load('images/objects/pipe/body.png').convert_alpha(),
        ]
        self.disguise = 0
        self.state = 0

    def get_sprite(self):
        return self.sprites[self.type]

    def get_position(self):
        return (0, 0)

    def get_collision(self, xy: tuple):
        return self.sprites[self.type].get_rect(topleft=xy)
