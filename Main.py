import pygame
from python.Mario import Mario
from python.Distance import Distance

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((512, 448))
pygame.display.set_caption("Super Mario Bros.")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/1-1.png').convert()
bg_x = 0
bg_music = pygame.mixer.Sound('sounds/1-1.wav')
bg_music.play(loops=99)

myfont = pygame.font.Font('font/font.ttf', 16)
text_mario = myfont.render('MARIO', False, 'White')
text_coins_x = myfont.render('×', False, 'White')
text_coins_num = myfont.render('00', False, 'White')
frames = 0

mario: Mario = Mario()

running = True
while running:

    text_frames = myfont.render(str(frames), False, 'White')
    text_speed = myfont.render(str(mario.current_speed.get_blocks()) + "\n" + str(mario.current_speed.get_pixels()) + "\n" + str(mario.current_speed.get_subpixels()) + "\n" + str(mario.current_speed.get_subsubpixels()) + "\n" + str(mario.current_speed.get_subsubsubpixels()), False, "White")
    text_max_speed = myfont.render(str(mario.max_speed.get_blocks()) + "\n" + str(mario.max_speed.get_pixels()) + "\n" + str(mario.max_speed.get_subpixels()) + "\n" + str(mario.max_speed.get_subsubpixels()) + "\n" + str(mario.max_speed.get_subsubsubpixels()), False, "White")

    screen.blit(bg, (bg_x, -16))
    screen.blit(mario.get_sprite(), mario.get_position())
    screen.blit(text_frames, (300, 300))
    screen.blit(text_speed, (150, 150))
    screen.blit(text_max_speed, (150, 128))

    pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        mario.run_right()
    elif keys[pygame.K_LEFT]:
        mario.run_left()
    else:
        mario.stand()

    if keys[pygame.K_SPACE]:
        mario.jump(1)
    elif mario.is_jump:
        mario.jump(0)

    if keys[pygame.K_LSHIFT]:
        mario.fast_run()
    elif mario.is_fastrunning():
        mario.slow_run()

    if mario.get_position()[0] >= 224 and mario.get_speed() > 0:
        bg_x -= mario.get_speed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    frames += 1

    clock.tick(60)
