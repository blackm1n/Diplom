import pygame

from Block import Block
from Coin import Coin
from CoinBlock import CoinBlock
from Flag import Flag
from Koopa import Koopa
from LevelMario import Mario
from Distance import Distance
from Pole import Pole
from ScoreNum import ScoreNum


class CollisionHandler:

    activate: bool

    def __init__(self):
        self.activate = False

    def handle(self, mario: Mario, objects: [], entities: []):
        mario.grounded = False
        for object in objects:
            if object[2] is not None:
                if not mario.is_dead:
                    if mario.collision.colliderect(object[2]) and ((mario.y <= object[2][1] - 16 and mario.jump_speed.get_distance(5) <= Distance(0, -4, 0, 0, 0).get_distance(5)) or (mario.y <= object[2][1] - 22 and mario.jump_speed.get_distance(5) <= Distance(0, -1, 0, 0, 0).get_distance(5)) or mario.y <= object[2][1] - 28) and mario.x + 28 >= object[2][0] >= mario.x - (28 - 32 + object[2][2]):
                        if object[0].disguise != 2 or object[0].state == 1:
                            mario.jump_speed = Distance(0, 0, 0, 0, 0)
                            mario.grounded = True
                            mario.combo = 0
                            mario.y = object[2][1] - 30
                    elif mario.collision.colliderect(object[2]) and ((mario.y >= object[2][1] + 16 and mario.jump_speed.get_distance(5) >= Distance(0, 2, 0, 0, 0).get_distance(5)) or (mario.y >= object[2][1] + 24 and mario.jump_speed.get_distance(5) > Distance(0, 0, 0, 0, 0).get_distance(5))) and mario.x + 16 >= object[2][0] >= mario.x - 16:
                        mario.jump_speed = Distance(0, 0, 0, 0, 0)
                        mario.y = object[2][1] + 32
                        if isinstance(object[0], CoinBlock) and object[0].state == 0 and (object[0].contains == "Coin" or object[0].contains == "Hidden_Coin" or object[0].contains == "Invisible_Coin"):
                            mario.coins += 1
                            mario.score += 200
                            entities.append((object[2][0] + 8, object[2][1] - 48, Coin(object[2][0] + 8, object[2][1] - 48)))
                            entities.append((object[2][0] + 8, object[2][1] - 48, ScoreNum(object[2][0] + 8, object[2][1] - 48, 2, 30)))
                        jump = 0
                        if isinstance(object[0], CoinBlock):
                            if object[0].state == 0:
                                jump = 1
                        if isinstance(object[0], Block):
                            if object[0].type == 2:
                                jump = 1
                        if jump:
                            for entity in entities:
                                if entity[2].get_collision() is not None and not isinstance(entity[2], Pole):
                                    if entity[2].get_collision().colliderect(object[2]) and entity[2].y <= object[2][1] - 16:
                                        mario.combo += 1
                                        mario.score += mario.combo_list[mario.combo]
                                        entity[2].die(1)
                                        entities.append((entity[2].x + 8, entity[2].y - 8, ScoreNum(entity[2].x + 8, entity[2].y - 8, mario.combo, 0)))
                        object[0].hit()
                    elif mario.collision.colliderect(object[2]) and mario.y + 24 >= object[2][1] >= mario.y - 24:
                        if object[0].disguise != 2 or object[0].state == 1:
                            if mario.x <= object[2][0] + 8 and mario.current_speed.get_distance(5) >= 0:
                                mario.x = object[2][0] - 32
                                mario.current_speed = Distance(0, 0, 0, 0, 0)
                            elif mario.x >= object[2][0] - 8 and mario.current_speed.get_distance(5) <= 0:
                                mario.x = object[2][0] + object[2][2]
                                mario.current_speed = Distance(0, 0, 0, 0, 0)

        for entity in entities:
            if not isinstance(entity[2], Pole) and not isinstance(entity[2], Flag) and not entity[2].dead:
                if entity[2].get_collision() is not None:
                    if not mario.is_dead:
                        if mario.collision.colliderect(entity[2].get_collision()) and mario.jump_speed.get_distance(5) >= 0:
                            if mario.bounce_timer == 0:
                                mario.die()
                        elif mario.collision.colliderect(entity[2].get_collision()):
                            mario.jump_speed.set_pixels(4)
                            mario.is_jump = False
                            mario.combo += 1
                            mario.score += mario.combo_list[mario.combo]
                            entity[2].die(0)
                            entities.append((entity[2].x + 8, entity[2].y - 8, ScoreNum(entity[2].x + 8, entity[2].y - 8, mario.combo, 0)))
                            mario.bounce_timer = 5

                entity[2].grounded = False
                if entity[2].get_collision() is not None:
                    for object in objects:
                        if object[2] is not None:
                            if entity[2].get_collision().colliderect(object[2]) and entity[2].y <= object[2][1] - 16 and entity[2].y_speed.get_distance(5) <= 0:
                                entity[2].grounded = True
                                entity[2].y = object[2][1] - 30
                            elif entity[2].get_collision().colliderect(object[2]) and entity[2].y_speed.get_distance(5) <= 0:
                                if entity[2].x <= object[2][0] + 16:
                                    entity[2].x = object[2][0] - 32
                                else:
                                    entity[2].x = object[2][0] + object[2][2]
                                entity[2].x_speed = entity[2].x_speed.reverse()
                    for entity2 in entities:
                        if entity != entity2 and not isinstance(entity2[2], Pole) and not isinstance(entity[2], Flag):
                            if entity2[2].get_collision() is not None and entity[2].get_collision() is not None:
                                if entity[2].get_collision().colliderect(entity2[2].get_collision()):
                                    if isinstance(entity2[2], Koopa) and entity2[2].dead:
                                        entity2[2].combo += 1
                                        mario.score += entity2[2].combo_list[entity2[2].combo]
                                        entity[2].die(1)
                                        entities.append((entity[2].x + 8, entity[2].y - 8, ScoreNum(entity[2].x + 8, entity[2].y - 8, entity2[2].combo + 3, 0)))
                                    else:
                                        if entity[2].x <= entity2[2].x + 16:
                                            entity[2].x = entity2[2].x - 32
                                        else:
                                            entity[2].x = entity2[2].x + 32
                                        entity[2].x_speed = entity[2].x_speed.reverse()
            elif not isinstance(entity[2], Pole) and not isinstance(entity[2], Flag):
                if entity[2].get_collision() is not None:
                    if not mario.is_dead:
                        if mario.collision.colliderect(entity[2].get_collision()) and mario.jump_speed.get_distance(5) >= 0 and entity[2].x_speed.get_distance(5) != 0 and entity[2].kicktime == 0:
                            mario.die()
                        elif mario.collision.colliderect(entity[2].get_collision()) and entity[2].x_speed.get_distance(5) != 0 and entity[2].kicktime == 0:
                            mario.jump_speed.set_pixels(4)
                            mario.is_jump = False
                            mario.combo += 1
                            mario.score += mario.combo_list[mario.combo]
                            entity[2].x_speed = Distance(0, 0, 0, 0, 0)
                            entities.append((entity[2].x + 8, entity[2].y - 8, ScoreNum(entity[2].x + 8, entity[2].y - 8, mario.combo, 0)))
                            entity[2].sounds[1].play()
                            entity[2].kicktime = 5
                        elif mario.collision.colliderect(entity[2].get_collision()) and entity[2].kicktime == 0:
                            if mario.jump_speed.get_distance(5) < 0:
                                mario.jump_speed.set_pixels(4)
                                mario.is_jump = False
                            mario.score += mario.combo_list[3]
                            entities.append((entity[2].x + 8, entity[2].y - 8, ScoreNum(entity[2].x + 8, entity[2].y - 8, 3, 0)))
                            if mario.x <= entity[2].x - 16:
                                entity[2].x_speed = Distance(0, 3, 0, 0, 0)
                            else:
                                entity[2].x_speed = Distance(0, -3, 0, 0, 0)
                            entity[2].kicktime = 5
                            entity[2].sounds[1].play()

                    entity[2].grounded = False
                    for object in objects:
                        if object[2] is not None:
                            if entity[2].get_collision().colliderect(object[2]) and entity[2].y <= object[2][1] - 16 and entity[2].y_speed.get_distance(5) <= 0:
                                entity[2].grounded = True
                                entity[2].y = object[2][1] - 30
                            elif entity[2].get_collision().colliderect(object[2]) and entity[2].y_speed.get_distance(5) <= 0:
                                if entity[2].x <= object[2][0] + 16:
                                    entity[2].x = object[2][0] - 32
                                else:
                                    entity[2].x = object[2][0] + object[2][2]
                                entity[2].x_speed = entity[2].x_speed.reverse()
            elif isinstance(entity[2], Pole):
                if mario.collision.colliderect(entity[2].get_collision()):
                    if self.activate == False:
                        if mario.y >= 308:
                            mario.score += 100
                            entities.append((entity[2].x + 16, mario.y - 8, ScoreNum(entity[2].x + 16, mario.y - 8, 1, 0)))
                        elif mario.y >= 248:
                            mario.score += 400
                            entities.append((entity[2].x + 16, mario.y - 8, ScoreNum(entity[2].x + 16, mario.y - 8, 3, 0)))
                        elif mario.y >= 188:
                            mario.score += 800
                            entities.append((entity[2].x + 16, mario.y - 8, ScoreNum(entity[2].x + 16, mario.y - 8, 5, 0)))
                        elif mario.y >= 128:
                            mario.score += 2000
                            entities.append((entity[2].x + 16, mario.y - 8, ScoreNum(entity[2].x + 16, mario.y - 8, 7, 0)))
                        else:
                            mario.score += 5000
                            entities.append((entity[2].x + 16, mario.y - 8, ScoreNum(entity[2].x + 16, mario.y - 8, 9, 0)))
                    self.activate = True
            elif isinstance(entity[2], Flag):
                if self.activate:
                    entity[2].activate = True



