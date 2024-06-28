import random
import pygame

from python.Distance import Distance


class Koopa:

    x: int
    y: int
    frame: int
    grounded: bool
    loaded: int
    diestate: int
    dead: bool
    kicktime: int
    timer: int
    y_speed: Distance
    x_speed: Distance
    collision: pygame.rect.Rect
    sprites: []
    state: int
    sounds: []
    combo: int
    combo_list: []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = -1
        self.grounded = False
        self.dead = False
        self.kicktime = 0
        self.diestate = 0
        self.timer = 0
        self.y_speed = Distance(0, 0, 0, 0, 0)
        self.x_speed = Distance(0, 0, -5, 0, 0)
        self.state = 0
        self.sprites = [
            [
                pygame.image.load('images/entities/koopa/left_1.png').convert_alpha(),
                pygame.image.load('images/entities/koopa/left_2.png').convert_alpha()
            ],
            [
                pygame.image.load('images/entities/koopa/right_1.png').convert_alpha(),
                pygame.image.load('images/entities/koopa/right_2.png').convert_alpha()
            ],
            [
                pygame.image.load('images/entities/koopa/dead_1.png').convert_alpha(),
                pygame.image.load('images/entities/koopa/dead_2.png').convert_alpha()
            ],
            [
                pygame.image.load('images/entities/koopa/hitbox.png').convert_alpha()
            ]
        ]
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_stomp.wav'),
            pygame.mixer.Sound('sounds/smb_kick.wav')
        ]
        self.collision = self.sprites[3][0].get_rect(topleft=(self.x, self.y))
        self.loaded = 0
        self.combo = 0
        self.combo_list = [0, 500, 800, 1000, 2000, 4000, 5000, 8000]

    def render(self):
        self.loaded = 1
        if not self.dead:
            if not self.grounded:
                self.y -= self.y_speed.get_distance(5)
                self.y_speed.remove_distance_d(Distance(0, 0, 7, 0, 0))
            else:
                self.y_speed = Distance(0, 0, 0, 0, 0)

            if self.x_speed.get_distance(5) < 0:
                self.state = 0
            elif self.x_speed.get_distance(5) > 0:
                self.state = 1

        else:
            self.die(self.diestate)

        self.x += self.x_speed.get_distance(3)
        self.collision = self.sprites[3][0].get_rect(topleft=(self.x, self.y))

    def get_sprite(self):
        if not self.dead:
            if self.frame < 19:
                self.frame += 1
            else:
                self.frame = 0
            return self.sprites[self.state][self.frame // 10]
        return self.sprites[self.state][self.frame]

    def die(self, diestate):
        if not self.dead:
            self.kicktime = 5
            self.x_speed = Distance(0, 0, 0, 0, 0)
            self.timer = 300
            self.sounds[0].play()
            self.dead = True
            self.state = 2
            self.frame = 0

        if self.kicktime > 0:
            self.kicktime -= 1

        if self.x_speed.get_distance(5) != 0:
            self.timer = 300
        else:
            self.combo = 0
            self.timer -= 1

        if self.timer <= 60 and self.timer % 15 == 0:
            self.frame = (self.frame + 1) % 2
        elif self.timer <= 0:
            self.timer = 0
            num = random.randint(0, 1)
            if num == 0:
                self.x_speed = Distance(0, 0, -5, 0, 0)
            else:
                self.x_speed = Distance(0, 0, 5, 0, 0)
            self.state = num
            self.dead = False

    def get_position(self):
        return self.x, self.y - 16

    def get_collision(self):
        return self.collision