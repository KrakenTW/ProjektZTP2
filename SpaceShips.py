import random
import time
import keyboard
from abc import ABCMeta, abstractmethod
from os import X_OK, path
from threading import Lock, Thread
import py_compile
import pygame

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'dźwięki')

WIDTH = 1024
HEIGHT = 768
FPS = 75
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
scoreBOARD = (250, 0 ,255)
         
# Initialize pygame and create window
all_sprites = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # #############
pygame.display.set_caption("Spaceships")     # ############
clock = pygame.time.Clock()     # ############
font_name = pygame.font.match_font('arial')
         
# Load all game graphics
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
enemy_images = []
enemy_list = ['ufoGreen.png', 'ufoRed.png',
                'ufoYellow.png']
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed08.png")).convert()
for img in enemy_list:
    enemy_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    
explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "pill_yellow.png")).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "pill_red.png")).convert()
#dźwięk globalny
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser.wav'))    
    
# Funkcja wyświetla ilość punktów zdobytych przez gracza w określonym przez parametry miejscu
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
# Funkcja wyświetla pasek pasek tarczy na współrzędnych określonych w parametrach oraz
# wypełnia go na zielono częsci podanej w parametrze percent
def draw_shield_bar(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
# Funkcja wyświetla mały obrazek statku w ilości odpowiadającej obecnej ilości szans gracza
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
    
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Spaceshooter", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, Space to fire", 22, WIDTH/2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_shop_screen(poziom):
    screen.blit(background, background_rect)
    draw_text(screen, "SHOP", 72, WIDTH/2, HEIGHT - 680)
    draw_text(screen, "1. Bonus ATK : koszt 3500", 32, WIDTH - 800, HEIGHT- 580)
    draw_text(screen, "2. Bonus HP  : koszt 2750", 32, WIDTH - 800, HEIGHT- 480)
    draw_text(screen, "3. Bonus Live: koszt 6000", 32, WIDTH - 800, HEIGHT- 380)
    draw_text(screen, "4. Poziom +1 : koszt 4500", 32, WIDTH - 800, HEIGHT- 280)
    draw_text(screen, "5. Spawn Boss: koszt 6000", 32, WIDTH - 795, HEIGHT- 180)
    draw_text(screen, "6. Exit  ", 32, WIDTH - 935, HEIGHT- 80)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        if keyboard.is_pressed('1'):
            print("player power is now + 1")
            return 1
        if keyboard.is_pressed('2'):
            print("player shield is now full")
            return 2
        if keyboard.is_pressed('3'):
            print("player lives are now + 1")
            return 3 
        if keyboard.is_pressed('4'):
            print("You leveled up")
            return 4    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False    

class LVLState(metaclass = ABCMeta):
    @abstractmethod
    def changeState(self):
        pass

class TurnedUP(LVLState):
    def changeState(self):
        return "LVL UP"

class TurnedDOWN(LVLState):
    def changeState(self):
        return "LVL DOWN"

class IncreaseLVL(LVLState):
    def changeState(self):
        return "LVL + 1"

class DecreaseLVL(LVLState):
    def changeState(self):
        return "LVL - 1"

class LVLStation(LVLState):
    def __init__(self):
        self.state = None
    
    def setState(self, status):
        self.state = status
    
    def getState(self):
        return self.state
    
    def changeState(self):
        self.state = self.state.changeState()
    
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.RECEIVER = CommandReceiver()
        self.MOVE_RIGHT = MoveRightCommand(self.RECEIVER)
        self.MOVE_LEFT = MoveLeftCommand(self.RECEIVER)
        self.SHOOT = ShootCommand(self.RECEIVER)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
    
    def update(self):
        # Czas trwania mocy po zebraniu obiektu ulepszającego właściwości statku gracza
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # odkrywanie
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
    
        self.speedx = 0
        # Rejestrowanie komend przy użyciu invokera (InputHandler)
        command = InputHandler()
    
        # Wywołanie komend zarejestrowanych przez Invoker (InputHandler)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            command.register("LEFT", self.MOVE_LEFT)
            command.execute("LEFT")
            self.speedx = self.RECEIVER.move_left()
        if keystate[pygame.K_RIGHT]:
            command.register("RIGHT", self.MOVE_RIGHT)
            command.execute("RIGHT")
            self.speedx = self.RECEIVER.move_right()
        if keystate[pygame.K_SPACE]:
            command.register("SHOOT", self.SHOOT)
            command.execute("SHOOT")
            shoot_sound
            if self.RECEIVER.move_right():
                self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.game.all_sprites.add(bullet)
                self.game.bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                shoot_sound.play()
            if self.power == 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.all_sprites.add(bullet3)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                self.game.bullets.add(bullet3)
                shoot_sound.play()
            if self.power >= 4:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                bullet4 = Bullet(self.rect.left - 50, self.rect.centery)
                bullet5 = Bullet(self.rect.right + 50, self.rect.centery)
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.all_sprites.add(bullet3)
                self.game.all_sprites.add(bullet4)
                self.game.all_sprites.add(bullet5)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                self.game.bullets.add(bullet3)
                self.game.bullets.add(bullet4)
                self.game.bullets.add(bullet5)
                shoot_sound.play()


    def hide(self):
        # tymczasowo ukryj obiekt gracza
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
       
class Action(metaclass=ABCMeta):    # Command interface
    
    @staticmethod
    @abstractmethod
    def execute():
        pass
        
class MoveRightCommand(Action):     # ConcreteCommand
    
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.move_right()
       
class MoveLeftCommand(Action):      # ConcreteCommand
    
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.move_left()
       
class ShootCommand(Action):     # ConcreteCommand
    
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.shoot()
        
class InputHandler: #Invoker
    
    def __init__(self):
        self._commands = {}
        self._history = []
    
    @property
    def history(self):
        return self._history
    
    def register(self, command_name, command):
        self._commands[command_name] = command
    
    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._history.append((time.time(), command_name))
            self._commands[command_name].execute()
        else:
            print(f"Command [{command_name}] not recognised")
       
class CommandReceiver:  # Receiver
    
    def move_right(self):
        # print("moved right")
        return 8
    
    def move_left(self):
        # print("moved left")
        return -8
    
    def shoot(self):
        # print("bullet shot")
        return True
        
def new_asteroid(all_sprites, asteroids):
    
    chosen_move_strategy = random.randrange(0, 3)
    strategy_type = None
    
    if chosen_move_strategy == 0:
        strategy_type = XShiftStrategy()
    elif chosen_move_strategy == 1:
        strategy_type = StraightAtPlayerStrategy()
    elif chosen_move_strategy == 2:
        strategy_type = RotationStrategy()
    
    a = Asteroid(strategy_type)
    # a.set_strategy(strategy_type)
    # print(a.get_strategy())
    
    all_sprites.add(a)
    asteroids.add(a)
    
    return all_sprites, asteroids

def new_mob(all_sprites, mobs):
    chosen_move_strategy = random.randrange(0,3)
    strategy_type = None

    if(chosen_move_strategy == 0):
        strategy_type = LVL1Strategy()
    elif chosen_move_strategy == 1:
        strategy_type = LVL2Strategy()
    elif chosen_move_strategy == 2:
        strategy_type = LVL3Strategy()  

    m = Mob(strategy_type) 
    all_sprites.add(m)
    mobs.add(m) 
   
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, strategy):
        self._strategy = strategy
        pygame.sprite.Sprite.__init__(self)
        self.STATE = LVLStation()
        self.InitialLVL = TurnedUP()
        self.IncreaseInitLVL = IncreaseLVL()
        self.RECEIVER = CommandReceiver()
        self.MOVE_RIGHT = MoveRightCommand(self.RECEIVER)
        self.MOVE_LEFT = MoveLeftCommand(self.RECEIVER)
        self.SHOOT = ShootCommand(self.RECEIVER)
        self.image_original = pygame.transform.scale(random.choice(enemy_images),(50,30))
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(30, WIDTH - 60) #
        self.rect.y = random.randrange(30, 300) #
        self.moves = 1
        self.speedy = 1 #random.randrange(1, 8) #
        self.speedx = 1 #random.randrange(-3, 3) #
        self.move = 2
        self.move_speed = 1
        self.rotation = 0
        self.rotation_speed = 8#random.randrange(-8, 8) #
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = random.randrange(1700,2500)
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.move_time = pygame.time.get_ticks()
        self.move_delay = 1500


    def LVLUP(self):
        LVL = LVLStation()
        print("The LVL state is currently: {}".format(LVL.getState()))

        ON = TurnedUP()
        OFF = TurnedDOWN()

        print("Turning on ")
        LVL.setState(ON)
        LVL.changeState()
        print("The LVL state is currently: {}".format(LVL.getState()))

    def get_strategy(self):
        return self._strategy
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def update(self):
        self.rotate()
        self.move_strategy()
        self.rect.x += self.speedx * self.power
        self.rect.y += self.speedy * self.power
        if self.speedx == 0 or self.speedx < -1 or self.speedx > 1:
            self.speedx = random.randrange(-1, 1)
        # MOB
        T = self.rect.x
        if (T == WIDTH - 495 or T == WIDTH - 470 
        or T == WIDTH - 445 or T == WIDTH - 420 
        or T == WIDTH - 395 or T == WIDTH - 370):
            self.speedx = self.speedx * -1
            self.shoot()
            
        if (T == WIDTH - 350 or T == WIDTH - 325 
            or T == WIDTH - 300 or T == WIDTH - 275 
            or T == WIDTH - 250 or T == WIDTH - 225 
            or T == WIDTH - 200):
            self.speedx = self.speedx * -1
            self.shoot()
            
        if (T == WIDTH - 175 or T == WIDTH - 150 
        or T == WIDTH - 125 or T == WIDTH - 100 
        or T == WIDTH - 75 or T == WIDTH - 50 
        or T == WIDTH - 25):
            self.speedx = self.speedx * -1
            
        if (T == WIDTH - 520 or T == WIDTH - 545 
        or T == WIDTH - 570 or T == WIDTH - 595 
        or T == WIDTH - 620 or T == WIDTH - 645 
        or T == WIDTH - 670):
            self.speedx = self.speedx * -1
            
        if (T == WIDTH - 705 or T == WIDTH - 730 
        or T == WIDTH - 755 or T == WIDTH - 780 
        or T == WIDTH - 805 or T == WIDTH - 830 
        or T == WIDTH - 860 or T == WIDTH - 890 
        or T == WIDTH - 920 or T == WIDTH - 950 
        or T == WIDTH - 980):
            self.speedx = self.speedx * -1
            
        if self.rect.right>WIDTH :
            self.speedx = self.speedx  -1
            
        if self.rect.left < 0 :
            self.speedx = self.speedx  +1
        if self.rect.y >= HEIGHT + 45 or self.rect.y <= HEIGHT - 760:
            self.speedy = self.speedy *-1.2
            if self.speedy > 9:
                self.speedy = 2    

    def move_strategy(self):
        self._strategy.move_strategy()
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemybullet = EnemyBullet(self.rect.x, self.rect.y)
            all_sprites.add(enemybullet)
            enemybullets.add(enemybullet)
    
