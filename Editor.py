import pygame

from Block import Block
from CoinBlock import CoinBlock
from Goomba import Goomba
from Koopa import Koopa
from Pipe import Pipe
from python.Level import Level

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((512, 448))
pygame.display.set_caption("Super Mario Bros.")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

myfont = pygame.font.Font('font/font.ttf', 16)

bg = pygame.image.load('images/bg.png').convert()
level1_1 = pygame.image.load('images/1-1.png').convert_alpha()

bg_music = pygame.mixer.Sound('sounds/1-1.wav')

square = pygame.Surface((32, 32))
square.fill((255, 255, 255))
x = 0
y = 16

speed = 32

level: Level = Level(227, 1)

running = True
while running:

    objects = level.get_objects()
    entities = level.get_entities()

    screen.blit(bg, (0, 0))

    screen.blit(square, (x - level.camera_x, y))

    for object in objects:
        screen.blit(object[0].get_sprite(), (object[1][0] - level.camera_x, object[1][1]))

    for entity in entities:
        screen.blit(entity[2].get_sprite(), (entity[0] - level.camera_x, entity[1]))

    screen.blit(level1_1, (-level.camera_x, -16))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LSHIFT]:
        speed = 16
    else:
        speed = 32

    if keys[pygame.K_RIGHT]:
        x += speed
    elif keys[pygame.K_LEFT]:
        x -= speed
    elif keys[pygame.K_DOWN]:
        y += speed
    elif keys[pygame.K_UP]:
        y -= speed

    if keys[pygame.K_1]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Block(0)
    if keys[pygame.K_2]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Block(1)
    if keys[pygame.K_3]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Block(2)
    if keys[pygame.K_4]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Block(3)
    if keys[pygame.K_5]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Pipe(0)
    if keys[pygame.K_6]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = Pipe(1)
    if keys[pygame.K_7]:
        level.objects[(x + 4 * 32) // 32][(y + 16) // 32] = CoinBlock("Coin")
    if keys[pygame.K_8]:
        level.entities.append((x, y + 2, Goomba(x, y + 2)))
    if keys[pygame.K_9]:
        level.entities.append((x, y + 2, Koopa(x, y + 2)))

    if x > level.camera_x + 480:
        level.camera_x += 32

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.export_l()
            running = False
            pygame.quit()

    clock.tick(10)
