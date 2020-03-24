import pygame
import random
import numpy as np

pygame.init()
pygame.font.init()

sx = 450
sy = 529
win = pygame.display.set_mode((sx, 529))

pygame.display.set_caption("Katerina Tennis Game")

# Load pictures
bg = pygame.image.load('c:/PythonGame/img/bg.jpg')
standing = [pygame.image.load('c:/PythonGame/img/katerina_standing.png'),
            pygame.image.load('c:/PythonGame/img/anton_standing.png')]
walk = [[pygame.image.load('c:/PythonGame/img/katerina_walk1.png'),
         pygame.image.load('c:/PythonGame/img/katerina_walk2.png')],
        [pygame.image.load('c:/PythonGame/img/anton_walk1.png'),
         pygame.image.load('c:/PythonGame/img/anton_walk2.png')]]

shoot = [[pygame.image.load('c:/PythonGame/img/katerina_shoot1.png'),
          pygame.image.load('c:/PythonGame/img/katerina_shoot2.png'),
          pygame.image.load('c:/PythonGame/img/katerina_shoot3.png')],
         [pygame.image.load('c:/PythonGame/img/anton_shoot1.png'),
          pygame.image.load('c:/PythonGame/img/anton_shoot2.png'),
          pygame.image.load('c:/PythonGame/img/anton_shoot3.png')]]

ballpic = [pygame.image.load('c:/PythonGame/img/ball.png'),
           pygame.image.load('c:/PythonGame/img/ball2.png'),
           pygame.image.load('c:/PythonGame/img/ball3.png')]

clock = pygame.time.Clock()

