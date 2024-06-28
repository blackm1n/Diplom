import pygame
from Distance import Distance


class Mario:
    x: int
    y: int
    max_speed: Distance
    current_speed: Distance
    frame: int
    state: int
    is_jump: bool
    jump_speed: int
    gravity: Distance
    gravity_a: Distance
    is_dead: bool
    fastrunning: bool
    grounded: bool
    sounds: list[pygame.mixer.Sound]
    sprites: list[list[pygame.surface.Surface]]
    timer: int
    old_direction: int
    acceleration_speed: Distance

    def __init__(self, ai):
        self.x = 84
        self.y = 370
        self.max_speed: Distance = Distance(0, 1, 9, 0, 0)
        self.current_speed: Distance = Distance(0, 0, 0, 0, 0)
        self.acceleration_speed: Distance = Distance(0, 0, 0, 9, 8)
        self.frame = 0
        self.state = 0
        self.is_jump = False
        self.grounded = True
        self.jump_speed: Distance = Distance(0, 0, 0, 0, 0)
        self.gravity: Distance = Distance(0, 0, 0, 0, 0)
        self.gravity_a: Distance = Distance(0, 0, 0, 0, 0)
        self.is_dead = False
        self.fastrunning = False
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_jump-small.wav'),
            pygame.mixer.Sound('sounds/smb_mariodie.wav')
        ]
        self.sprites = [
            [
                pygame.image.load('images/mario/idle_right.png').convert_alpha(),
                pygame.image.load('images/mario/walk_right_1.png').convert_alpha(),
                pygame.image.load('images/mario/walk_right_2.png').convert_alpha(),
                pygame.image.load('images/mario/walk_right_3.png').convert_alpha(),
                pygame.image.load('images/mario/skid_right.png').convert_alpha()],
            [
                pygame.image.load('images/mario/idle_left.png').convert_alpha(),
                pygame.image.load('images/mario/walk_left_1.png').convert_alpha(),
                pygame.image.load('images/mario/walk_left_2.png').convert_alpha(),
                pygame.image.load('images/mario/walk_left_3.png').convert_alpha(),
                pygame.image.load('images/mario/skid_left.png').convert_alpha()],
            [
                pygame.image.load('images/mario/jump_right.png').convert_alpha(),
                pygame.image.load('images/mario/jump_left.png').convert_alpha()],
            [
                pygame.image.load('images/mario/dead.png').convert_alpha()
            ]
        ]
        self.timer = 0

    def run_right(self):
        self.state = 0
        if self.current_speed.get_distance(5) >= 0:
            if self.current_speed.get_distance(5) == 0:
                self.current_speed.add_distance(0, 0, 1, 3, 0)
            elif self.current_speed.get_distance(5) < self.max_speed.get_distance(3):
                self.current_speed.add_distance_d(self.acceleration_speed)
            elif self.current_speed.get_distance(5) >= self.max_speed.get_distance(3):
                self.current_speed.set_subsubpixels(0)
                self.current_speed.set_subsubsubpixels(0)

            if not self.is_jump:
                if self.current_speed.get_distance(5) > self.max_speed.get_distance(3) and self.timer > 0 and self.fastrunning == False:
                    self.timer -= 1
                    if self.timer == 0:
                        self.current_speed.remove_distance_d(self.current_speed)
                        self.current_speed.add_distance_d(self.max_speed)

            if self.frame >= 3:
                self.frame = 1
            else:
                self.frame += 1
        else:
            if self.current_speed.get_distance(5) < Distance(0, 0, -9, 0, 0).get_distance(5):
                self.frame = 4
                self.current_speed.add_distance(0, 0, 1, 10, 0)
            else:
                self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if self.x <= 0 and self.current_speed.get_distance(5) <= 0:
            self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if self.x < 224 and not (self.x <= 0 and self.current_speed.get_distance(5) < 0):
            self.x += self.current_speed.get_distance(3)

    def run_left(self):
        self.state = 1
        if self.current_speed.get_distance(5) <= 0:
            if self.current_speed.get_distance(5) == 0:
                self.current_speed.remove_distance(0, 0, 1, 3, 0)
            elif self.current_speed.get_distance(5) > -self.max_speed.get_distance(3):
                self.current_speed.remove_distance_d(self.acceleration_speed)
            elif self.current_speed.get_distance(5) <= -self.max_speed.get_distance(3):
                self.current_speed.set_subsubpixels(0)
                self.current_speed.set_subsubsubpixels(0)

            if not self.is_jump:
                if self.current_speed.get_distance(5) < -self.max_speed.get_distance(3) and self.timer > 0 and self.fastrunning == False:
                    self.timer -= 1
                    if self.timer == 0:
                        self.current_speed.remove_distance_d(self.current_speed)
                        self.current_speed.remove_distance_d(self.max_speed)

            if self.frame >= 3:
                 self.frame = 1
            else:
                self.frame += 1
        else:
            if self.current_speed.get_distance(5) > Distance(0, 0, 9, 0, 0).get_distance(5):
                self.frame = 4
                self.current_speed.remove_distance(0, 0, 1, 10, 0)
            else:
                self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if self.x <= 0:
            self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if self.x > 0 and not (self.x >= 224 and self.current_speed.get_distance(5) > 0):
            self.x += self.current_speed.get_distance(3)

    def stand(self):
        if Distance(0, 0, -1, 0, 0).get_distance(5) < self.current_speed.get_distance(5) < Distance(0, 0, 1, 0, 0).get_distance(5):
            self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if not self.is_jump:
            if self.current_speed.get_distance(5) > 0:
                self.current_speed.remove_distance(0, 0, 0, 13, 0)
            elif self.current_speed.get_distance(5) < 0:
                self.current_speed.add_distance(0, 0, 0, 13, 0)

        if self.x < 224 and self.x > 0:
            self.x += self.current_speed.get_distance(3)
        self.frame = 0

    def jump(self, hold):
        if not self.is_jump:
            self.old_direction = self.state
            if Distance(0, -1, 0, 0, 0).get_distance(5) < self.current_speed.get_distance(5) < Distance(0, 1, 0, 0, 0).get_distance(5):
                self.jump_speed: Distance = Distance(0, 4, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 7, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 2, 0, 0)
            elif Distance(0, -2, -4, -15, -15).get_distance(5) < self.current_speed.get_distance(5) < Distance(0, 2, 4, 15, 15).get_distance(5):
                self.jump_speed: Distance = Distance(0, 4, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 6, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 1, 14, 0)
            else:
                self.jump_speed: Distance = Distance(0, 5, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 9, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 2, 8, 0)
            self.is_jump = True
            self.grounded = False
            self.sounds[0].play()
        else:
            self.state = 2
            self.frame = self.old_direction
            if not self.grounded:
                self.y -= self.jump_speed.get_distance(5)
                if hold == 1 and self.jump_speed.get_distance(5) > 0:
                    self.jump_speed.remove_distance_d(self.gravity_a)
                else:
                    self.jump_speed.remove_distance_d(self.gravity)
            else:
                self.is_jump = False
                self.state = self.old_direction

            if self.y > 370:
                self.y = 370
                self.grounded = True




    def fast_run(self):
        self.max_speed: Distance = Distance(0, 2, 9, 0, 0)
        self.acceleration_speed: Distance = Distance(0, 0, 0, 14, 4)
        self.timer = 10
        self.fastrunning = True

    def slow_run(self):
        self.max_speed: Distance = Distance(0, 1, 9, 0, 0)
        self.acceleration_speed: Distance = Distance(0, 0, 0, 9, 8)
        self.fastrunning = False

    def get_speed(self):
        return self.current_speed.get_distance(3)

    def get_sprite(self):
        return self.sprites[self.state][self.frame]

    def get_position(self):
        return self.x, self.y

    def is_fastrunning(self):
        return self.fastrunning
