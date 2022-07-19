import pygame
# how to import and use sounds in pygame import mixer
from pygame import mixer
import math
import random

# used ufo.png from https://www.flaticon.com/free-icon/ufo_3306604?term=alien&page=1&position=3&page=1&position=3&related_id=3306604&origin=search
# used spaceship.png from "https://www.flaticon.com/free-icons/spaceship" Spaceship icons created by Freepik - Flaticon
# used enemy.png from https://www.flaticon.com/free-icons/alien" Alien icons created by Freepik - Flaticon
# used bullet.ong from "https://www.flaticon.com/free-icons/bullet" Bullet icons created by Vector Stall - Flaticon

# initializing pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800,600))

# how to use background image for pygame application
# background
# background = pygame.image.load("./sprites/background.png")

# code to implement background music
# background music
# mixer.music.load("./sounds/background.wav")
# mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./sprites/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./sprites/player.png')
playerX = 370
playerY = 480
playerX_Change = 0

def player(x, y):
  screen.blit(playerImg, (x, y))

# enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load("./sprites/enemy.png"))
  enemyX.append(random.randint(0,735))
  enemyY.append(random.randint(50,150))
  enemyX_Change.append(0.1)
  enemyY_Change.append(40)

def enemy(x,y,i):
  screen.blit(enemyImg[i], (x,y))


# bullet
# ready - you cannot see the bullet on the screen
# fire = the bullet is currently moving
bulletImg = pygame.image.load("./sprites/bullet.png")
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = .5
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text

over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x,y):
  game_score = font.render("Score : " + str(score), True, (0,0,0))
  screen.blit(game_score, (x, y))

def game_over_text():
  over_text = over_font.render("GAME OVER", True, (0,0,0))
  screen.blit(over_text, (200,250))

def fire_bullet(x,y):
  global bullet_state
  bullet_state = "fire"
  screen.blit(bulletImg, (x + 16 , y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
  distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY,2)))
  if distance < 27:
    return True
  else:
    return False

# Game Loop 
running = True
while running: 
  # RGB - Red, Green, Blue
  screen.fill((255, 255, 255))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    # if keystroke is pressed check whether its right or left
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        playerX_Change = -0.3
      if event.key == pygame.K_RIGHT:
        playerX_Change = 0.3
      if event.key == pygame.K_SPACE:
        if bullet_state is "ready":
          # how to use mixer.sound for bullet
          # bullet_sound = mixer.Sound("./sounds/laser.wav")
          # bullet_sound.play()

          # get current x coordinate of spaceship
          bulletX = playerX
          fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        playerX_Change = 0

  # set boundaries for player
  playerX += playerX_Change
  if playerX <= 0:
    playerX = 0
  elif playerX >= 736:
    playerX = 736

  # setting boundaries and movements for enemies
  for i in range(num_of_enemies):

    # Game Over
    if enemyY[i] > 440:
      for j in range(num_of_enemies):
        enemyY[j] = 2000
      game_over_text()
      break

    enemyX[i] += enemyX_Change[i]
    if enemyX[i] <= 0:
      enemyX_Change[i] = 0.1
      enemyY[i] += enemyY_Change[i]
    elif enemyX[i] >= 736:
      enemyX_Change[i] = -0.1
      enemyY[i] += enemyY_Change[i]

    # collision
    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    if collision:
      # mixer.sound code for implementing explosion sound on collision
      # explosion_sound  = mixer.Sound("./sounds/explosion.wav")
      # explosion_sound.play()
      bulletY = 480
      bullet_state = "ready"
      score += 1
      enemyX[i] = random.randint(0, 735)
      enemyY[i] = random.randint(50, 150)
    enemy(enemyX[i], enemyY[i], i)

  # bullet movement 
  if bulletY <= 0 :
    bulletY = 480
    bullet_state = "ready"
  if bullet_state is "fire":
    fire_bullet(bulletX, bulletY)
    bulletY -= bulletY_Change
 

  player(playerX, playerY)
  show_score(textX, textY)

  pygame.display.update()