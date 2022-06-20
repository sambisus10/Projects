import pygame
from typing import List
from random import randint
import menu
from ship import Ship, Bullet
from enemy import Enemy, EnemyBullet

WIN_WIDTH = 800
WIN_HEIGHT = 600
TICK = 45

NUMBER_OF_ENEMIES = 7
NUMBER_OF_ENEMY_BULLETS = 8


def create_enemies():
    return [Enemy(j * 64, i * 64) for j in range(NUMBER_OF_ENEMIES)
            for i in range(NUMBER_OF_ENEMIES // 2)]


def create_enemy_bullets():
    return [EnemyBullet() for _ in range(NUMBER_OF_ENEMY_BULLETS)]


def check_event(bullet: Bullet, ship: Ship, win):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        ship.check(event)
        bullet.check(event, ship.position_x(), win)

    return True


def manage_enemies(enemies: List[Enemy], win, ship: Ship, bullet: Bullet,
                   enemy_bullets: List[EnemyBullet]) -> List[Enemy]:
    enemies_copy = enemies.copy()
    for i in range(len(enemies)):
        if enemies[i].move_x():
            for j in range(len(enemies)):
                enemies[j].move_y()

        enemies[i].draw(win)
        pos_x, pos_y = enemies[i].get_position()
        enemy_rect = enemies[i].return_rect()

        if bullet.collision(enemy_rect):
            enemies_copy.remove(enemies[i])

        if ship.collision(enemy_rect):
            menu.main_menu()

        num = len(enemies) if len(enemies) <= 16 else 16

        if i >= len(enemies) - num and i % 2 == 0:
            enemy_bullet = enemy_bullets[(len(enemies) - i - 1) // 2]
            if randint(1, 150) == 1 and not enemy_bullet.return_state():
                enemy_bullet.shoot(pos_x, pos_y)

    return enemies_copy


def manage_enemy_bullets(ship: Ship, enemy_bullets: List[EnemyBullet], win):
    for i in range(NUMBER_OF_ENEMY_BULLETS):
        enemy_bullet = enemy_bullets[i]
        if enemy_bullet.return_state():
            enemy_bullet.move(win)

        if enemy_bullet.collision(ship.return_rect()):
            menu.main_menu()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    ship = Ship()
    bullet = Bullet()
    enemies = create_enemies()
    enemy_bullets = create_enemy_bullets()

    while True:
        clock.tick(TICK)
        win.fill((0, 0, 0))

        if not check_event(bullet, ship, win):
            return None

        ship.move()
        ship.draw(win)
        enemies = manage_enemies(enemies, win, ship, bullet, enemy_bullets)

        if not enemies:
            menu.main_menu()

        manage_enemy_bullets(ship, enemy_bullets, win)
        bullet.move(win)
        pygame.display.update()


if __name__ == "__main__":
    menu.main_menu()
