# Imports
import pygame
import random
import sys
import os

if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(__file__)
else:
    current_path = os.path.dirname(__file__)

# Initialize game engine
pygame.init()

# Window
WIDTH = 1000
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Cosmic Intruders"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(current_path + "/assets/fonts/space_age.ttf", 24)
FONT_MD = pygame.font.Font(current_path + "/assets/fonts/space_age.ttf", 32)
FONT_LG = pygame.font.Font(current_path + "/assets/fonts/space_age.ttf", 64)
FONT_XL = pygame.font.Font(current_path + "/assets/fonts/space_age.ttf", 96)

# Images
ship_img = pygame.image.load(current_path + '/assets/images/player.png')
laser_img = pygame.image.load(current_path + '/assets/images/laserRed.png')
mob_img = pygame.image.load(current_path + '/assets/images/enemyShip.png')
bomb_img = pygame.image.load(current_path + '/assets/images/laserGreen.png')
full_shield = pygame.image.load(current_path + '/assets/images/FullShield.png')
first_hit = pygame.image.load(current_path + '/assets/images/Shield2.png')
second_hit = pygame.image.load(current_path + '/assets/images/Shield4.png')
last_hit = pygame.image.load(current_path + '/assets/images/EmptyShield.png')
mob_purple = pygame.image.load(current_path + '/assets/images/enemyShipPurple.png')
space = pygame.image.load(current_path + '/assets/images/background.jpg')

# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed =5
        self.shield = 3

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        if self.shield == 0:
            self.kill()

        if self.rect.x <= 1:
            self.speed -= 5
            self.rect.x += 5
            self.speed +=5

        if self.rect.x >= 900:
            self.speed -= 5
            self.rect.x -= 5
            self.speed +=5

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        stars = []
        for i in range(400):
            x = random.randrange(-200, 800)
            y = random.randrange(-50, 600)
            r = random.randrange(1, 2)
            #z = random.randrange(1, 8)
            #g = random.randrange(450, 600)
            s = [x, y, r]
            stars.append(s)

        def update(self, s):
            x = s[0]
            y = s[1]
            r = s[2]
            #z = s[3]
            if x <= 810:
                x += 2
            else:
                x = -200
            pygame.draw.ellipse(screen, WHITE, [x, y, r])

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 7

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image, shield):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = shield

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        #if len(hit_list) > self.shield:
            #self.kill()

        for h in hit_list:
            self.shield -= 1
            player.score +=1
        if self.shield == 0:
            self.kill()

class Bomb(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()

        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None

    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()


# Make game objects
ship = Ship(484, 636, ship_img)
mob1 = Mob(128, 64, mob_img, 1)
mob2 = Mob(256, 64, mob_img, 1)
mob3 = Mob(384, 64, mob_img, 1)
mob4 = Mob(128, 4, mob_img, 1)
mob5 = Mob(256, 4, mob_img, 1)
mob6 = Mob(384, 4, mob_img, 1)
mob7 = Mob(512, 64, mob_img, 1)
mob8 = Mob(512, 4, mob_img, 1)
mob9 = Mob(640, 64, mob_img, 1)
mob10 = Mob(640, 4, mob_img, 1)
mob11 = Mob(128, -56, mob_purple, 2)
mob12 = Mob(256, -56, mob_purple, 2)
mob13 = Mob(384, -56, mob_purple, 2)
mob14 = Mob(512, -56, mob_purple, 2)
mob15 = Mob(640, -56, mob_purple, 2)
star = Sky()

# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

beams = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11, mob12, mob13, mob14, mob15)

bombs = pygame.sprite.Group()

fleet = Fleet(mobs)

# set stage
stage = START

# Game helper functions
def show_title_screen():
    title_text = FONT_LG.render("Cosmic Intruders!", 1, WHITE)
    screen.blit(title_text, [78, 204])

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])


# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            if event.key == pygame.K_x:
                pygame.quit()
            elif stage == PLAYING:
                if len(mobs) > 0:
                    if len(player) > 0:
                        if event.key == pygame.K_SPACE:
                            ship.shoot()

    if stage >= 1:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        # Game logic (Check for collisions, update points, etc.)
        if stage == PLAYING:
            player.update(bombs)
            lasers.update()
            mobs.update(lasers)
            mobs.update(player)
            bombs.update()
            fleet.update()
            star.update()

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    screen.blit(space, [0,0])
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    if (ship.shield) == 3:
        screen.blit(full_shield, [20, 640])
    elif (ship.shield) == 2:
        screen.blit(first_hit, [20, 640])
    elif (ship.shield) == 1:
        screen.blit(second_hit, [20, 640])
    elif (ship.shield) == 0:
        screen.blit(last_hit, [20, 640])

    if stage == START:
        show_title_screen()
    show_stats(player)

    if len(mobs) == 0:
        win = FONT_MD.render(("You Won!"), 1, WHITE)
        #miss = FONT_MD.render(("You missed ") + str(missed) + (" shots"), 1, WHITE)
        screen.blit(win, [400, 100])
        #screen.blit(miss, [250, 175])

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()

