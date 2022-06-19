import pygame


class Ship:
    def __init__(self):
        self.img = pygame.image.load("ship.png")
        self.rect = self.img.get_rect()
        self.rect.x = 370
        self.rect.y = 500
        self.change = 0

    def position_x(self):
        return self.rect.x

    def return_rect(self):
        return self.rect

    def draw(self, win):
        win.blit(self.img, self.rect)

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change = -6

            if event.key == pygame.K_RIGHT:
                self.change = 6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.change = 0

    def move(self):
        self.rect.x += self.change

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 736:
            self.rect.x = 736

    def collision(self, enemy_rect):
        if self.rect.colliderect(enemy_rect):
            return True

        return False


class Bullet:
    def __init__(self):
        self.img = pygame.image.load("bullet.png")
        self.rect = self.img.get_rect()
        self.rect.x = 0
        self.rect.y = 480
        self.y_change = 10
        self.fired = False

    def fire(self, win):
        self.fired = True
        win.blit(self.img, (self.rect.x + 23, self.rect.y + 12))

    def check(self, event, ship_x, win):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.fired is False:
                self.rect.x = ship_x
                self.fire(win)

    def move(self, win):
        if self.fired is True:
            self.fire(win)
            self.rect.y -= self.y_change

        if self.rect.y <= -10:
            self.fired = False
            self.rect.y = 480

    def collision(self, enemy_rect):
        if self.rect.colliderect(enemy_rect):
            self.rect.y = 480
            self.fired = False
            return True
        else:
            return False

