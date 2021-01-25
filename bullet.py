import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.65)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    def notify_sprite_groups(self):
        all_sprites.add(self)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
