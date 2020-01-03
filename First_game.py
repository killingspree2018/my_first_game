import pygame

pygame.init()

# background images and sounds
win = pygame.display.set_mode((1000, 480))
pygame.display.set_caption("First Game")
bg = [pygame.image.load('IMAGES/backgrounds/bg.png'), pygame.image.load('IMAGES/backgrounds/bg1.png'), pygame.image.load('IMAGES/backgrounds/bg2.jpg'),
      pygame.image.load('IMAGES/backgrounds/bg3.png'), pygame.image.load('IMAGES/backgrounds/bg4.png')]
music = pygame.mixer.music.load("SOUND/music.mp3")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

# game sounds
bulletSound = pygame.mixer.Sound("SOUND/shoot.wav")
hitSound = pygame.mixer.Sound("SOUND/hit.wav")
killedsound = pygame.mixer.Sound("SOUND/killed.wav")
deadsound = pygame.mixer.Sound("SOUND/dead.wav")
starting = pygame.mixer.Sound("SOUND/start.wav")
failed = pygame.mixer.Sound("SOUND/failed.wav")
won = pygame.mixer.Sound("SOUND/won.wav")


# enemy class
class enemy(object):
    walkRight = [pygame.image.load('IMAGES/ENEMY/RIGHT/R1.png'), pygame.image.load('IMAGES/ENEMY/RIGHT/R2.png'),
                 pygame.image.load('IMAGES/ENEMY/RIGHT/R3.png'),
                 pygame.image.load('IMAGES/ENEMY/RIGHT/R4.png'), pygame.image.load('IMAGES/ENEMY/RIGHT/R5.png'),
                 pygame.image.load('IMAGES/ENEMY/RIGHT/R6.png'),
                 pygame.image.load('IMAGES/ENEMY/RIGHT/R7.png'), pygame.image.load('IMAGES/ENEMY/RIGHT/R8.png')
                 # , pygame.image.load('IMAGES/ENEMY/RIGHT/R9.png'),
                 # pygame.image.load('IMAGES/ENEMY/RIGHT/R10.png'), pygame.image.load('IMAGES/ENEMY/RIGHT/R11.png')
                 ]
    walkLeft = [pygame.image.load('IMAGES/ENEMY/LEFT/L1.png'), pygame.image.load('IMAGES/ENEMY/LEFT/L2.png'),
                pygame.image.load('IMAGES/ENEMY/LEFT/L3.png'),
                pygame.image.load('IMAGES/ENEMY/LEFT/L4.png'), pygame.image.load('IMAGES/ENEMY/LEFT/L5.png'),
                pygame.image.load('IMAGES/ENEMY/LEFT/L6.png'),
                pygame.image.load('IMAGES/ENEMY/LEFT/L7.png'), pygame.image.load('IMAGES/ENEMY/LEFT/L8.png')
                # , pygame.image.load('IMAGES/ENEMY/LEFT/L9.png'),
                # pygame.image.load('IMAGES/ENEMY/LEFT/L10.png'), pygame.image.load('IMAGES/ENEMY/LEFT/L11.png')
                ]

    def __init__(self, start, x, y, width, height, end, dir, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [start, end]
        self.walkCount = 0
        self.vel = (3 + man.score // 200) * dir
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = health
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 24:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 15 + (man.score // 100), 10))
            pygame.draw.rect(win, (0, 118, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, self.health + (man.score // 100), 10))
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):

        if self.health + man.score // 100 > 0:
            self.health -= (1 + man.score // 1000)
            killedsound.play()
        else:
            killedsound.play()
            self.visible = False


# players class
class player(object):
    walkRight = [pygame.image.load('IMAGES/COWBOY/RIGHT/R1.png'), pygame.image.load('IMAGES/COWBOY/RIGHT/R2.png'),
                 pygame.image.load('IMAGES/COWBOY/RIGHT/R3.png'),
                 pygame.image.load('IMAGES/COWBOY/RIGHT/R4.png'), pygame.image.load('IMAGES/COWBOY/RIGHT/R5.png'),
                 pygame.image.load('IMAGES/COWBOY/RIGHT/R6.png'),
                 pygame.image.load('IMAGES/COWBOY/RIGHT/R7.png'), pygame.image.load('IMAGES/COWBOY/RIGHT/R8.png')
                 # , pygame.image.load('IMAGES/COWBOY/RIGHT/R9.png')
                 ]
    walkLeft = [pygame.image.load('IMAGES/COWBOY/LEFT/L1.png'), pygame.image.load('IMAGES/COWBOY/LEFT/L2.png'),
                pygame.image.load('IMAGES/COWBOY/LEFT/L3.png'),
                pygame.image.load('IMAGES/COWBOY/LEFT/L4.png'), pygame.image.load('IMAGES/COWBOY/LEFT/L5.png'),
                pygame.image.load('IMAGES/COWBOY/LEFT/L6.png'),
                pygame.image.load('IMAGES/COWBOY/LEFT/L7.png'), pygame.image.load('IMAGES/COWBOY/LEFT/L8.png')
                # , pygame.image.load('IMAGES/COWBOY/LEFT/L9.png')
                ]
    char = pygame.image.load('IMAGES/COWBOY/standing.png')

    def __init__(self, x, y, width, height):
        self.name = ''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.score = 0
        self.lives = 5
        file1 = open("high_score.txt", "r")
        self.high_score = file1.read(4)
        # print(self.high_score)
        file1.close()
        self.immune = 50

    def draw(self, win):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(self.walkLeft[0], (self.x, self.y))
            else:
                win.blit(self.char, (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.score % 400 == 0 and self.score > 0:
            self.vel += 1
        if self.score % 500 == 0 and self.score > 0:
            self.lives += 1
        self.score += (1 + self.score // 1000)

    def killed(self):
        deadsound.play()
        if self.lives > 0:
            self.x = 500
            self.walkCount = 0
            self.lives -= 1
            self.immune = 50
            i = 0
            while i < 200:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
            if self.lives > 0:
                starting.play()


class projectile(object):
    def __init__(self, x, y, color, radius, facing):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.facing = facing
        self.vel = (8 + man.score // 400) * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg[(man.score // 500) % 5], (0, 0))
    # win.blit(bg, (500, 0))
    if start:
        if man.lives > 0:
            man.draw(win)
            text1 = font.render('Score: ' + str(man.score), 1, (200, 200, 200))
            text2 = font.render('Lives: ' + str(man.lives), 1, (200, 200, 200))
            win.blit(text1, (800, 20))
            win.blit(text2, (800, 60))
            for goblin in goblins:
                goblin.draw(win)
            for bullet in bullets:
                bullet.draw(win)
        else:
            # print(man.high_score)
            # print(str(man.score))
            if int(man.high_score) < (man.score):
                man.high_score = str(man.score)
                file1 = open("high_score.txt", "w")
                file1.write(man.high_score + '   ' + man.name)
                file1.close()
                won.play()
            else:
                failed.play()
            game_over()
    else:
        start_game()
    pygame.display.update()


def start_game():
    global start
    text9 = font.render('ENTER YOUR NAME', 1, (255, 0, 0))
    win.blit(text9, (350, 270))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = True
                starting.play()
            elif event.key == pygame.K_BACKSPACE:
                man.name = man.name[:-1]
            else:
                man.name += event.unicode
    text10 = font.render(man.name, 1, (0, 0, 255))
    win.blit(text10, (350, 300))
    pygame.display.update()


def game_over():
    text3 = font1.render('GAME OVER', 1, (0, 0, 0))
    text4 = font.render('FINAL SCORE: ' + man.name + '   ' + str(man.score), 1, (0, 0, 255))
    file1 = open("high_score.txt", "r")
    text5 = font.render('HIGHEST SCORE: ' + file1.read(), 1, (150, 0, 0))
    file1.close()
    text6 = font2.render('PRESS SPACE TO PLAY AGAIN', 1, (0, 255, 0))
    win.blit(text3, (350, 150))
    win.blit(text4, (350, 270))
    win.blit(text5, (350, 320))
    win.blit(text6, (350, 400))
    pygame.display.update()
    i = 1
    while i:
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            man.score = 0
            man.lives = 5
            goblins.clear()
            bullets.clear()
            file1 = open("high_score.txt", "r")
            man.high_score = file1.read(4)
            file1.close()
            i = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


# mainloop
man = player(500, 410, 64, 64)
bullets = []
shoot = 0
attack = 0
fly_goblin = 2
font = pygame.font.SysFont('comicsansms', 30, True)
font1 = pygame.font.SysFont('comicsansms', 70, True)
font3 = pygame.font.SysFont('comicsansms', 120, True)
font2 = pygame.font.SysFont('comicsansms', 20, True, True)
goblins = [enemy(3, 70, 410, 64, 64, 950, 1, 15)]
run = True
start = False

while run:
    clock.tick(27)
    if start:
        if shoot > 0:
            shoot += 1
        if shoot > 3:
            shoot = 0
        if attack >= 0:
            attack += 1
        if attack == 200 or goblins == []:
            if man.x > 250 * 2 or man.score < 100:
                if man.score > 100:
                    if fly_goblin == 2 + man.score // 400:
                        goblins.append(enemy(3, 70, 250, 64, 64, 950, 1, 2))
                        fly_goblin = 0
                    fly_goblin += 1
                goblins.append(enemy(3, 910, 410, 64, 64, 950, -1, 15))
            if man.x < 500 or man.score < 100:
                if man.score > 100:
                    if fly_goblin == 2 + man.score // 400:
                        goblins.append(enemy(3, 910, 250, 64, 64, 950, -1, 2))
                        fly_goblin = 0
                    fly_goblin += 1
                goblins.append(enemy(3, 70, 410, 64, 64, 950, 1, 15))
            attack = 0
        if man.immune > 0:
            man.immune -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for goblin in goblins:
            if goblin.visible:
                if not man.immune:
                    if goblin.hitbox[1] < man.hitbox[3] + man.hitbox[1] and man.hitbox[1] < goblin.hitbox[1] + \
                            goblin.hitbox[3]:
                        if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > \
                                goblin.hitbox[0]:
                            man.killed()
            else:
                goblins.pop(goblins.index(goblin))
        for bullet in bullets:
            x = 1
            for goblin in goblins:
                if goblin.visible:
                    if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                            goblin.hitbox[1]:
                        if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                                goblin.hitbox[2]:
                            man.hit()
                            goblin.hit()
                            while x:
                                bullets.pop(bullets.index(bullet))
                                x -= 1
            if 0 < bullet.x < 1000:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shoot == 0:
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5 + (man.score // 200) % 5:
                bulletSound.play()
                bullets.append(
                    projectile(round(man.x + man.width * (facing > 0) - 13 * facing), round(man.y + man.height // 1.4),
                               (0, 0, 255), 4, facing))
            shoot = 1

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 1000 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            # man.right = False
            # man.left = False
            man.walkCount = 0
            man.standing = True

        if not man.isJump:
            if keys[pygame.K_UP]:
                man.isJump = True
                # man.right = False
                # man.left = False
                man.standing = True
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