# Load music
sound_hit = pygame.mixer.Sound('c:/PythonGame/sound/hit.wav')
pygame.mixer.music.load('c:/PythonGame/sound/music.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)


# Tennis player
class player(object):
    def __init__(self, x, y, width, height, playername):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True
        self.walkCount = 0
        self.shooting = 0
        self.playername = playername
        if (playername == 'Katerina'):
            self.hitbox = (self.x + 4, self.y + 37, 29, 38)
        if (playername == 'Anton'):
            self.hitbox = (self.x + 4, self.y + 5, 29, 38)

    def draw(self, win):

        if self.playername == 'Katerina':
            picindex = 0
            self.vel = 5
        elif self.playername == 'Anton':
            picindex = 1
            self.vel = 4

        if self.shooting > 0:
            win.blit(shoot[picindex][(self.shooting - 1) // 3], (self.x, self.y))
            self.shooting += 1
            if (self.shooting >= 9):
                self.shooting = 0
        else:
            if self.walkCount + 1 >= 6:
                self.walkCount = 0
            if self.left:
                win.blit(walk[picindex][self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walk[picindex][self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.up:
                win.blit(walk[picindex][self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.down:
                win.blit(walk[picindex][self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.standing:
                win.blit(standing[picindex], (self.x, self.y))

        if (self.playername == 'Katerina'):
            self.hitbox = (self.x + 4, self.y + 41, 29, 20)
        if (self.playername == 'Anton'):
            self.hitbox = (self.x + 4, self.y + 41, 29, 20)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


class ball(object):
    def __init__(self, x, y, speedx, speedy, width, height):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.width = width
        self.height = height

    def draw(self, win):
        if (abs(self.y - sy / 2) < 75):
            win.blit(ballpic[2], (self.x, self.y))
        elif (abs(self.y - sy / 2) < 180):
            win.blit(ballpic[1], (self.x, self.y))
        else:
            win.blit(ballpic[0], (self.x, self.y))

    def point(self, name, score):
        font1 = pygame.font.SysFont('Sans', 60)
        text1 = font1.render('Game ' + name, 1, (0, 0, 0))
        text2 = font1.render(str(score[0]) + ':' + str(score[1]), 1, (0, 0, 0))
        win.blit(text1, (round(sx / 2 - (text1.get_width() / 2)), 100))
        win.blit(text2, (round(sx / 2 - (text2.get_width() / 2)), 150))

        if score[0] == 5 or score[1] == 5:
            text3 = font1.render(name, 1, (0, 0, 0))
            text4 = font1.render('wins the match', 1, (0, 0, 0))

            win.blit(text3, (round(sx / 2 - (text3.get_width() / 2)), 270))
            win.blit(text4, (round(sx / 2 - (text4.get_width() / 2)), 320))

        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


def redrawGameWindow():
    win.blit(bg, (0, 0))
    for numball in balls:
        numball.draw(win)
    kate.draw(win)
    anto.draw(win)
    pygame.display.update()


# Score
score = [0, 0]
balls = []

# mainloop
kate = player(200, 410, 60, 64, 'Katerina')
anto = player(200, 5, 60, 64, 'Anton')

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if (len(balls) == 0):
        if (anto.x < 190):
            anto.x += anto.vel
            anto.left = False
            anto.right = True
            anto.standing = False
        elif (anto.x > 210):
            anto.x -= anto.vel
            anto.left = True
            anto.right = False
            anto.standing = False
        else:
            anto.left = False
            anto.right = False
            anto.standing = True

    for numball in balls:
        if 0 < numball.x and numball.x < sx and 0 <= numball.y and numball.y < sy:
            numball.x += numball.speedx
            numball.y -= numball.speedy
        else:
            # Katerina wins point
            if (numball.speedy > 0 and (20 < numball.x and numball.x < sx - 20)):
                print('Katerina wins point')
                score[0] += 1
                numball.point('Katerina', score)
            # Katerina looses point
            elif (numball.speedy > 0 and (numball.x <= 20 or sx - 20 <= numball.x)):
                print('Katerina looses point')
                score[1] += 1
                numball.point('Anton', score)
            # Anton wins point
            elif (numball.speedy < 0 and (20 < numball.x and numball.x < sx - 20)):
                print('Anton wins point')
                score[1] += 1
                numball.point('Anton', score)
            # Anton looses point
            elif (numball.speedy < 0 and (numball.x <= 20 or sx - 20 <= numball.x)):
                print('Anton looses point')
                score[0] += 1
                numball.point('Katerina', score)

            if (score[0] == 5 or score[1] == 5):
                score = [0, 0]

            balls.pop(balls.index(numball))

        if (len(balls) > 0):

            # Hit anton
            if numball.y < anto.hitbox[1] + anto.hitbox[3] and anto.hitbox[0] < numball.x and numball.x < anto.hitbox[
                0] + anto.hitbox[2]:
                sound_hit.play()
                anto.shooting = 1
                pygame.time.delay(10)
                numball.speedy = -numball.speedy + random.randint(-2, 1)
                numball.speedx += np.sign(numball.speedx) * random.randint(-2, 0)
                numball.y = anto.hitbox[1] + anto.hitbox[3] + 3

                # Hit Katerina
            if kate.hitbox[1] < numball.y and numball.y < kate.hitbox[1] + kate.hitbox[3] and kate.hitbox[
                0] < numball.x and numball.x < kate.hitbox[0] + kate.hitbox[2]:
                sound_hit.play()
                kate.shooting = 1
                pygame.time.delay(10)
                numball.speedy = -numball.speedy + random.randint(-2, 1)
                numball.speedx = -numball.speedx + random.randint(-2, 2)
                numball.y = kate.hitbox[1] - 3

                # Anton movement
            if numball.x < anto.x + 10 and numball.speedy > 0:  # and (anto.left or anto.standing or abs(numball.x - anto.x) > 4):
                anto.x -= anto.vel
                anto.left = True
                anto.right = False
                anto.standing = False
            elif numball.x > anto.x and numball.speedy > 0:  # and (anto.right or anto.standing or abs(numball.x - anto.x) > 4):
                anto.x += anto.vel
                anto.left = False
                anto.right = True
                anto.standing = False
            elif anto.x < 190 and numball.speedy < 0:
                anto.x += anto.vel
                anto.left = False
                anto.right = True
                anto.standing = False
            elif anto.x > 210 and numball.speedy < 0:
                anto.x -= anto.vel
                anto.left = True
                anto.right = False
                anto.standing = False
            elif numball.speedy < 0:
                anto.left = False
                anto.right = False
                anto.standing = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and kate.x > kate.vel - 20:
        kate.x -= kate.vel
        kate.left = True
        kate.right = False
        kate.up = False
        kate.standing = False
        kate.down = False
    elif keys[pygame.K_RIGHT] and kate.x < 450 - 25:
        kate.x += kate.vel
        kate.right = True
        kate.left = False
        kate.up = False
        kate.standing = False
        kate.down = False
    if keys[pygame.K_UP] and kate.y > 280 - kate.height - kate.vel:
        kate.y -= kate.vel
        kate.right = False
        kate.left = False
        kate.up = True
        kate.standing = False
        kate.down = False
    elif keys[pygame.K_DOWN] and kate.y < 529 - kate.width - kate.vel:
        kate.right = False
        kate.left = False
        kate.up = False
        kate.down = True
        kate.standing = False
        kate.y += kate.vel
    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        kate.right = False
        kate.left = False
        kate.up = False
        kate.down = False
        kate.standing = True
        kate.walkCount = 0

    if keys[pygame.K_SPACE]:
        if len(balls) == 0:
            sound_hit.play()
            kate.shooting = 1
            xspeed = random.randint(-3, 3)
            newball = ball(kate.x + 8, kate.y + 15, xspeed, 10, 9, 9)
            balls.append(newball)

    redrawGameWindow()

pygame.quit()
