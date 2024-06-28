import pygame

class Background:

    type: int
    sprites: []
    loaded: int

    def __init__(self, type):
        self.type = type
        self.sprites = [
            pygame.image.load("images/background/screen_1.png").convert_alpha(),
            pygame.image.load("images/background/screen_2.png").convert_alpha(),
            pygame.image.load("images/background/screen_3.png").convert_alpha(),
            pygame.image.load("images/background/castle.png").convert_alpha()
        ]
        self.loaded = 0

    def get_sprite(self):
        self.loaded = 1
        return self.sprites[self.type]