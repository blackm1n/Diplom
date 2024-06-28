import pygame
from python.Distance import Distance

class CoinBlock:

    y: int
    state: int
    contains: str
    frame: int
    sprites: []
    speed: Distance
    is_hit: bool
    sounds: []
    disguise: int
    hits: int

    def __init__(self, contains):
        self.contains = contains
        if self.contains.split("_")[0] == "Hidden":
            self.disguise = 1
        elif self.contains.split("_")[0] == "Invisible":
            self.disguise = 2
        else:
            self.disguise = 0
        self.state = 0
        self.frame = -1
        self.sprites = [
            pygame.image.load('images/objects/coinblock/frame_1.png').convert_alpha(),
            pygame.image.load('images/objects/coinblock/frame_2.png').convert_alpha(),
            pygame.image.load('images/objects/coinblock/frame_3.png').convert_alpha(),
            pygame.image.load('images/objects/coinblock/frame_2.png').convert_alpha(),
            pygame.image.load('images/objects/coinblock/frame_1.png').convert_alpha(),
            pygame.image.load('images/objects/coinblock/frame_4.png').convert_alpha(),
            pygame.image.load('images/objects/blocks/block.png').convert_alpha(),
            pygame.image.load('images/objects/blocks/void_block.png').convert_alpha()
        ]
        self.y = 0
        self.speed = Distance(0, -1, 0, 0, 0)
        self.is_hit = False
        self.hits = 0
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_bump.wav'),
            pygame.mixer.Sound('sounds/smb_coin.wav')
        ]

    def get_sprite(self):
        if self.state == 0:
            if self.disguise == 0:
                if self.frame < 49:
                    self.frame += 1
                else:
                    self.frame = 0
            elif self.disguise == 1:
                self.frame = 60
            else:
                self.frame = 70
        else:
            self.frame = 50
        return self.sprites[self.frame // 10]

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
        return self.sprites[self.frame // 10].get_rect(topleft=(xy[0], xy[1]))

    def hit(self):
        if self.state == 0:
            self.speed = Distance(0, -1, 0, 0, 0)
            self.sounds[0].play()
            if self.contains == "Coin" or self.contains == "Hidden_Coin" or self.contains == "Invisible_Coin":
                self.sounds[1].play()
            self.hits += 1
            if (self.disguise == 1 and self.hits == 10 and self.contains == "Hidden_Coin") or (self.disguise != 1):
                self.state = 1
            self.is_hit = True