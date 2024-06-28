import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((512, 448))
pygame.display.set_caption("Super Mario Bros.")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

square = pygame.Surface((512, 48))
square.fill((156, 76, 0))

myfont = pygame.font.Font('font/font.ttf', 16)
text_mario = myfont.render('MARIO', False, 'White')
text_coins_x = myfont.render('×', False, 'White')
text_coins_num = myfont.render('00', False, 'White')

title = pygame.image.load('images/title.png').convert_alpha()
mario = [
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

goomba = [
    pygame.image.load('images/entities/goomba/goomba_1.png').convert_alpha(),
    pygame.image.load('images/entities/goomba/goomba_2.png').convert_alpha(),
    pygame.image.load('images/entities/goomba/goomba_dead.png').convert_alpha()
]
goomba_anim_count = 0
goomba_x = 620

bg = pygame.image.load('images/1-1.png').convert()
print(type(bg))
bg_x = 0
bg_music = pygame.mixer.Sound('sounds/1-1.mp3')
bg_music.play()

coin = [
    pygame.image.load('images/coin/coin_1.png').convert_alpha(),
    pygame.image.load('images/coin/coin_2.png').convert_alpha(),
    pygame.image.load('images/coin/coin_3.png').convert_alpha(),
    pygame.image.load('images/coin/coin_2.png').convert_alpha(),
    pygame.image.load('images/coin/coin_1.png').convert_alpha()
]

coin_anim_count = 0

player_anim_count = 0
player_state = 0
max_player_speed = 5
current_player_speed = 0
player_x = 84
player_y = 370
player_jump = pygame.mixer.Sound('sounds/smb_jump-small.wav')
last_direction = 0
player_die = pygame.mixer.Sound('sounds/smb_mariodie.wav')
print(type(player_die))
player_isDead = False

stomp = pygame.mixer.Sound('sounds/smb_stomp.wav')

is_jump = False
jump_count = 7

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    #screen.blit(square, (0, 400))
    screen.blit(text_mario, (48, 14))
    screen.blit(text_coins_x, (192, 32))
    screen.blit(text_coins_num, (208, 30))
    screen.blit(coin[coin_anim_count], (176, 32))
    #screen.blit(title, (80, 48))
    screen.blit(mario[player_state][player_anim_count], (player_x, player_y))
    screen.blit(goomba[goomba_anim_count], (goomba_x + bg_x, 370))

    player_rect = mario[0][0].get_rect(topleft=(player_x, player_y))
    if goomba_anim_count < 2:
        goomba_rect = goomba[0].get_rect(topleft=(goomba_x + bg_x, 370))


    keys = pygame.key.get_pressed()
    if player_isDead:
        player_state = 3
        player_anim_count = 0
        if jump_count > -7:
            player_y -= (jump_count ** 2) / 2
        else:
            player_y += (jump_count ** 2) / 2
        jump_count -= 1
    else:
        if player_rect.colliderect(goomba_rect):
            if is_jump:
                goomba_rect = goomba[0].get_rect(topleft=(0, 0))
                stomp.play()
                goomba_anim_count = 2
                jump_count = 6
                if jump_count >= -7:
                    if jump_count > -5:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
            else:
                player_die.play()
                bg_music.stop()
                player_isDead = True

        if keys[pygame.K_RIGHT] and player_x < 224:
            player_state = 0
            if current_player_speed < max_player_speed:
                current_player_speed += 1
            elif current_player_speed > max_player_speed:
                current_player_speed -= 1
            player_x += current_player_speed
            if current_player_speed < 0:
                player_anim_count = 4
            else:
                if player_anim_count >= 3:
                    player_anim_count = 1
                else:
                    player_anim_count += 1
        elif keys[pygame.K_RIGHT]:
            player_state = 0
            if current_player_speed < max_player_speed:
                current_player_speed += 1
            elif current_player_speed > max_player_speed:
                current_player_speed -= 1
            bg_x -= current_player_speed
            if current_player_speed < 0:
                player_anim_count = 4
            else:
                if player_anim_count >= 3:
                    player_anim_count = 1
                else:
                    player_anim_count += 1
        elif keys[pygame.K_LEFT] and player_x > 224 and current_player_speed > 0:
            player_state = 1
            if current_player_speed > -max_player_speed:
                current_player_speed -= 1
            elif current_player_speed < max_player_speed:
                current_player_speed += 1
            bg_x -= current_player_speed
            if current_player_speed > 0:
                player_anim_count = 4
            else:
                if player_anim_count >= 3:
                    player_anim_count = 1
                else:
                    player_anim_count += 1
        elif keys[pygame.K_LEFT] and player_x > 0:
            player_state = 1
            if current_player_speed > -max_player_speed:
                current_player_speed -= 1
            elif current_player_speed < max_player_speed:
                current_player_speed += 1
            player_x += current_player_speed
            if current_player_speed > 0:
                player_anim_count = 4
            else:
                if player_anim_count >= 3:
                    player_anim_count = 1
                else:
                    player_anim_count += 1
        else:
            if current_player_speed > 0:
                current_player_speed -= 1
            elif current_player_speed < 0:
                current_player_speed += 1
            player_anim_count = 0

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                player_jump.play()
                last_direction = player_state
        else:
            player_anim_count = last_direction
            player_state = 2
            if jump_count >= -7:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                player_anim_count = 0
                player_state = last_direction
                jump_count = 7

        if keys[pygame.K_LSHIFT]:
            max_player_speed = 10
        else:
            max_player_speed = 5

    if coin_anim_count == 4:
        coin_anim_count = 0
    else:
        coin_anim_count += 1

    if goomba_anim_count < 2:
        goomba_x -= 2

    if goomba_anim_count == 1:
        goomba_anim_count = 0
    elif goomba_anim_count == 0:
        goomba_anim_count += 1

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(30)
