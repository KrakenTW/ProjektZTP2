from typing import List

import pygame


class StatekGracza(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 14
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = 0
        self.last_update = pygame.time.get_ticks()
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 65)
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # timeout for powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def move_left(self):
        self.speedx = -5

    def move_right(self):
        self.speedx = 5

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, -4, bullet_img)
            bullets = [bullet]
            if self.power == 1:
                self._add_bullets(bullets)
            if self.power == 2:
                bullet2 = Bullet(self.rect.right, self.rect.top, -4, bullet_img)
                bullets.append(bullet2)
                self._add_bullets(bullets)
            if self.power == 3:
                bullet3 = Bullet(self.rect.centerx, self.rect.top, -4, bullet_img)
                bullets.append(bullet3)
                self._add_bullets(bullets)
            if self.power >= 4:
                bullet4 = Bullet(self.rect.centerx, self.rect.top + 30, -4, bullet_img)
                bullets.append(bullet4)
                self._add_bullets(bulltes)

    def _add_bullets(self, bullets: List):
        all_sprites.add(bullets)
        bullets.add(bullets)
        shoot_sound.play()

    def hide(self):
        # to hide player from bullets
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
