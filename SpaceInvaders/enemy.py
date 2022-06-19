import pygame


class Enemy:
    def __init__(self, x, y):
        self.img = \
            pygame.transform.scale(pygame.image.load("enemy.png"), (32, 32))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = 3
        self.y_change = 35

    def return_rect(self):
        return self.rect

    def get_position(self):
        return self.rect.x, self.rect.y

    def draw(self, win):
        win.blit(self.img, self.rect)

    def move_x(self):
        self.rect.x += self.x_change

        if self.rect.x <= 0 or self.rect.x >= 780:
            return True

        return False

    def move_y(self):
        self.rect.y += self.y_change
        self.x_change = self.x_change * -1

    def corner_enemy_check(self):
        if self.rect.x <= 0 or self.rect.x >= 768:
            return True

        return False


class EnemyBullet:
    def __init__(self):
        self.bullet = pygame.image.load("enemy_bullet.png")
        self.rect = self.bullet.get_rect()
        self.rect.x = -50
        self.rect.y = 0
        self.vel = 5
        self.fired = False

    def return_state(self):
        return self.fired

    def move(self, win):
        self.rect.y += self.vel

        if self.rect.y > 600:
            self.fired = False
            self.rect.x = -50
            self.rect.y = 0

        win.blit(self.bullet, self.rect)

    def shoot(self, enemy_x, enemy_y):
        self.fired = True
        self.rect.x = enemy_x + 15
        self.rect.y = enemy_y + 15

    def collision(self, ship_rect):
        if self.rect.colliderect(ship_rect):
            self.fired = False
            self.rect.x = -50
            self.rect.y = 0
            return True

        return False
