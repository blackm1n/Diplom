import pygame
from python.Distance import Distance

class Mario:
    x: int
    max_x: int
    y: int
    max_speed: Distance
    current_speed: Distance
    direction: int
    frame: int
    frametimer: int
    state: int
    is_jump: bool
    jump_speed: Distance
    start_jump_speed: Distance
    gravity: Distance
    gravity_a: Distance
    is_dead: bool
    fastrunning: bool
    grounded: bool
    sounds: list[pygame.mixer.Sound]
    sprites: list[list[list[pygame.surface.Surface]]]
    timer: int
    old_direction: int
    collision: pygame.rect.Rect
    acceleration_speed: Distance
    combo: int
    combo_list: []
    score: int
    coins: int
    bounce_timer: int
    end: bool
    ai: bool

    def __init__(self, ai):
        self.x = 80
        self.max_x = 80
        self.y = 370
        self.max_speed: Distance = Distance(0, 1, 9, 0, 0)
        self.current_speed: Distance = Distance(0, 0, 0, 0, 0)
        self.acceleration_speed: Distance = Distance(0, 0, 0, 9, 8)
        self.frame = 0
        self.state = 0
        self.is_jump = False
        self.can_jump = True
        self.grounded = True
        self.jump_speed: Distance = Distance(0, 0, 0, 0, 0)
        self.start_jump_speed: Distance = Distance(0, 0, 0, 0, 0)
        self.gravity: Distance = Distance(0, 0, 7, 0, 0)
        self.gravity_a: Distance = Distance(0, 0, 0, 0, 0)
        self.combo = 0
        self.combo_list = [0, 100, 200, 400, 500, 800, 1000, 2000, 4000, 5000, 8000]
        self.is_dead = False
        self.fastrunning = False
        self.frametimer = 0
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_jump-small.wav'),
            pygame.mixer.Sound('sounds/smb_mariodie.wav')
        ]
        self.sprites = [
            [
                [
                    pygame.image.load('images/mario/idle_right.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_right_1.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_right_2.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_right_3.png').convert_alpha(),
                    pygame.image.load('images/mario/skid_right.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/jump_right.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_right.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_right.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_right.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_right.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/dead.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/climb_right_1.png').convert_alpha(),
                    pygame.image.load('images/mario/climb_right_2.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/invisible.png').convert_alpha()
                ]
            ],
            [
                [
                    pygame.image.load('images/mario/idle_left.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_left_1.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_left_2.png').convert_alpha(),
                    pygame.image.load('images/mario/walk_left_3.png').convert_alpha(),
                    pygame.image.load('images/mario/skid_left.png').convert_alpha()],
                [
                    pygame.image.load('images/mario/jump_left.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_left.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_left.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_left.png').convert_alpha(),
                    pygame.image.load('images/mario/jump_left.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/dead.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/climb_left_1.png').convert_alpha(),
                    pygame.image.load('images/mario/climb_left_2.png').convert_alpha()
                ],
                [
                    pygame.image.load('images/mario/invisible.png').convert_alpha()
                ]
            ]]
        self.timer = 0
        self.direction = 0
        self.collision = self.sprites[self.direction][self.state][self.frame].get_rect(topleft=(self.x, self.y))
        self.score = 0
        self.coins = 0
        self.bounce_timer = 0
        self.end = False
        self.ai = ai

    def render(self, keys):
        if not self.end:
            if not self.is_dead:
                if not self.ai:
                    if (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]) and self.grounded:
                        self.run(keys)
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                        self.air_run(keys)
                    else:
                        self.stand()

                    if keys[pygame.K_SPACE] or self.is_jump:
                        self.jump()

                    if keys[pygame.K_LSHIFT]:
                        self.fast_run()
                    elif self.is_fastrunning():
                        self.slow_run()

                    if not self.grounded:
                        if self.jump_speed.get_distance(5) <= Distance(0, -4, -8, 0, 0).get_distance(5):
                            self.jump_speed: Distance = Distance(0, -4, 0, 0, 0)
                        self.y -= self.jump_speed.get_distance(5)
                        if keys[pygame.K_SPACE] and self.jump_speed.get_distance(5) > 0 and self.is_jump:
                            self.jump_speed.remove_distance_d(self.gravity_a)
                        else:
                            self.jump_speed.remove_distance_d(self.gravity)
                else:
                    if (keys[2] == 1 or keys[1] == 1) and self.grounded:
                        self.run(keys)
                    elif keys[2] == 1 or keys[1] == 1:
                        self.air_run(keys)
                    else:
                        self.stand()

                    if keys[3] == 1 or self.is_jump:
                        self.jump()

                    if keys[4] == 1:
                        self.fast_run()
                    elif self.is_fastrunning():
                        self.slow_run()

                    if not self.grounded:
                        if self.jump_speed.get_distance(5) <= Distance(0, -4, -8, 0, 0).get_distance(5):
                            self.jump_speed: Distance = Distance(0, -4, 0, 0, 0)
                        self.y -= self.jump_speed.get_distance(5)
                        if keys[3] == 1 and self.jump_speed.get_distance(5) > 0 and self.is_jump:
                            self.jump_speed.remove_distance_d(self.gravity_a)
                        else:
                            self.jump_speed.remove_distance_d(self.gravity)

                if self.y >= 448:
                    self.die()

                if self.bounce_timer > 0:
                    self.bounce_timer -= 1

                self.x += self.current_speed.get_distance(3)

                if self.x >= self.max_x + 32:
                    self.max_x = self.x
                    self.score += 16

                self.collision = self.sprites[self.direction][self.state][self.frame].get_rect(topleft=(self.x, self.y))
            else:
                self.die()
        else:
            if not self.grounded:
                self.y -= self.jump_speed.get_distance(5)
                self.jump_speed.remove_distance_d(self.gravity)
            self.x += self.current_speed.get_distance(3)
            self.collision = self.sprites[self.direction][self.state][self.frame].get_rect(topleft=(self.x, self.y))

    def run(self, keys):
        if not self.ai:
            if keys[pygame.K_RIGHT]:
                self.direction = 0
                acceleration_speed = self.acceleration_speed
                min_speed = Distance(0, 0, 1, 3, 0)
                skid_speed = Distance(0, 0, 1, 10, 0)
            else:
                self.direction = 1
                acceleration_speed = self.acceleration_speed.reverse()
                min_speed = Distance(0, 0, -1, -3, 0)
                skid_speed = Distance(0, 0, -1, -10, 0)
        else:
            if keys[2] == 1:
                self.direction = 0
                acceleration_speed = self.acceleration_speed
                min_speed = Distance(0, 0, 1, 3, 0)
                skid_speed = Distance(0, 0, 1, 10, 0)
            else:
                self.direction = 1
                acceleration_speed = self.acceleration_speed.reverse()
                min_speed = Distance(0, 0, -1, -3, 0)
                skid_speed = Distance(0, 0, -1, -10, 0)

        self.state = 0

        if self.current_speed.get_distance(5) + (2 * self.current_speed.get_distance(5) * -self.direction) >= 0:
            if abs(self.current_speed.get_distance(5)) == 0:
                self.current_speed.add_distance_d(min_speed)
            elif abs(self.current_speed.get_distance(5)) <= self.max_speed.get_distance(3):
                self.current_speed.add_distance_d(acceleration_speed)
            elif abs(self.current_speed.get_distance(5)) > self.max_speed.get_distance(3):
                self.current_speed.set_subsubpixels(0)
                self.current_speed.set_subsubsubpixels(0)

            if not self.is_jump:
                if abs(self.current_speed.get_distance(5)) > self.max_speed.get_distance(3) and self.timer > 0 and self.fastrunning == False:
                    self.timer -= 1
                    if self.timer == 0:
                        self.current_speed.remove_distance_d(self.current_speed)
                        self.current_speed.add_distance_d(self.max_speed)

            if Distance(0, -1, -9, 0, 0).get_distance(5) <= self.current_speed.get_distance(3) <= Distance(0, 1, 9, 0, 0).get_distance(5):
                self.frame = (self.frametimer // 5 % 3) + 1
            else:
                self.frame = (self.frametimer // 2 % 3) + 1
            self.frametimer += 1

        else:
            if abs(self.current_speed.get_distance(5)) > Distance(0, 0, 9, 0, 0).get_distance(5):
                self.frame = 4
                self.current_speed.add_distance_d(skid_speed)
            else:
                self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        self.start_jump_speed = self.current_speed.get_distance_d()

    def air_run(self, keys):
        if Distance(0, -1, -9, 0, 0).get_distance(5) <= self.start_jump_speed.get_distance(3) <= Distance(0, 1, 9, 0, 0).get_distance(5):
            max_speed = Distance(0, 1, 9, 0, 0)
        else:
            max_speed = Distance(0, 2, 9, 0, 0)

        if not self.ai:
            if keys[pygame.K_RIGHT]:
                if self.current_speed.get_distance(3) < max_speed.get_distance(5):
                    if self.current_speed.get_distance(3) < Distance(0, 1, 9, 0, 0).get_distance(5):
                        self.current_speed.add_distance(0, 0, 0, 9, 8)
                    else:
                        self.current_speed.add_distance(0, 0, 0, 14, 4)
                else:
                    self.current_speed.set_subsubpixels(0)
                    self.current_speed.set_subsubsubpixels(0)

            elif keys[pygame.K_LEFT]:
                if self.current_speed.get_distance(3) > -max_speed.get_distance(5):
                    if self.current_speed.get_distance(3) >= Distance(0, 1, 9, 0, 0).get_distance(5):
                        self.current_speed.remove_distance(0, 0, 0, 14, 4)
                    elif self.start_jump_speed.get_distance(3) >= Distance(0, 1, 13, 0, 0).get_distance(5):
                        self.current_speed.remove_distance(0, 0, 0, 13, 0)
                    else:
                        self.current_speed.remove_distance(0, 0, 0, 9, 8)
                else:
                    self.current_speed.set_subsubpixels(0)
                    self.current_speed.set_subsubsubpixels(0)
        else:
            if keys[2] == 1:
                if self.current_speed.get_distance(3) < max_speed.get_distance(5):
                    if self.current_speed.get_distance(3) < Distance(0, 1, 9, 0, 0).get_distance(5):
                        self.current_speed.add_distance(0, 0, 0, 9, 8)
                    else:
                        self.current_speed.add_distance(0, 0, 0, 14, 4)
                else:
                    self.current_speed.set_subsubpixels(0)
                    self.current_speed.set_subsubsubpixels(0)

            elif keys[1] == 1:
                if self.current_speed.get_distance(3) > -max_speed.get_distance(5):
                    if self.current_speed.get_distance(3) >= Distance(0, 1, 9, 0, 0).get_distance(5):
                        self.current_speed.remove_distance(0, 0, 0, 14, 4)
                    elif self.start_jump_speed.get_distance(3) >= Distance(0, 1, 13, 0, 0).get_distance(5):
                        self.current_speed.remove_distance(0, 0, 0, 13, 0)
                    else:
                        self.current_speed.remove_distance(0, 0, 0, 9, 8)
                else:
                    self.current_speed.set_subsubpixels(0)
                    self.current_speed.set_subsubsubpixels(0)

        if not self.is_jump:
            if Distance(0, -1, -9, 0, 0).get_distance(5) <= self.current_speed.get_distance(3) <= Distance(0, 1, 9, 0, 0).get_distance(5):
                self.frame = (self.frametimer // 5 % 3) + 1
            else:
                self.frame = (self.frametimer // 2 % 3) + 1
            self.frametimer += 1

    def stand(self):
        if abs(self.current_speed.get_distance(5)) < Distance(0, 0, 1, 0, 0).get_distance(5):
            self.current_speed: Distance = Distance(0, 0, 0, 0, 0)

        if not self.is_jump:
            if self.current_speed.get_distance(5) > 0:
                self.current_speed.remove_distance(0, 0, 0, 13, 0)
            elif self.current_speed.get_distance(5) < 0:
                self.current_speed.add_distance(0, 0, 0, 13, 0)

        self.frame = 0
        if self.grounded:
            self.state = 0

    def jump(self):
        if not self.is_jump and self.grounded:
            if Distance(0, -1, 0, 0, 0).get_distance(5) < self.current_speed.get_distance(3) < Distance(0, 1, 0, 0, 0).get_distance(5):
                self.jump_speed: Distance = Distance(0, 4, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 7, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 2, 0, 0)
            elif Distance(0, -2, -4, -15, -15).get_distance(5) < self.current_speed.get_distance(3) < Distance(0, 2, 4, 15, 15).get_distance(5):
                self.jump_speed: Distance = Distance(0, 4, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 6, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 1, 14, 0)
            else:
                self.jump_speed: Distance = Distance(0, 5, 0, 0, 0)
                self.gravity: Distance = Distance(0, 0, 9, 0, 0)
                self.gravity_a: Distance = Distance(0, 0, 2, 8, 0)
            self.start_jump_speed = self.current_speed.get_distance_d()
            self.is_jump = True
            self.grounded = False
            self.sounds[0].play()
        else:
            self.state = 1
            self.frame = 0
            if self.grounded:
                self.start_jump_speed = self.current_speed.get_distance_d()
                self.state = 0
                self.is_jump = False

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.sounds[1].play()
        self.grounded = False
        self.state = 2
        self.frame = 0
        self.timer += 1
        if self.timer == 60:
            self.jump_speed = Distance(0, 6, 0, 0, 0)
        elif self.timer > 60:
            self.y -= self.jump_speed.get_distance(5)
            self.jump_speed.remove_distance_d(Distance(0, 0, 7, 0, 0))


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

    def set_speed(self, distance):
        self.current_speed = distance

    def get_sprite(self):
        return self.sprites[self.direction][self.state][self.frame]

    def get_position(self):
        return self.x, self.y

    def is_fastrunning(self):
        return self.fastrunning
