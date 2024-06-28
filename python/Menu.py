import pygame

from python.HUD import HUD
from python.Level import Level


class Menu:

    level: Level
    hud: HUD
    sprites: []
    text: []
    font: pygame.font.Font
    cursor: tuple
    game: int

    def __init__(self):
        self.level: Level = Level(24, 0, False)
        self.hud: HUD = HUD()
        self.sprites = [
            pygame.image.load('images/title.png').convert_alpha(),
            pygame.image.load('images/cursor.png').convert_alpha()
        ]
        self.text = [
            (112, 222, "©2023 СЕРГЕЙ ЛЮБИМОВ"),
            (176, 270, "HUMAN PLAYER GAME"),
            (176, 302, "AI PLAYER GAME")
        ]
        self.font = pygame.font.Font('font/font.ttf', 16)
        self.cursor = (self.sprites[1], (144, 272))
        self.game = 0

    def render(self, keys):
        if keys[pygame.K_UP]:
            self.cursor = (self.sprites[1], (144, 272))
        elif keys[pygame.K_DOWN]:
            self.cursor = (self.sprites[1], (144, 304))

        if keys[pygame.K_RETURN]:
            if self.cursor[1] == (144, 272):
                self.game = 1
            else:
                self.game = 2

    def get_sprites(self):
        res = []
        backgrounds = self.level.get_backgrounds()
        for background in backgrounds:
            res.append((background[2].get_sprite(), (background[0], background[1])))
        objects = self.level.get_objects()
        for object in objects:
            res.append((object[0].get_sprite(), object[1]))
        mario = self.level.get_mario()
        res.append((mario.get_sprite(), mario.get_position()))
        self.hud.time = 400
        text_hud = self.hud.get_texts(mario, self.level.end_state)
        for i in range(len(text_hud) - 1):
            res.append((self.font.render(text_hud[i][2], False, "White"), (text_hud[i][0], text_hud[i][1])))
        coin = self.hud.get_coin()
        res.append((coin[2], (coin[0], coin[1])))
        res.append((self.sprites[0], (80, 48)))
        for i in range(len(self.text)):
            if i == 0:
                res.append((self.font.render(self.text[i][2], False, (255, 206, 197)), (self.text[i][0], self.text[i][1])))
            else:
                res.append((self.font.render(self.text[i][2], False, "White"), (self.text[i][0], self.text[i][1])))
        res.append(self.cursor)
        return res