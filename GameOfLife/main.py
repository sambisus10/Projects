import pygame
from cell import Cell, CELL_SIZE
from typing import List

WIN_WIDTH = 1600
WIN_HEIGHT = 900


def event_check(field, playing):
    space = playing
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            return False, False

        if event.type == pygame.MOUSEBUTTONDOWN:
            field[pos[0] // CELL_SIZE][pos[1] // CELL_SIZE].change_state()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = not playing

            if event.key == pygame.K_UP:
                pass

            if event.key == pygame.K_DOWN:
                pass

    return True, space


def check_cells(field: List[List[Cell]], space: bool, tick: int, win) -> int:
    for row in range(len(field)):
        for col in range(len(field[row])):
            field[row][col].draw(win, CELL_SIZE)
            if space:
                field[row][col].check_neighbours(field, row, col)
                if tick != 100:
                    tick = 100
            else:
                if tick == 100:
                    tick = 30

    return tick


def main():
    pygame.init()

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Game of Life")

    field = [[Cell(x * CELL_SIZE + 1, y * CELL_SIZE + 1)
              for y in range(WIN_HEIGHT // CELL_SIZE)]
             for x in range(WIN_WIDTH // CELL_SIZE)]

    space = False
    tick = 30
    running = True
    while running:
        clock.tick(tick)
        win.fill((0, 0, 0))

        running, space = event_check(field, space)
        tick = check_cells(field, space, tick, win)

        for row in field:
            for elem in row:
                elem.state = elem.temp_state

        pygame.display.update()


if __name__ == "__main__":
    main()
