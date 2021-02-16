import pygame, random, math
from pygame import mixer
# Initialize
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
#Header png
pygame.display.set_caption("space Blasters")
icon = pygame.image.load("heading.png")
pygame.display.set_icon(icon)
#bg img
background = pygame.image.load("background.png")
pygame.display.set_icon(background)

playerChangeX = 0
playerChangeY = 0
speed = 1.5
gameover = False


#opposing spaceships
class bad:
    badX = random.randint(0, 540)
    badY = 10
    badImg = pygame.image.load("badspaceshipthing.png")
    badImg = pygame.transform.scale(badImg, (60,60))
    badspeed = 3
    badChangeX = 2
    badChangeY = 20
    def __init__(self):
        self.badX = random.randint(0, 740)
        self.badY = random.randint(0, 100)
    def bad(self, X, Y):
        screen.blit(self.badImg, (self.badX,self.badY))


ammout = 300
e = [bad() for i in range(ammout)]

#blaster
bulletX = 360
bulletY = 500
bulletImg = pygame.image.load("bad.png")
bulletImg = pygame.transform.scale(bulletImg, (60,60))
bulletshot = 0
bulletChangeY = 3
bbulletspeed = 3
def bullet(X, Y):
    screen.blit(bulletImg, (X,Y))

score = 0


def player(X, Y):
    screen.blit(playerImg, (X,Y))
running = True
background = pygame.transform.scale(background, (800, 600))
def bgimg(X, Y):
    screen.blit(background, (0,0))
#player
playerX = 360
playerY = 500
playerImg = pygame.image.load("spaceship thing.gif")
playerImg = pygame.transform.scale(playerImg, (60,60))

# background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.08)
pygame.mixer.music.play(-1)


def gameOver():
   over = pygame.font.Font("freesansbold.ttf", 64)
   gameover = over.render("Game Over", True, (255, 255, 255))
   pygame.mixer.music.set_volume(0)
   oof = mixer.Sound("oof.wav")
   oof.set_volume(0.1)
   oof.play()
   screen.blit(gameover, (240, 250))


#game loop
running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_a:
               playerChangeX = -speed
           if event.key == pygame.K_d:
               playerChangeX = +speed

           if event.key == pygame.K_SPACE:
               if bulletshot == 0:
                   bulletX = playerX
                   bulletY = playerY
                   bulletshot = 1
                   fire = mixer.Sound("pewpew.wav")
                   fire.play()


       if event.type == pygame.KEYUP:
           playerChangeX = 0
           playerChangeY = 0

   if (playerX<0):
        playerX = 0
   if (playerX>740):
       playerX = 740

   if (playerY < 0):
       playerY = 0
   if (playerY > 540):
       playerY = 540

       # Detect collision

   bgimg(0, 0)
   num=int(5+score*0.5)
   if (num>30):
       num = 30
   if not gameover:
       for i in range(num):
           e[i].badX += e[i].badChangeX
           if e[i].badX < 0:
               e[i].badX = 0
               e[i].badChangeX = -e[i].badChangeX
               e[i].badY += e[i].badChangeY
           if e[i].badX > 740:
               e[i].badX = 740
               e[i].badChangeX = -e[i].badChangeX
               e[i].badY += e[i].badChangeY
           e[i].bad(e[i].badX, e[i].badY)

           d = math.sqrt(math.pow((e[i].badX) - (bulletX), 2) + math.pow((e[i].badY) - (bulletY), 2))
           if d < 30 and bulletshot==1:
               print ("Its a hit")
               explode = mixer.Sound("boom.wav")
               explode.set_volume(0.4)
               explode.play()
               e[i].badY = random.randint(0, 100)
               e[i].badX = random.randint(0, 740)
               bulletY = 500
               score = score + 1
               print(score)
               bulletshot = 0
               # del(e[i])
               break
   if bulletY < 0:
       bulletshot = 0

   for i in range(len(e)):
       if e[i].badY > 500:
           gameover = True
           e[i].badY = 1000
   if gameover:
       gameOver()

    #opposing spaceship's movement

   #badX += badChangeX
   #if badX < 0:
   #    badX = 0
    #   badChangeX = - badChangeX
  #     badY += badChangeY
       #    if badX > 740:
       #        badX = 740
       #        badChangeX = -badChangeX
       #        badY += badChangeY



   playerX = playerX + playerChangeX
   if (bulletshot == 1):
        bullet(bulletX, bulletY)
   playerY = playerY + playerChangeY
   bulletY = bulletY - bulletChangeY

   # Print score in screen
   font = pygame.font.Font('freesansbold.ttf', 24)
   scr = font.render("Score: " + str(score), True, (255, 255, 255))
   screen.blit(scr, (10, 10))

   player(playerX, playerY)
   pygame.display.update()