class Mob(pygame.sprite.Sprite):
    def __init__(self,strategy,game):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.scale(random.choice(enemy_images), (50,30))
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
        self.shoot_delay = random.randrange(700,1500)
        self.last_shot = pygame.time.get_ticks()
        self.Health = 2
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx == 0 or self.speedx < -1 or self.speedx > 1:
            self.speedx = random.randrange(-1, 1)
        # T = tymczasowa zmienna pozycji
        T = self.rect.x
        if (T == WIDTH - 495 or T == WIDTH - 470 
        or T == WIDTH - 445 or T == WIDTH - 420 
        or T == WIDTH - 395 or T == WIDTH - 370):
            self.speedx = self.speedx * -1
            self.shooting()
        if (T == WIDTH - 350 or T == WIDTH - 325 
            or T == WIDTH - 300 or T == WIDTH - 275 
            or T == WIDTH - 250 or T == WIDTH - 225 
            or T == WIDTH - 200):
            self.speedx = self.speedx * -1
            self.shooting()
        if (T == WIDTH - 175 or T == WIDTH - 150 
        or T == WIDTH - 125 or T == WIDTH - 100 
        or T == WIDTH - 75 or T == WIDTH - 50 
        or T == WIDTH - 25):
            self.speedx = self.speedx * -1
            self.shooting()
        if (T == WIDTH - 520 or T == WIDTH - 545 
        or T == WIDTH - 570 or T == WIDTH - 595 
        or T == WIDTH - 620 or T == WIDTH - 645 
        or T == WIDTH - 670):
            self.speedx = self.speedx * -1
            self.shooting()
        if (T == WIDTH - 705 or T == WIDTH - 730 
        or T == WIDTH - 755 or T == WIDTH - 780 
        or T == WIDTH - 805 or T == WIDTH - 830 
        or T == WIDTH - 860 or T == WIDTH - 890 
        or T == WIDTH - 920 or T == WIDTH - 950 
        or T == WIDTH - 980):
            self.speedx = self.speedx * -1
            self.shooting()
        if self.rect.right>WIDTH :
            self.speedx = self.speedx  -1
            self.shooting()
        if self.rect.left < 0 :
            self.speedx = self.speedx  +1
            self.shooting()

    def shooting(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now         
            enemybullet = EnemyBullet(self.rect.centerx, self.rect.top )
            self.all_sprites.add(enemybullet)
            enemybullets.add(enemybullet)   

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()    

class Strategy(metaclass=ABCMeta):
    
    @abstractmethod
    def move_strategy(self):
        pass
        print("Error: Strategy not chosen")
        
class XShiftStrategy(Strategy):
    def move_strategy(self):
        pass
        print("XShiftStrategy")
      
class StraightAtPlayerStrategy(Strategy):
    def move_strategy(self):
        pass
        print("StraightAtPlayerStrategy")
        
class RotationStrategy(Strategy):
    def move_strategy(self):
        pass
        print("RotationStrategy")

class LVL1Strategy(Strategy):
    def move_strategy(self):
        pass
        print("LVL1Strategy")

class LVL2Strategy(Strategy):
    def move_strategy(self):
        pass
        print("LVL2Strategy")

class LVL3Strategy(Strategy):
    def move_strategy(self):
        pass
        print("LVL3Strategy")    
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_bullet_img, (10,20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.65)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 3  

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the bottom of the screen
        if self.rect.bottom < 0 :
            self.kill()  
    
class PowerupObject(pygame.sprite.Sprite):
    def __init__(self, center, power_type):
        pygame.sprite.Sprite.__init__(self)
        self.type = power_type
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 0
    
    def get_speedy(self):
        return self.speedy
    
    def get_center(self):
        return self.rect.center
    
    def get_power_type(self):
        return self.type
        
class PowerupType(pygame.sprite.Sprite):
    def __init__(self, powerup):
        self.powerup = powerup
    
    def get_speedy(self):
        return self.powerup.get_speedy()
    
    def get_center(self):
        return self.powerup.get_center()
    
    def get_power_type(self):
        return self.powerup.get_power_type()
        
class Powerup(PowerupType):
    def __init__(self, powerup):
        pygame.sprite.Sprite.__init__(self)
        super(Powerup, self).__init__(powerup)
        self.type = self.get_power_type()
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.get_center()
        self.speedy = self.get_speedy()
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()
    
    def get_speedy(self):
        return super(Powerup, self).get_speedy()
    
    def get_center(self):
        return super(Powerup, self).get_center()
    
    def get_power_type(self):
        return super(Powerup, self).get_power_type()
        
class RestoreShield(PowerupType):
    
    def __init__(self, powerup):
        super(RestoreShield, self).__init__(powerup)
    
    def get_speedy(self):
        return super(RestoreShield, self).get_speedy() + 2
    
    def get_center(self):
        return super(RestoreShield, self).get_center()
    
    def get_power_type(self):
        return super(RestoreShield, self).get_power_type()
       
class UpgradeBullet(PowerupType):
    
    def __init__(self, powerup):
        super(UpgradeBullet, self).__init__(powerup)
    
    def get_speedy(self):
        return super(UpgradeBullet, self).get_speedy() + 4
    
    def get_center(self):
        return super(UpgradeBullet, self).get_center()
    
    def get_power_type(self):
        return super(UpgradeBullet, self).get_power_type()
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self. image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        
class Game:
    #load of all sounds
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser.wav'))
    pygame.mixer.music.load(path.join(snd_dir, 'background.ogg'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops = -1)
    __instance = None
    
    def __init__(self, arg):
        if not Game.__instance:
            Game.__instance = Game.__Game(arg)
    
        else:
            Game.__instance.test = arg
    
    def __getattr__(self, name):
        return getattr(self.__instance, name)
    
    class __Game:
    
        def __init__(self, test):
            self.test = test
            self.running = True
            self.game_over = True
            self.all_sprites = None
            self.asteroids = None
            self.mobs = None
            self.bullets = None
            self.powerups = None
            self.hits = None
            self.score = 0
            self.scoreLVLUP = 0
            self.pow = None
            self.action = InputHandler()
            self.poziom = 0
            self.hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hit.wav'))

        def play(self):
            while self.running:
                
                if self.game_over:
                    show_go_screen()
                    self.game_over = False
    
                    self.all_sprites = pygame.sprite.Group()
                    self.asteroids = pygame.sprite.Group()
                    self.bullets = pygame.sprite.Group()
                    self.enemybullets = pygame.sprite.Group()
                    self.powerups = pygame.sprite.Group()
                    self.mobs = pygame.sprite.Group()
    
                    player = Player(Game(True))
                    self.all_sprites.add(player)
                    for i in range(22):
                        self.all_sprites, self.asteroids = new_asteroid(self.all_sprites, self.asteroids)
                    #for i in range(5):
                    #    self.all_sprites, self.mobs = new_mob(self.all_sprites, self.mobs)
                if keyboard.is_pressed('p'):
                    print("You entered shop")
                    zakup = show_shop_screen(self.poziom)
                    if zakup == 1 and self.score>= 150 and player.power<5:
                        player.powerup()
                        self.score = self.score - 150
                    if zakup == 2 and self.score >=100 and player.shield <100:
                        player.shield = 100
                        self.score = self.score - 100
                    if zakup == 3 and self.score >= 200 and player.lives < 3:
                        self.score = self.score - 200
                        player.lives += 1
                    if zakup == 4:
                        Asteroid.LVLUP()
                        self.score -= 450
    
                    # keep loop running at the right speed
                clock.tick(FPS)
                # Process input (events)
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.running = False
    
                # Update
                self.all_sprites.update()

                #check if player has enough points collected to LVL up
                if self.scoreLVLUP >= 4000:
                    print(self.scoreLVLUP)
                    Asteroid.LVLUP(self)
                    self.scoreLVLUP = 0
                    print(self.scoreLVLUP)
                #check if playser was hitted by enemybullet
                self.hits = pygame.sprite.spritecollide(player, enemybullets, True, pygame.sprite.collide_circle)
                for hit in self.hits: 
                    self.hit_sound.play()
                    player.shield = player.shield - hit.radius *2
                    self.Health = player.shield
                    expl = Explosion(hit.rect.center, 'sm')
                    self.all_sprites.add(expl)  
                    if player.shield <= 0:
                        death_explosion = Explosion(hit.rect.center, 'player')
                        self.all_sprites.add(death_explosion)
                        player.hide()
                        player.lives = player.lives - 1
                        player.shield = 100
                # check to see if a bullet hit the mob
                self.hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
                for hit in self.hits:
                    self.score += 50 - hit.radius
                    self.scoreLVLUP += 50 - hit.radius
                    self.hit_sound.play()
                    expl = Explosion(hit.rect.center, 'lg')
                    self.all_sprites.add(expl)
                    power_type = random.choice(['shield', 'gun'])
                    if random.random() > 0.9:  # chance for powerup dropped by asteroid
                        if power_type == 'shield':
                            self.pow = Powerup((RestoreShield((PowerupObject(hit.rect.center, power_type)), )), )
                        elif power_type == 'gun':
                            self.pow = Powerup((UpgradeBullet((PowerupObject(hit.rect.center, power_type)), )), )
                        self.all_sprites.add(self.pow)
                        self.powerups.add(self.pow)
                    self.all_sprites, self.asteroids = new_asteroid(self.all_sprites, self.asteroids)
    
                # check to see if a mob hit the player
                self.hits = pygame.sprite.spritecollide(player, self.asteroids, True, pygame.sprite.collide_circle)
    
                for hit in self.hits:
                    player.shield -= hit.radius * 2
                    self.hit_sound.play()
                    expl = Explosion(hit.rect.center, 'sm')
                    self.all_sprites.add(expl)
                    self.all_sprites, self.asteroids = new_asteroid(self.all_sprites, self.asteroids)
    
                    if player.shield <= 0:
                        death_explosion = Explosion(player.rect.center, 'player')
                        self.all_sprites.add(death_explosion)
                        player.hide()
                        player.lives -= 1
                        player.shield = 100
    
                # sprawdź czy gracz zebrał bonus
                self.hits = pygame.sprite.spritecollide(player, self.powerups, True)
                for hit in self.hits:
                    if hit.type == 'shield':
                        player.shield += random.randrange(10, 30)
                        if player.shield >= 100:
                            player.shield = 100
                    if hit.type == 'gun':
                        player.powerup()
    
                # if player died and explosion has finished playing
                if player.lives == 0 and not death_explosion.alive():
                    self.game_over = True
                # Draw / render
                screen.fill(BLACK)
                screen.blit(background, background_rect)
                self.all_sprites.draw(screen)
                draw_text(screen, str(self.score), 18, WIDTH / 2, 10)
                draw_shield_bar(screen, 5, 5, player.shield)
                draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
                # *after* drawing everything, flip the display
                pygame.display.flip()
    
            pygame.quit()
        
if __name__ == '__main__':
         
    game1 = Game(True)
    game2 = Game(False)
         
    print(game1._Game__instance)
    print(game2._Game__instance)
         
    if game1._Game__instance == game2._Game__instance:
        print("Referencja identyczna")
    game1.play()
    exit()
         

