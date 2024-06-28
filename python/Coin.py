import pygame
from python.Distance import Distance


class Coin:

    x: int
    spawn_y: int
    y: int
    frame: int
    dead: bool
    speed: Distance
    sprites: []

    def __init__(self, x, y):
        self.x = x
        self.spawn_y = y
        self.dead = False
        self.y = self.spawn_y
        self.frame = 0
        self.speed = Distance(0, 6, 0, 0, 0)
        self.sprites = [
            pygame.image.load('images/entities/coin/frame_1.png').convert_alpha(),
            pygame.image.load('images/entities/coin/frame_2.png').convert_alpha(),
            pygame.image.load('images/entities/coin/frame_3.png').convert_alpha(),
            pygame.image.load('images/entities/coin/frame_4.png').convert_alpha()
        ]

    def render(self):
        if self.y <= self.spawn_y:
            self.y -= self.speed.get_distance(5)
            self.speed.remove_distance_d(Distance(0, 0, 7, 0, 0))
        else:
            self.x = -666

    def get_collision(self):
        return

    def get_sprite(self):
        if self.frame < 6:
            self.frame += 1
        else:
            self.frame = 0
        return self.sprites[self.frame // 2]

    def get_position(self):
        return self.x, self.y
