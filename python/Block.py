import pygame
from python.Distance import Distance

class Block:

    y: int
    type: int
    sprites: []
    speed: Distance
    is_hit: bool
    sounds: []
    disguise: int
    state: int

    def __init__(self, type):
        self.type = type
        self.sprites = [
            pygame.image.load('images/objects/blocks/void_block.png').convert_alpha(),
            pygame.image.load('images/objects/blocks/ground_block.png').convert(),
            pygame.image.load('images/objects/blocks/block.png').convert(),
            pygame.image.load('images/objects/blocks/hard_block.png').convert()
        ]
        self.y = 0
        self.speed = Distance(0, -1, 0, 0, 0)
        self.is_hit = False
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_bump.wav')
        ]
        self.disguise = 0
        self.state = 0

    def get_sprite(self):
        return self.sprites[self.type]

    def get_position(self):
        if self.is_hit:
            self.y += self.speed.get_distance(5)
            if self.y > 0:
                self.y = 0
                self.is_hit = False
            else:
                self.speed.add_distance(0, 0, 4, 0, 0)
        return (0, self.y)

    def get_collision(self, xy: tuple):
        if self.type > 0:
            return self.sprites[self.type].get_rect(topleft=(xy[0], xy[1]))

    def hit(self):
        self.speed = Distance(0, -1, 0, 0, 0)
        self.sounds[0].play()
        self.is_hit = True


