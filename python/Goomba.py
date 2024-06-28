import pygame
from python.Distance import Distance


class Goomba:

    x: int
    y: int
    frame: int
    grounded: bool
    loaded: int
    diestate: int
    dead: bool
    timer: int
    y_speed: Distance
    x_speed: Distance
    collision: pygame.rect.Rect
    sprites: []
    sounds: []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = -1
        self.grounded = False
        self.dead = False
        self.diestate = 0
        self.timer = 0
        self.y_speed = Distance(0, 0, 0, 0, 0)
        self.x_speed = Distance(0, 0, -5, 0, 0)
        self.sprites = [
            pygame.image.load('images/entities/goomba/goomba_1.png').convert_alpha(),
            pygame.image.load('images/entities/goomba/goomba_2.png').convert_alpha(),
            pygame.image.load('images/entities/goomba/goomba_dead.png').convert_alpha(),
            pygame.image.load('images/entities/goomba/upside_down.png').convert_alpha()
        ]
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_stomp.wav')
        ]
        self.collision = self.sprites[self.frame].get_rect(topleft=(self.x, self.y))
        self.loaded = 0

    def render(self):
        self.loaded = 1
        if not self.dead:
            if not self.grounded:
                self.y -= self.y_speed.get_distance(5)
                self.y_speed.remove_distance_d(Distance(0, 0, 7, 0, 0))
            else:
                self.y_speed = Distance(0, 0, 0, 0, 0)

            self.x += self.x_speed.get_distance(3)

            self.collision = self.sprites[self.frame // 10].get_rect(topleft=(self.x, self.y))
        else:
            self.die(self.diestate)

    def get_sprite(self):
        if not self.dead:
            if self.frame < 19:
                self.frame += 1
            else:
                self.frame = 0
            return self.sprites[self.frame // 10]
        return self.sprites[self.frame]

    def die(self, diestate):
        if diestate == 0:
            if not self.dead:
                self.timer = 30
                self.sounds[0].play()
                self.dead = True
                self.frame = 2

            if self.timer > 0:
                self.timer -= 1
            else:
                self.x = -666
        else:
            if not self.dead:
                self.grounded = False
                self.y_speed = Distance(0, 4, 0, 0, 0)
                self.sounds[0].play()
                self.dead = True
                self.frame = 3
                self.diestate = 1
                if self.x_speed.get_distance(5) > 0:
                    self.x_speed.add_distance(0, 1, 0, 0, 0)
                else:
                    self.x_speed.remove_distance(0, 1, 0, 0, 0)
                self.x_speed = self.x_speed.reverse()

            self.x += self.x_speed.get_distance(5)
            self.y -= self.y_speed.get_distance(5)
            self.y_speed.remove_distance_d(Distance(0, 0, 7, 0, 0))

            if self.y >= 1000:
                self.x = -666

    def get_position(self):
        return self.x, self.y

    def get_collision(self):
        if not self.dead:
            return self.collision

