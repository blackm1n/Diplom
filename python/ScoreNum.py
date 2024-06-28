import pygame
from python.Distance import Distance


class ScoreNum:

    x: int
    spawn_y: int
    y: int
    dead: bool
    timer: int
    spawn_timer: int
    frame: int
    speed: Distance
    sprites: []

    def __init__(self, x, y, frame, spawn_timer):
        self.x = x
        self.spawn_y = y
        self.y = self.spawn_y
        self.spawn_timer = spawn_timer
        self.dead = False
        self.timer = 30
        self.frame = frame
        self.speed = Distance(0, 0, 4, 0, 0)
        self.sprites = [
            pygame.image.load('images/scorenum/nothing.png').convert_alpha(),
            pygame.image.load('images/scorenum/100.png').convert_alpha(),
            pygame.image.load('images/scorenum/200.png').convert_alpha(),
            pygame.image.load('images/scorenum/400.png').convert_alpha(),
            pygame.image.load('images/scorenum/500.png').convert_alpha(),
            pygame.image.load('images/scorenum/800.png').convert_alpha(),
            pygame.image.load('images/scorenum/1000.png').convert_alpha(),
            pygame.image.load('images/scorenum/2000.png').convert_alpha(),
            pygame.image.load('images/scorenum/4000.png').convert_alpha(),
            pygame.image.load('images/scorenum/5000.png').convert_alpha(),
            pygame.image.load('images/scorenum/8000.png').convert_alpha()
        ]

    def render(self):
        if self.spawn_timer <= 0:
            self.y -= self.speed.get_distance(5)
            self.timer -= 1

            if self.timer < 0:
                self.x = -666

    def get_collision(self):
        return

    def get_sprite(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return self.sprites[0]
        else:
            return self.sprites[self.frame]

    def get_position(self):
        return self.x, self.y