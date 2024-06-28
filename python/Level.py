import numpy as np
import pygame.mixer

from python.Background import Background
from python.Block import Block
from python.Coin import Coin
from python.CoinBlock import CoinBlock
from python.Flag import Flag
from python.Goomba import Goomba
from python.Koopa import Koopa
from python.LevelMario import Mario
from python.Distance import Distance
from python.Pipe import Pipe
from python.Pole import Pole
from python.ScoreNum import ScoreNum

bottomless_deaths = 0
game_won = True
goomba_deaths = 0


class Level:
    camera_x: int
    objects: [[]]
    loaded_objects: [[]]
    entities: []
    loaded_entities: []
    backgrounds: []
    loaded_backgrounds: []
    sounds: []
    mario: Mario
    flag: Flag
    end_state: int
    timer: int
    loaded_pos: int
    old_score: int
    backwall: bool
    init_backwall: int
    max_x: int
    ground_distance: int
    next_to_block: bool
    pipe_reward: float
    bottomless_pit: bool

    def __init__(self, x, load, ai):
        self.camera_x = 0
        self.objects = [[Block(0) if i < 13 else Block(1) for i in range(15)] for j in range(x)]
        # self.objects[7][7] = CoinBlock("Coin")
        # for i in range(6):
        #     self.objects[9 + i][10] = Block(2)
        # for i in range(6):
        #     self.objects[12 + i][7] = Block(2)
        # for i in range(6):
        #     self.objects[15 + i][4] = Block(2)
        # for i in range(6):
        #     self.objects[21 + i][7] = Block(2)
        # for i in range(6):
        #     self.objects[24 + i][10] = Block(2)
        # self.objects[32][10] = Pipe(0)
        # self.objects[32][11] = Pipe(1)
        # self.objects[32][12] = Pipe(1)
        self.loaded_objects = []
        self.entities = []
        self.loaded_entities = []
        self.flag = Flag(-666, -666)
        self.backgrounds = [(i * 512, 48, Background(i % 3)) for i in range((x // 16) + 1)]
        self.backgrounds.append((6464, 256, Background(3)))
        self.loaded_backgrounds = [self.backgrounds[0], self.backgrounds[1]]
        self.sounds = [
            pygame.mixer.Sound('sounds/smb_flagpole.wav'),
            pygame.mixer.Sound('sounds/smb_stage_clear.wav')
        ]
        if load:
            self.import_l()
        for i in range(24):
            self.loaded_objects.append(self.objects[i])
        self.end_state = 0
        self.timer = 30
        self.loaded_pos = 0
        self.mario: Mario = Mario(ai)
        self.old_score = 0
        self.max_x = self.mario.x
        self.init_backwall = self.mario.x
        self.ground_distance = 0
        self.next_to_block = False
        self.pipe_reward = 0
        self.bottomless_pit = False

    def load_objects(self):
        new_pos = int(self.camera_x // 32)
        # self.loaded_objects = []
        # for i in range(24):
        #     self.loaded_objects.append(self.objects[i + new_pos])
        if new_pos != self.loaded_pos:
            self.loaded_objects.pop(0)
            self.loaded_objects.append(self.objects[new_pos + 23])

    def get_objects(self):
        res = []
        if self.flag.activate:
            self.end()
        self.load_objects()
        for i in range(len(self.loaded_objects)):
            for j in range(len(self.loaded_objects[i])):
                res.append([self.loaded_objects[i][j], (self.loaded_objects[i][j].get_position()[0] + i * 32 - 4 * 32 + int(self.camera_x // 32) * 32, self.loaded_objects[i][j].get_position()[1] + j * 32 - 16), self.loaded_objects[i][j].get_collision((i * 32 - 4 * 32 + int(self.camera_x // 32) * 32, j * 32 - 16))])
        return res

    def load_entities(self):
        new_pos = int(self.camera_x // 32)
        for entity in self.loaded_entities:
            if entity[0] <= new_pos * 32:
                self.loaded_entities.remove(entity)
            elif entity[0] >= new_pos * 32 + 17 * 32:
                self.loaded_entities.remove(entity)
        if new_pos != self.loaded_pos:
            for entity in self.entities:
                if entity[0] <= new_pos * 32 + 16 * 32 and not entity[2].loaded:
                    self.loaded_entities.append(entity)
            self.loaded_pos = new_pos

    def get_entities(self):
        res = []
        self.load_entities()
        for entity in self.loaded_entities:
            res.append((entity[2].get_position()[0], entity[2].get_position()[1], entity[2]))
        return res

    def load_backgrounds(self):
        new_pos = int(self.camera_x // 32)
        for background in self.loaded_backgrounds:
            if background[0] <= new_pos * 32 - 512:
                self.loaded_backgrounds.remove(background)
        if new_pos != self.loaded_pos:
            for background in self.backgrounds:
                if background[0] <= new_pos * 32 + 24 * 32 and not background[2].loaded:
                    self.loaded_backgrounds.append(background)

    def get_backgrounds(self):
        self.move_camera()
        self.load_backgrounds()
        return self.loaded_backgrounds

    def move_camera(self):
        if self.end_state == 0:
            if self.mario.x - 224 > self.camera_x:
                self.camera_x = self.mario.x - 224
            elif self.camera_x >= self.mario.x:
                self.mario.x = self.camera_x + 1
                self.mario.current_speed = Distance(0, 0, 0, 0, 0)
        elif self.end_state == 3:
            if self.mario.x - 264 > self.camera_x:
                self.camera_x = self.mario.x - 264
            elif self.camera_x >= self.mario.x - 40:
                self.mario.x = self.camera_x + 1
                self.mario.current_speed = Distance(0, 0, 0, 0, 0)

    def get_mario(self):
        return self.mario

    def export_l(self):
        f = open("level_data.txt", "w")
        for i in range(len(self.objects)):
            for j in range(len(self.objects[i])):
                if isinstance(self.objects[i][j], Block):
                    if (j >= 13 and self.objects[i][j].type == 0) or (j < 13 and self.objects[i][j].type == 1) or self.objects[i][j].type >= 2:
                        f.write(f'{i},{j},Block,{self.objects[i][j].type}\n')
                elif isinstance(self.objects[i][j], Pipe):
                    f.write(f'{i},{j},Pipe,{self.objects[i][j].type}\n')
                elif isinstance(self.objects[i][j], CoinBlock):
                    f.write(f'{i},{j},CoinBlock,{self.objects[i][j].contains}\n')

        f.write("ENTITY\n")

        for i in range(len(self.entities)):
            if isinstance(self.entities[i][2], Goomba):
                f.write(f'{self.entities[i][0]},{self.entities[i][1]},Goomba\n')
            elif isinstance(self.entities[i][2], Koopa):
                f.write(f'{self.entities[i][0]},{self.entities[i][1]},Koopa\n')

    def import_l(self):
        f = open("level_data.txt", "r")
        lines = f.readlines()
        state = 0
        for line in lines:
            line = line[:-1]
            data = line.split(",")
            if state == 0:
                if data[0] != "ENTITY":
                    if data[2] == "Block":
                        self.objects[int(data[0])][int(data[1])] = Block(int(data[3]))
                    elif data[2] == "Pipe":
                        self.objects[int(data[0])][int(data[1])] = Pipe(int(data[3]))
                    elif data[2] == "CoinBlock":
                        self.objects[int(data[0])][int(data[1])] = CoinBlock(data[3])
                else:
                    state = 1
            else:
                if data[2] == "Goomba":
                    self.entities.append((int(data[0]), int(data[1]), Goomba(int(data[0]), int(data[1]))))
                elif data[2] == "Koopa":
                    self.entities.append((int(data[0]), int(data[1]), Koopa(int(data[0]), int(data[1]))))
                elif data[2] == "Pole":
                    self.entities.append((int(data[0]), int(data[1]), Pole(int(data[0]), int(data[1]))))
                elif data[2] == "Flag":
                    self.flag = Flag(int(data[0]), int(data[1]))
                    self.entities.append((int(data[0]), int(data[1]), self.flag))

    def end(self):
        if self.end_state == 0:
            self.mario.end = True
            self.mario.state = 3
            self.mario.frame = 0
            self.mario.frametimer = 0
            self.mario.x += 8
            self.mario.set_speed(Distance(0, 0, 0, 0, 0))
            self.sounds[0].play()
            self.end_state += 1

        elif self.end_state == 1:
            if not self.mario.grounded:
                self.mario.jump_speed = Distance(0, -2, 0, 0, 0)
            else:
                self.mario.frame = 0
                self.mario.jump_speed = Distance(0, 0, 0, 0, 0)

            self.flag.y -= Distance(0, -2, 0, 0, 0).get_distance(5)
            if self.mario.jump_speed.get_distance(5) != 0:
                self.mario.frame = self.mario.frametimer // 5 % 2
                self.mario.frametimer += 1

            if self.flag.y >= 326:
                self.flag.y = 326
                self.end_state += 1
                self.mario.jump_speed = Distance(0, 0, 0, 0, 0)
                self.mario.x += 28
                self.mario.direction = 1
                self.mario.frame = 0

        elif self.end_state == 2:
            self.mario.jump_speed = Distance(0, 0, 0, 0, 0)
            self.timer -= 1
            if self.timer == 0:
                self.end_state += 1
                self.mario.direction = 0
                self.mario.state = 0
                self.mario.frame = 1
                self.mario.set_speed(Distance(0, 0, 13, 0, 0))
                self.sounds[1].play()

        elif self.end_state == 3:
            self.mario.frame = (self.mario.frametimer // 5 % 3) + 1
            self.mario.frametimer += 1
            if self.mario.x >= self.flag.x - 24 + 16 + 6 * 32:
                self.end_state += 1
                self.mario.set_speed(Distance(0, 0, 0, 0, 0))
                self.mario.state = 4
                self.mario.frame = 0
                self.timer = 400

        elif self.end_state == 4:
            self.timer -= 1
            if self.timer == 0:
                self.timer = 30
                self.end_state += 1

        elif self.end_state == 5:
            self.timer -= 1
            if self.timer == 0:
                self.timer = 10
                self.end_state += 1

        elif self.end_state == 6:
            self.timer -= 1
            if self.timer == 0:
                self.end_state += 1

    def get_state(self):
        self.next_to_block = False
        block_x = 0
        i = -1
        while self.mario.x > block_x:
            i += 1
            block_x = (self.loaded_pos + i - 4) * 32

        bottomless_near = False
        bottomless_distance = 128

        for k in range(5):
            if (isinstance(self.loaded_objects[i + k - 1][13], Block) and self.loaded_objects[i + k - 1][13].type == 0):
                bottomless_near = True
                bottomless_distance = (self.loaded_pos + (i + k - 1) - 4) * 32 - self.mario.x - 4
                if bottomless_distance < 0:
                    bottomless_distance = 0
                break

        if bottomless_distance == 0:
            self.bottomless_pit = True
        else:
            self.bottomless_pit = False

        block_y = 0
        j = -1
        while self.mario.y - 2 > block_y:
            j += 1
            block_y = j * 32 - 16

        if j > 14:
            j = 14

        for k in range(len(self.loaded_objects[i]) - j):
            if (isinstance(self.loaded_objects[i][j + k], Block) and self.loaded_objects[i][j + k].type != 0) or (not isinstance(self.loaded_objects[i][j + k], Block)):
                self.ground_distance = ((j + k) * 32 - 16) - (self.mario.y + 30)
                break

        ray_x = -1
        ray_type = 0

        pipe = False
        for k in range(9):
            if isinstance(self.loaded_objects[i][j], Block):
                if self.loaded_objects[i][j].type != 0:
                    ray_x = (self.loaded_pos + i - 4) * 32 - self.mario.x
                    break
            else:
                if isinstance(self.loaded_objects[i][j], Pipe):
                    pipe = True
                ray_x = (self.loaded_pos + i - 4) * 32 - self.mario.x
                break
            i += 1

        if ray_x != -1:
            ray_x -= 32
            if ray_x < 0:
                ray_x = 0
            ray_type = 1
        else:
            ray_x = 32 * 8

        if ray_x <= 32:
            self.next_to_block = True

        for entity in self.loaded_entities:
            if not isinstance(entity[2], Pole) and not isinstance(entity[2], Flag):
                if entity[2].x - self.mario.x - 32 < ray_x and 0 >= self.mario.y - entity[2].y >= -32 and not entity[2].dead and not isinstance(entity[2], ScoreNum) and not isinstance(entity[2], Coin):
                    ray_x = entity[2].x - self.mario.x - 32
                    ray_type = 2
                    ray_y = self.mario.y + 32 - entity[2].y

        if ray_type == 0:
            ray_y = 0
        elif ray_type == 1:
            while not isinstance(self.loaded_objects[i][j], Block) and self.loaded_objects[i][j] != 0:
                j -= 1
            ray_y = self.mario.y - ((j * 32) - 16)

        self.pipe_reward = 0
        if self.next_to_block and pipe and ray_x <= 16:
            self.pipe_reward = self.ground_distance / 4

        backwall_distance = self.mario.x - self.loaded_pos * 32

        state = [
            self.mario.current_speed.get_distance(5),
            self.mario.jump_speed.get_distance(5),

            self.mario.grounded,
            self.mario.y,
            self.ground_distance,

            ray_type,
            ray_x,
            ray_y,

            self.next_to_block,

            backwall_distance,

            bottomless_near,
            bottomless_distance
        ]

        return np.array(state)

    def get_rds(self, time):
        global bottomless_deaths
        global game_won
        global goomba_deaths
        game_over = False
        backwall_distance = self.mario.x - self.loaded_pos * 32
        reward = (backwall_distance - self.init_backwall) / 5
        if reward > 0:
            reward = 0

        # if self.pipe_reward > 0:
        #     reward = -self.pipe_reward

        if self.mario.x > self.max_x:
            reward = (self.mario.x - self.max_x) * 10
            self.max_x = self.mario.x

        if self.old_score < self.mario.score:
            reward = 100
            self.old_score = self.mario.score

        if game_won:
            if self.bottomless_pit:
                reward = 400 - self.mario.y
                if reward <= 0:
                    reward *= 1 + (0.25 * bottomless_deaths)
            if 4412 <= self.mario.x <= 4452:
                reward = (400 - self.mario.y - (32 * 5)) / 2

        if self.mario.is_dead and time > 0:
            reward = -1000
            if game_won:
                if self.mario.y >= 448:
                    bottomless_deaths += 1
                else:
                    bottomless_deaths = 0
            if self.mario.x <= 651:
                reward = -1000 - (50 * goomba_deaths)
                goomba_deaths += 1
            else:
                goomba_deaths = 0
            game_over = True
        elif self.mario.is_dead:
            bottomless_deaths = 0
            goomba_deaths = 0
            game_over = True

        if self.end_state == 7:
            game_won = True
            game_over = True

        print(reward)

        return reward, game_over, self.mario.score
