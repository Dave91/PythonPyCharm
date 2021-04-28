import csv
import os
import random

import pygame

pygame.font.init()
pygame.mixer.init()

SETTINGS = []
with open('config.txt', mode='r') as fopen:
    fread = csv.reader(fopen, delimiter='=')
    for fline in fread:
        SETTINGS.append(fline)

SET_MUSIC = (SETTINGS[0])[1]  # True
SET_FPS = int((SETTINGS[1])[1])  # 60
SET_VEL = int((SETTINGS[2])[1])  # 5
SET_BULLET_VEL = int((SETTINGS[3])[1])  # 7
SET_MAX_BULLETS = int((SETTINGS[4])[1])  # 3
SET_PLAYERS_HEALTH = int((SETTINGS[5])[1])  # 10

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Multiplayer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

TITLE_FONT = pygame.font.SysFont("comicsans", 70)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SHIP_EXPLOSION = pygame.mixer.Sound('Assets/explosion.wav')
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hitsound.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/laser.wav')

PLAY_MUSIC = SET_MUSIC
FPS = SET_FPS
VEL = SET_VEL
BULLET_VEL = SET_BULLET_VEL
MAX_BULLETS = SET_MAX_BULLETS
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))  # background.png


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, players_max_health,
                yellow_score, red_score):
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    # healthbar yellow (p1) (coords: x, y, size: x, y)
    pygame.draw.rect(WINDOW, RED, (yellow.x - 10, yellow.y,
                                   5, YELLOW_SPACESHIP.get_height()))
    pygame.draw.rect(WINDOW, GREEN, (yellow.x - 10, yellow.y,
                                     5, YELLOW_SPACESHIP.get_height() * (yellow_health / players_max_health)))
    # healthbar red (p2) (coords: x, y, size: x, y)
    pygame.draw.rect(WINDOW, RED, (red.x + RED_SPACESHIP.get_width() + 10, red.y,
                                   5, RED_SPACESHIP.get_height()))
    pygame.draw.rect(WINDOW, GREEN, (red.x + RED_SPACESHIP.get_width() + 10, red.y,
                                     5, RED_SPACESHIP.get_height() * (red_health / players_max_health)))

    yellow_score_text = SCORE_FONT.render("(Player1) " + str(yellow_score), True, WHITE)
    red_score_text = SCORE_FONT.render(str(red_score) + " (Player2)", True, WHITE)
    WINDOW.blit(yellow_score_text, (10, 10))
    WINDOW.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):  # p1 move wasd (left, right, up, down)
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):  # p2 move arrows (left, right, up, down)
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def bot_actions():
    rand_action = random.randint(0, 10)
    if rand_action in range(5):
        if rand_action == 0:
            actionevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
            pygame.event.post(actionevent)
        if rand_action == 1:
            actionevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
            pygame.event.post(actionevent)
        if rand_action == 2:
            actionevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
            pygame.event.post(actionevent)
        if rand_action == 3:
            actionevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
            pygame.event.post(actionevent)
        if rand_action == 4:
            actionevent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RCTRL)
            pygame.event.post(actionevent)


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WINDOW.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main(yellow_score, red_score):
    if PLAY_MUSIC:
        pygame.mixer.music.load("Assets/background.wav")
        pygame.mixer.music.play(-1)

    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    players_max_health = SET_PLAYERS_HEALTH
    red_health = SET_PLAYERS_HEALTH
    yellow_health = SET_PLAYERS_HEALTH
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:  # Space p1 fire
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:  # RCTRL p2 fire
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Player1 (Yellow) Wins!"
            yellow_score += 1
        if yellow_health <= 0:
            winner_text = "Player2 (Red) Wins!"
            red_score += 1
        if winner_text != "":
            SHIP_EXPLOSION.play()
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, players_max_health, yellow_score, red_score)

    main(yellow_score, red_score)


def main_menu():
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title_label = TITLE_FONT.render("Click to begin...", True, WHITE)
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                yellow_score = 0
                red_score = 0
                main(yellow_score, red_score)

    pygame.quit()


if __name__ == "__main__":
    main_menu()
