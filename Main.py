import pygame

from python.Menu import Menu
from python.HUD import HUD
from python.Level import Level
from python.CollisionHandler import CollisionHandler
from python.agent import Agent

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((512, 448))
pygame.display.set_caption("Super Mario Bros.")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

myfont = pygame.font.Font('font/font.ttf', 16)

hud: HUD = HUD()

bg = pygame.image.load('images/bg.png').convert()
bg_music = pygame.mixer.Sound('sounds/1-1.mp3')
bg_music_played = False

game_over_music = pygame.mixer.Sound('sounds/smb_gameover.wav')
game_over_music_played = False

menu: Menu = Menu()
menu_state = 0

max_score = 0

finished_games = 0

with open('stats.csv', 'r') as file:
    lines = file.readlines()
    if not lines[-1][0].isalpha():
        games = int(lines[-1].split(";")[0])
    else:
        games = 0

running = True
while running:

    if menu_state == 0:

        ai = False

        sprites = menu.get_sprites()
        screen.blit(bg, (0, 0))
        for sprite in sprites:
            screen.blit(sprite[0], sprite[1])

        pygame.display.update()

        keys = pygame.key.get_pressed()

        menu.render(keys)

        bg_music_played = False

        if menu.game == 1:
            menu_state = 1
        elif menu.game == 2:
            menu_state = 1
            agent = Agent()
            agent.load()
            ai = True

    elif menu_state == 1:

        if not bg_music_played:
            game_over_timer = 0
            game_over_music_played = False
            screen.fill((0, 0, 0))
            loading = myfont.render("Loading...", False, "White")
            screen.blit(loading, (175, 225))
            pygame.display.update()
            level: Level = Level(227, 1, ai)
            collision_handler: CollisionHandler = CollisionHandler()
            hud.time = 400
            hud.timer = 0
            games += 1

        backgrounds = level.get_backgrounds()
        objects = level.get_objects()
        entities = level.get_entities()
        mario = level.get_mario()
        texts = hud.get_texts(mario, level.end_state)

        screen.blit(bg, (0, 0))

        for background in backgrounds:
            screen.blit(background[2].get_sprite(), (background[0] - level.camera_x, background[1]))

        for object in objects:
            screen.blit(object[0].get_sprite(), (object[1][0] - level.camera_x, object[1][1]))

        for entity in entities:
            entity[2].render()
            screen.blit(entity[2].get_sprite(), (entity[0] - level.camera_x, entity[1]))

        for text in texts:
            screen.blit(myfont.render(text[2], False, "White"), (text[0], text[1]))
        coin = hud.get_coin()
        screen.blit(coin[2], (coin[0], coin[1]))

        if not ai:
            final_move = pygame.key.get_pressed()
        else:
            state_old = level.get_state()
            final_move = agent.get_action(state_old)

        mario.render(final_move)

        if mario.end:
            bg_music.stop()

        collision_handler.handle(mario, objects, entities)

        level.loaded_entities = entities

        screen.blit(mario.get_sprite(), (mario.get_position()[0] - level.camera_x, mario.get_position()[1]))


        if not bg_music_played:
            bg_music_played = True
            bg_music.play(99)

        if not ai:
            if level.end_state == 6:
                screen.fill((0, 0, 0))
            elif level.end_state == 7:
                menu.game = 0
                menu_state = 0

        pygame.display.update()

        if ai:
            reward, done, score = level.get_rds(hud.time)
            state_new = level.get_state()
            if level.end_state == 0:
                agent.train_short_memory(state_old, final_move, reward, state_new, done)
                agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                agent.n_game += 1
                agent.train_long_memory()
                agent.model.save('model.pth')

                bg_music.stop()
                bg_music_played = False
                if level.end_state == 7:
                    finished_games += 1
                    agent.model.save('finished7.1\\game_'+str(finished_games)+'.pth')
                    with open('stats.csv', 'a') as file:
                        file.write("\n"+str(games)+";"+str(hud.score)+";"+str(hud.end_time)+";"+str(mario.x)+";Win")
                else:
                    cause_of_end = "Enemy"
                    if hud.time == 0:
                        cause_of_end = "Time"
                    elif mario.y >= 448:
                        cause_of_end = "Fall"

                    with open('stats.csv', 'a') as file:
                        file.write("\n"+str(games)+";"+str(hud.score)+";"+str(hud.time)+";"+str(mario.x)+";"+cause_of_end)

        if mario.is_dead:
            if not ai:
                game_over_timer += 1
                if game_over_timer >= 240:
                    menu_state = 2
                bg_music.stop()

    elif menu_state == 2:

        if not game_over_music_played:
            menu.game = 0
            game_over_music.play()
            game_over_music_played = True

        game_over_timer += 1
        screen.fill((0, 0, 0))
        game_over = myfont.render("GAME OVER", False, "White")
        screen.blit(game_over, (175, 225))
        pygame.display.update()

        if game_over_timer >= 480:
            menu_state = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # level.export()
            running = False
            pygame.quit()

    if not ai:
        clock.tick(60)
    else:
        clock.tick(180)
