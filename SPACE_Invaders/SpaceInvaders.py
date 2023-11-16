import pygame
from pygame import mixer
import random
import math

# Initalizes the pygame
pygame.init()
mixer.init()

#Generates Screen in X and Y axis
screen = pygame.display.set_mode((800,600))
running = True

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SPACE_Invaders/ufo.png')
pygame.display.set_icon(icon)

#PLayer
playerImg = pygame.image.load('SPACE_Invaders/player.png')
playerX = 370
playerY = 480
playerXChange = 0

#Enemy
ememyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChnage = []
numOfEnemies = 6

#this creates an array of different enemies
for i in range(numOfEnemies):
    ememyImg.append(pygame.image.load('SPACE_Invaders/enemy.png'))
    enemyX.append(random.randint(0, 100))
    enemyY.append(random.randint(50,100))
    enemyXChange.append(2)  #this gives each enemy a random speed
    enemyYChnage.append(1)


#bullet... ready means you cant see the bullet on the screen, but fire means the bullet is suppose to be moving
bulletImg = pygame.image.load('SPACE_Invaders/bullet.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 3 #this gives the bullet its speed
bullet_state = "ready"


#background image
bgImg = pygame.image.load('SPACE_Invaders/universe.png')
bgImg = pygame.transform.scale(bgImg, (800, 600))

#background sounds
mixer.music.load('SPACE_Invaders//bksong.mp3')
mixer.music.play(-1)

mixer.music.set_volume(0.2)


#score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#gameOver
gameOverFont = pygame.font.Font("freesansbold.ttf", 64)

def showScore(x,y):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score,(x,y))

#gameOver
def gameOverText():
    overText = gameOverFont.render("GAME OVER! " , True, (255,255,255))
    screen.blit(overText, (200,250))


def player(x, y):
    # blit means to draw
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    # blit means to draw
    screen.blit(ememyImg[i], (x, y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10 )) #this align to bullet with the space craft.

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Gameloop
while running:
    screen.blit(bgImg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerXChange = -2

            if event.key == pygame.K_RIGHT:
                playerXChange = 2

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound('SPACE_Invaders/shot.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0


    playerX += playerXChange

    #this creates the border. We picked 736 because our image is 64bits
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    #This part is generating the movement of a specific enemy at index I.
    for i in range(numOfEnemies):
        #Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break

        enemyX[i] += enemyXChange[i]

        if enemyX[i] >= 736:
            enemyY[i] += enemyYChnage[i]
            enemyXChange[i] = -enemyXChange[i]

        elif enemyX[i] <= 0:
            enemyY[i] += enemyYChnage[i]
            enemyXChange[i] = -enemyXChange[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            killsounds = mixer.Sound('SPACE_Invaders/kill.wav')
            killsounds.play()
            bulletY = 480
            bullet_state = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 100)


        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY<= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange


    player(playerX, playerY)
    showScore(textX,textY)
    pygame.display.update()