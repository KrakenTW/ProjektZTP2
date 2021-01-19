import pygame
import random
import time
from os import X_OK, path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'dźwięki')

WIDTH = 1024
HEIGHT = 768
FPS = 150

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SCOREBOARD = (250, 0 ,255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Statki")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, SCOREBOARD)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class draw_pas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Shield,(20,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 940
        self.rect.y = HEIGHT - 37
        #self.second_image = pygame.transform.scale(coin_img, (20,20))
        #self.second_image.set_colorkey(BLACK)
        #self.rect = self.second_image.get_rect()
        #self.rect.x = WIDTH - 990
        #self.rect.y = HEIGHT - 37
class spawn_bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Boss_img, (140, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = WIDTH /2
        self.rect.y = random.randrange(30, 300)
        self.speedy = 0
        self.speedx = 0
        self.move = 0 
        self.move_speed = 1
        self.last_update = pygame.time.get_ticks()

class StatekGracza(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70,45) )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 14 
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.last_update = pygame.time.get_ticks()
        self.shield = 100

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right>WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0
    

        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class MobBoss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Boss_img, (140, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = WIDTH /2
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

        if self.rect.right>WIDTH :#or self.rect.left<0:
            self.speedx = self.speedx  -1
            self.shooting()

        if self.rect.left < 0 :
            self.speedx = self.speedx  +1
            self.shooting()
    def shooting(self):
        enemybullet = EnemyBullet(self.rect.centerx, self.rect.top )
        all_sprites.add(enemybullet)
        enemybullets.add(enemybullet)
        


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(random.choice(enemy_images), (50,30))
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.x = random.randrange(0,WIDTH)
        self.rect.y = random.randrange(30, 300)
        self.speedy = 0
        self.speedx = 0
        self.move = 0 
        self.move_speed = 1
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx == 0 or self.speedx < -1 or self.speedx > 1:
            self.speedx = random.randrange(-1, 1)

        if self.rect.x == WIDTH - 495:
            self.speedx = self.speedx * -1
            self.shooting()
        if self.rect.x == WIDTH - 350:
            self.speedx = self.speedx * -1
            self.shooting()
        
        if self.rect.right>WIDTH :
            self.speedx = self.speedx  -1
            self.shooting()

        if self.rect.left < 0 :
            self.speedx = self.speedx  +1
            self.shooting()

    def shooting(self):
        enemybullet = EnemyBullet(self.rect.centerx, self.rect.top )
        all_sprites.add(enemybullet)
        enemybullets.add(enemybullet)
        
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, ( 10, 20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.65)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -4 

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_bullet_img, (10,20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.65)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5  

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 :
            self.kill()

            
#load all graphs from dirname
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
enemy_images = [] 
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
Boss_img = pygame.image.load(path.join(img_dir, "enemyRed4.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed08.png")).convert()
enemy_list = ['playerShip1_blue.png', 'playerShip1_green.png', 'playerShip1_orange.png']
Shield = pygame.image.load(path.join(img_dir, 'HP.png')).convert()

coin_img = pygame.image.load(path.join(img_dir, 'coin.png')).convert()
coin_img = pygame.transform.scale(coin_img, (18,18))
coin_rect = coin_img.get_rect()
coin_rect.x = WIDTH - 1018
coin_rect.y = HEIGHT - 37
for img in enemy_list:
    enemy_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#load of all sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser.wav'))
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hit.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'background.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
tarcza = pygame.transform.scale(Shield, (10,10))
player = StatekGracza()
Boss = MobBoss()
tarcza = draw_pas()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(tarcza)
for i in range(15 ):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#dynamics
counterboss = 0
counter = 0
counterplayer = 0
score = 0
Health = player.shield


pygame.mixer.music.play(loops = -1)

# Game loop
running = True
while running:
    
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False         
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame. K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    #if bullet killed mob 
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)  
    for hit in hits:
        score += 50 - hit.radius
        counterboss += 50 - hit.radius
        newmob()
    if counterboss > 100:
            all_sprites.add(Boss)
            counterboss = 0    

    #if player hits boss mob
    hits = pygame.sprite.spritecollide(Boss, bullets, True)
    for hit in hits:        
        counter = counter + 1
        if counter == 15:
            score += hit.radius /2 
            Boss.kill()
            bonus = spawn_bonus()
            all_sprites.add(bonus)

    #if Mob hits player
    hits = pygame.sprite.spritecollide(player, enemybullets, True, pygame.sprite.collide_circle)
    for hit in hits: 
        hit_sound.play()
        player.shield = player.shield - hit.radius *2
        Health = player.shield  
        if player.shield < 0:
            running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(coin_img, coin_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(Health), 18, WIDTH - 890, 730) 
    draw_text(screen, str(score), 18, WIDTH - 980, 730)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()