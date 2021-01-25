import random
import sys
import time
from os import X_OK, path

import pygame

from bullet import Bullet
from statek_gracza import StatekGracza

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "dźwięki")

WIDTH = 1024
HEIGHT = 768
FPS = 150
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SCOREBOARD = (250, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Statki")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def newboss():
    n = MobBoss()
    all_sprites.add(n)
    Bosses.add(n)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, SCOREBOARD)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Memento(object):
    def __init__(self, state):
        self._state = state

    def get_saved_state(self):
        return self._state


class Originator(object):
    _state = ""

    def set(self, state):
        print("Originator: Setting state to", state)
        self._state = state

    def save_to_memento(self):
        print("Originator: Saving to Memento.")
        return Memento(self._state)

    def restore_from_memento(self, memento):
        self._state = memento.get_saved_state()
        print("Originator: State after restoring from Memento:", self._state)


class draw_pas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Shield, (20, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 940
        self.rect.y = HEIGHT - 37
        # self.second_image = pygame.transform.scale(coin_img, (20,20))
        # self.second_image.set_colorkey(BLACK)
        # self.rect = self.second_image.get_rect()
        # self.rect.x = WIDTH - 990
        # self.rect.y = HEIGHT - 37


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 1

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class MobBoss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Boss_img, (140, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = WIDTH / 2
        lastx = self.rect.x
        self.rect.y = random.randrange(30, 300)
        lasty = self.rect.y
        self.speedy = 0
        self.speedx = 0
        self.move = 0
        self.move_speed = 1
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.speedx == 0 or self.speedx < -1 or self.speedx > 1:
            self.speedx = random.randrange(-1, 1)

        if self.rect.x == WIDTH - 600:
            self.speedx = self.speedx * -1
            self.shooting()

        if self.rect.x == WIDTH - 500:
            self.speedx = self.speedx * -1
            self.shooting()

        if self.rect.right > WIDTH:  # or self.rect.left<0:
            self.speedx = self.speedx - 1
            self.shooting()

        if self.rect.left < 0:
            self.speedx = self.speedx + 1
            self.shooting()

    def shooting(self):
        for i in range(4):
            enemybullet = Bullet(
                self.rect.centerx - 5 + i * 22,
                self.rect.top,
                speedy=3,
                bullet_img=enemy_bullet_img,
            )
            all_sprites.add(enemybullet)
            enemybullets.add(enemybullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(
            random.choice(enemy_images), (50, 30)
        )
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.x = random.randrange(30, WIDTH - 60)
        self.rect.y = random.randrange(30, 300)
        self.speedy = 0
        self.speedx = 0
        self.move = 0
        self.move_speed = 1
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = random.randrange(1700, 2500)
        self.last_shot = pygame.time.get_ticks()
        self.health = 2
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx == 0 or self.speedx < -1 or self.speedx > 1:
            self.speedx = random.randrange(-1, 1)
        # T = tymczasowa zmienna pozycji
        T = self.rect.x
        if (
            T == WIDTH - 495
            or T == WIDTH - 470
            or T == WIDTH - 445
            or T == WIDTH - 420
            or T == WIDTH - 395
            or T == WIDTH - 370
        ):
            self.speedx = self.speedx * -1
            self.shooting()
        if (
            T == WIDTH - 350
            or T == WIDTH - 325
            or T == WIDTH - 300
            or T == WIDTH - 275
            or T == WIDTH - 250
            or T == WIDTH - 225
            or T == WIDTH - 200
        ):
            self.speedx = self.speedx * -1
            self.shooting()
        if (
            T == WIDTH - 175
            or T == WIDTH - 150
            or T == WIDTH - 125
            or T == WIDTH - 100
            or T == WIDTH - 75
            or T == WIDTH - 50
            or T == WIDTH - 25
        ):
            self.speedx = self.speedx * -1
            self.shooting()
        if (
            T == WIDTH - 520
            or T == WIDTH - 545
            or T == WIDTH - 570
            or T == WIDTH - 595
            or T == WIDTH - 620
            or T == WIDTH - 645
            or T == WIDTH - 670
        ):
            self.speedx = self.speedx * -1
            self.shooting()
        if (
            T == WIDTH - 705
            or T == WIDTH - 730
            or T == WIDTH - 755
            or T == WIDTH - 780
            or T == WIDTH - 805
            or T == WIDTH - 830
            or T == WIDTH - 860
            or T == WIDTH - 890
            or T == WIDTH - 920
            or T == WIDTH - 950
            or T == WIDTH - 980
        ):
            self.speedx = self.speedx * -1
            self.shooting()
        if self.rect.right > WIDTH:
            self.speedx = self.speedx - 1
            self.shooting()
        if self.rect.left < 0:
            self.speedx = self.speedx + 1
            self.shooting()

    def shooting(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemybullet = Bullet(
                self.rect.centerx, self.rect.top, speedy=3, bullet_img=enemy_bullet_img
            )
            all_sprites.add(enemybullet)
            enemybullets.add(enemybullet)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


def show_menu_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "STARSHIP", 54, WIDTH / 2, HEIGHT / 4)
    draw_text(
        screen,
        "Strzałki - Ruch, Spacja - Strzał, czerwona kapsułka buff ataku, żółta kapsułka buff tarczy",
        20,
        WIDTH / 2,
        HEIGHT / 2,
    )
    draw_text(screen, "Naciśnij by zacząć", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# load all graphs from dirname
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
menu = pygame.image.load(path.join(img_dir, "menu.png")).convert()
menu_rect = menu.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (20, 20))
player_mini_img.set_colorkey(BLACK)
enemy_images = []
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
pow_bullet_img = pygame.image.load(path.join(img_dir, "powb.png")).convert()
Boss_img = pygame.image.load(path.join(img_dir, "enemyRed4.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed08.png")).convert()
enemy_list = ["playerShip1_blue.png", "playerShip1_green.png", "playerShip1_orange.png"]
Shield = pygame.image.load(path.join(img_dir, "HP.png")).convert()
powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(img_dir, "pill_yellow.png"))
powerup_images["gun"] = pygame.image.load(path.join(img_dir, "pill_red.png"))
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    expl_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    expl_anim["sm"].append(img_sm)
    filename = "sonicExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_pl = pygame.transform.scale(img, (110, 110))
    expl_anim["player"].append(img_pl)

tarcza = pygame.transform.scale(Shield, (10, 10))
coin_img = pygame.image.load(path.join(img_dir, "coin.png")).convert()
coin_img = pygame.transform.scale(coin_img, (18, 18))
coin_rect = coin_img.get_rect()
coin_rect.x = WIDTH - 1018
coin_rect.y = HEIGHT - 37
for img in enemy_list:
    enemy_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# load of all sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser.wav"))
hit_sound = pygame.mixer.Sound(path.join(snd_dir, "Hit.wav"))
pygame.mixer.music.load(path.join(snd_dir, "background.ogg"))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
player = StatekGracza()
Bosses = pygame.sprite.Group()
tarcza = draw_pas()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
newboss()
all_sprites.add(player)
all_sprites.add(tarcza)
for i in range(1):
    newmob()

# dynamics
counterboss = 0
counter = 0
counterplayer = 0
score = 0
Health = player.shield
saves = 0
poziom = 0
pygame.mixer.music.play(loops=-1)
# game state first state game menu
game_over = True
# Game loop
saved_states = []
originator = Originator()

running = True
while running:

    keystate = pygame.key.get_pressed()
    if game_over == True:
        show_menu_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = StatekGracza()
        Boss = MobBoss()
        tarcza = draw_pas()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        enemybullets = pygame.sprite.Group()
        all_sprites.add(player)
        player.shield = 100
        Health = player.shield
        all_sprites.add(tarcza)
        for i in range(45):
            newmob()
    # creating memento saves
    if keystate[pygame.K_0]:
        if saves == 1:
            print("none")
            # originator.set("State1")
            # saved_states.append(originator.save_to_memento())
            # saves = saves + 1
        if saves == 2:
            originator.set("State2")
            saved_states.append(originator.save_to_memento())
            saves = saves + 1
        if saves == 3:
            originator.set("State3")
            saved_states.append(originator.save_to_memento())
            saves = saves + 1
        if saves >= 3:
            saves = 0
        originator.restore_from_memento(saved_states[0])
    if keystate[pygame.K_UP]:
        show_menu_screen()

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        counterboss += 50 - hit.radius
        newmob()
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        poziom = poziom + 1
        # if poziom == 35:
        #    Mob.powerup()
        #    poziom = 0
        if random.random() > 0.8:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        if counterboss > 10000:
            newboss()
            counterboss = 0

    # if player hits boss mob
    hits = pygame.sprite.groupcollide(Bosses, bullets, True, True)
    for hit in hits:
        counter += 1
        if counter > 100:
            counter = 0
            newboss()
            counter = counter + 1
            expl = Explosion(hit.rect.center, "lg")
            all_sprites.add(expl)
            score += hit.radius / 2

    # if player hits pow
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield = player.shield + random.randrange(10, 30)
            Health = player.shield
            if player.shield >= 100:
                player.shield = 100
                Health = 100
        if hit.type == "gun":
            player.powerup()
    # if Mob hits player
    hits = pygame.sprite.spritecollide(
        player, enemybullets, True, pygame.sprite.collide_circle
    )
    for hit in hits:
        hit_sound.play()
        player.shield = player.shield - hit.radius * 2
        Health = player.shield
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        if player.shield <= 0:
            death_explosion = Explosion(hit.rect.center, "player")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives = player.lives - 1
            player.shield = 100

    # if player lost all lives:
    if player.lives == 0:  # and not death_explosion.alive():
        game_over = True
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(coin_img, coin_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH - 980, 730)
    draw_shield_bar(screen, WIDTH - 905, 733, Health)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
