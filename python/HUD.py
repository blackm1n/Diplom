import pygame

from python.LevelMario import Mario


class HUD:

    time: int
    timer: int
    score: int
    coins: int
    coin: []
    frame = int
    texts: []
    sounds: []
    end_time: int

    def __init__(self):
        self.time = 400
        self.timer = 0
        self.score = 0
        self.coins = 0
        self.texts = [
            (48, 14, "MARIO"),
            (48, 30, "000000"),
            (192, 32, "×"),
            (208, 30, "00"),
            (288, 14, "WORLD"),
            (304, 30, "1-1"),
            (400, 14, "TIME"),
            (416, 30, "400")
        ]
        self.coin = [
            pygame.image.load('images/coin/coin_1.png').convert_alpha(),
            pygame.image.load('images/coin/coin_2.png').convert_alpha(),
            pygame.image.load('images/coin/coin_3.png').convert_alpha(),
            pygame.image.load('images/coin/coin_2.png').convert_alpha(),
            pygame.image.load('images/coin/coin_1.png').convert_alpha()
        ]
        self.frame = -1
        self.sounds = [
            pygame.mixer.Sound('sounds/blip.mp3')
        ]
        self.end_time = self.time

    def update(self, mario: Mario, end_state: int):
        self.texts[1] = (self.texts[1][0], self.texts[1][1], "0" * (6 - len(str(mario.score))) + str(mario.score))
        self.score = mario.score
        self.texts[3] = (self.texts[3][0], self.texts[3][1], "0" * (2 - len(str(mario.coins))) + str(mario.coins))
        self.coins = mario.coins
        if end_state == 0:
            if self.timer % 24 == 0 and not mario.is_dead:
                self.time -= 1
            elif self.time < 0:
                self.time = 0
                mario.die()
            self.timer += 1
            self.texts[-1] = (self.texts[-1][0], self.texts[-1][1], "0" * (3 - len(str(self.time))) + str(self.time))

    def countdown(self):
        if self.time > 0:
            self.time -= 1
            self.score += 50
            self.sounds[0].play()
        self.texts[1] = (self.texts[1][0], self.texts[1][1], "0" * (6 - len(str(self.score))) + str(self.score))
        self.texts[-1] = (self.texts[-1][0], self.texts[-1][1], "0" * (3 - len(str(self.time))) + str(self.time))

    def get_texts(self, mario: Mario, end_state: int):
        if end_state == 0 or end_state == 1:
            self.update(mario, end_state)
            self.end_time = self.time
        elif end_state == 4:
            self.countdown()
        return self.texts

    def get_coin(self):
        if self.frame < 49:
            self.frame += 1
        else:
            self.frame = 0
        return 176, 32, self.coin[self.frame // 10]



