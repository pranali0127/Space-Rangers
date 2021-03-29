import pygame
from pygame.base import *
import random
import math
from pygame import mixer
import sys

# initialise pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# background adding
background = pygame.image.load('game_bg.png')

# background sound
# for continues sound we use mixer.music
# for short sound we use mixer.sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title
pygame.display.set_caption("Space Rangers")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('battleship.png')
global playerX
global playerX_change
playerX = 370
playerY = 480
playerX_change = 0

alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 8

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_change.append(4)
    alienY_change.append(40)

# ready = you cant see the bullet on the screen
# Fire = the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
global score_value
score_value = 0
font = pygame.font.Font('Orthographix.otf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('Orthographix.otf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("!!! GAME OVER !!!", True, (255, 255, 255))
    button_3 = pygame.Rect(50, 100, 200, 50)
    mx, my = pygame.mouse.get_pos()
    if button_3.collidepoint((mx, my)):
        if click:
            game()
    pygame.draw.rect(screen, (255, 255, 255), button_3)
    screen.blit(over_text, (200, 250))
    pygame.display.update()


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# collision detection
def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# drawing text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 3, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# creating menus

# game loop

running = True
while running:
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check key stroke
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_UP:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # get the current x coordinate
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
    # checking for boundries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # checking for alien boundries

    # alien movement
    for i in range(num_of_aliens):

        # game over
        if alienY[i] > 440.:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 4
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -4
            alienY[i] += alienY_change[i]
        # collison
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


#main_menu(