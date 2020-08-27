import pygame
import random
import math

from pygame import mixer

# Initialise the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))  # width and height

# Title and Icon
pygame.display.set_caption("SPACE INVADERS")  # Sets title
icon = pygame.image.load("icon.png")  # Loads an image
pygame.display.set_icon(icon)  # Sets icon

# Background
background = pygame.image.load("bg.jpg")

# Background music
mixer.music.load("bgm.wav")
mixer.music.play(-1)  # Play on loop

# Player
playerImg = pygame.image.load("ship.png")
playerX = 370
playerY = 480
playerX_change = 4


# Score
score_value = 0
font = pygame.font.Font("Starjedi.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemySpeed = 1

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(50, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY
bulletSpeed = 5
bulletState = False


def fire_bullet(x, y):
    global bulletState
    bulletState = True
    screen.blit(bulletImg, (x + 16, y))

# Collision detection


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def gameOver():
    gfont = pygame.font.Font("Starjedi.ttf", 64)
    gtextX = 200
    gtextY = 250

    gOver = gfont.render("GAME over", True, (255, 255, 255))
    screen.blit(gOver, (gtextX, gtextY))


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))  # Background colour (RGB)

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Clicking the red button
            running = False

    # Spaceship Movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= playerX_change
        elif event.key == pygame.K_RIGHT:
            playerX += playerX_change

    # Creating a bullet
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if bulletState == False:
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()

    # Bullet movement
    if bulletState == True:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletSpeed

    # Boundary checks (Spaceship)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        if enemyX[i] <= 0:
            enemyX_change[i] = enemySpeed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemySpeed
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bulletState = False
            score_value += 10  # Update Score
            # Create new enemy
            enemyX[i] = random.randint(50, 735)
            enemyY[i] = random.randint(50, 150)
            collsion_sound = mixer.Sound("boom.wav")
            collsion_sound.play()

        enemyX[i] += enemyX_change[i]

        # Draw enemy
        enemy(enemyX[i], enemyY[i], i)

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

    # Boundary checks (bullet)
    if bulletY <= 0:
        bulletState = False
        bulletY = playerY

    # Draw player
    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
