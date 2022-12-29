import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()

pygame.init()

clock_rate = pygame.time.Clock()


# colors
RED = (255, 0, 0)
BLOOD_RED = (228, 27, 23)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# game variables
game_start_count = 4
latest_count = pygame.time.get_ticks()
score = [0, 0]  # [fighter1, fighter2]
round_over = False
pause = False
ROUND_OVER_RESET = 3000
ko_song_play = False

# fighter variables
FIGHTER1_SIZE_X = 200
FIGHTER1_SIZE_Y = 202
FIGHTER1_SCALE = 5  # Because actual size is tiny
FIGHTER1_OFFSET = [90, 87.5]  # Because scale korle position theke shore jay
FIGHTER1_DATA = [FIGHTER1_SIZE_X, FIGHTER1_SIZE_Y,
                 FIGHTER1_SCALE, FIGHTER1_OFFSET]

FIGHTER2_SIZE_X = 250
FIGHTER2_SIZE_Y = 250
FIGHTER2_SCALE = 4
FIGHTER2_OFFSET = [113, 122]
FIGHTER2_DATA = [FIGHTER2_SIZE_X, FIGHTER2_SIZE_Y,
                 FIGHTER2_SCALE, FIGHTER2_OFFSET]

#bgm and sfx
pygame.mixer.music.load("resources/audio/fight.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 3000)
sword_fx = pygame.mixer.Sound("resources/audio/sword.wav")
sword_fx.set_volume(0.1)
magic_fx = pygame.mixer.Sound("resources/audio/magic.wav")
magic_fx.set_volume(0.1)
ko_fx = pygame.mixer.Sound("resources/audio/CUET.wav")
ko_fx.set_volume(0.1)

# Game window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Demon Slayer")
# Loading bg image
bg_maps = pygame.image.load(
    "resources/images/background/background3.jpg").convert_alpha()

# Loading Spritesheets
fighter1_sheet = pygame.image.load(
    "resources/images/characters/raiden/Sprites/Raiden.png")
fighter2_sheet = pygame.image.load(
    "resources/images/characters/fighter2/Sprites/wizard.png")

# KO image
ko_image = pygame.image.load("resources/images/icons/ko.png").convert_alpha()

# Number of steps in each animation
FIGHTER1_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
FIGHTER2_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# font
count_font = pygame.font.Font("resources/fonts/Khatulistiwa Demo.ttf", 200)
score_font = pygame.font.Font("resources/fonts/Khatulistiwa Demo.ttf", 30)
title_font = pygame.font.Font(
    "resources/fonts/Slaughter.ttf", 30, bold=pygame.font.Font.bold)
pause_font = pygame.font.Font(
    "resources/fonts/Slaughter.ttf", 200, bold=pygame.font.Font.bold)
resume_font = pygame.font.Font(
    "resources/fonts/Slaughter.ttf", 32, bold=pygame.font.Font.bold)


# show text
def show_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Background maps
def show_bg():
    scaled_bg = pygame.transform.scale(bg_maps, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for showing hp


def show_hp(health, x, y):
    ratio = health / 100  # percentage akare kombe every hit e
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))


# Fighters
fighter_1 = Fighter(1, 200, 500, False, FIGHTER1_DATA,
                    fighter1_sheet, FIGHTER1_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 900, 500, True, FIGHTER2_DATA,
                    fighter2_sheet, FIGHTER2_ANIMATION_STEPS, magic_fx)

# MAIN CODE
# game loop to run continuously
run = True
while run:

    clock_rate.tick(60)  # 60 fps er game
    show_bg()  # Show background
    key = pygame.key.get_pressed()

    if pause == True:
        show_text("PAUSED", pause_font, BLOOD_RED,
                  250, 200)
        show_text("Press ENTER to resume", resume_font, WHITE, 417, 467)
    # Show fighters
    fighter_1.show(screen)
    fighter_2.show(screen)

    # check for game over
    if round_over == False:
        ko_song_play = False
        if key[pygame.K_ESCAPE] and game_start_count == 0:
            pause = True  # game pause
        elif key[pygame.K_RETURN]:
            pause = False  # resume
        elif fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            print(score)
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:

        # show KO image
        screen.blit(ko_image, (360, 150))
        pygame.mixer.music.stop()
        if ko_song_play == False:
            ko_fx.play()
            ko_song_play = True

        # Game over howar 1.5s por ENTER press korte bolbe, ENTER press korle game restart hobe
        if pygame.time.get_ticks() - round_over_time > 1500:
            show_text("Press  ENTER  for new game",
                      title_font, WHITE, 400, 570)

            if key[pygame.K_RETURN]:
                ko_fx.stop()
                pygame.mixer.music.play()
                round_over = False
                game_start_count = 4
                fighter_1 = Fighter(1, 200, 500, False, FIGHTER1_DATA,
                                    fighter1_sheet, FIGHTER1_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 900, 500, True, FIGHTER2_DATA,
                                    fighter2_sheet, FIGHTER2_ANIMATION_STEPS, magic_fx)
        # pygame.time.get_ticks() - round_over_time > ROUND_OVER_RESET:

   # show player hp
    show_hp(fighter_1.health, 20, 40)
    show_hp(fighter_2.health, 780, 40)
    show_text("Raiden", score_font, RED, 20, 10)
    show_text("Wizard", score_font, RED, 780, 10)
    show_text("hp: "+str(fighter_1.health), score_font, RED, 20, 70)
    show_text("Win: "+str(score[0]), score_font, RED, 19, 95)
    show_text("hp: "+str(fighter_2.health), score_font, RED, 780, 70)
    show_text("Win: "+str(score[1]), score_font, RED, 779, 95)

    # update countdown
    if game_start_count <= 0:
        # Fighter Movement
        fighter_1.movement(WINDOW_WIDTH, WINDOW_HEIGHT,
                           fighter_2, round_over, pause)
        fighter_2.movement(WINDOW_WIDTH, WINDOW_HEIGHT,
                           fighter_1, round_over, pause)
    else:
        # show game intro count
        show_text(str(game_start_count), count_font, BLOOD_RED,
                  WINDOW_WIDTH / 2.15, WINDOW_HEIGHT / 3)
        # update intro count
        if (pygame.time.get_ticks() - latest_count) >= 1000:
            game_start_count -= 1
            latest_count = pygame.time.get_ticks()

    # update fighter animation
    fighter_1.animation_update()
    fighter_2.animation_update()

    # Quitting conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Display update
    pygame.display.update()

pygame.quit()
