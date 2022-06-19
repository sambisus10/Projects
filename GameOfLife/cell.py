import pygame

CELL_SIZE = 10
BLACK = (0, 0, 0)
YELLOW = (250, 250, 0)
WHITE = (230, 230, 230)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE - 1
        self.color = WHITE
        self.state = 0
        self.temp_state = 0

    def draw(self, win, cell_size):
        self.size = cell_size
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.size, self.size))

    def change_state(self):
        self.color = YELLOW if self.state == 0 else WHITE
        self.state = 1 - self.state
        self.temp_state = self.state

    def check_neighbours(self, field, row, col):
        neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not 0 <= row + i <= len(field) - 1 or \
                        not 0 <= col + j <= len(field[0]) - 1:
                    continue

                if i == 0 and j == 0:
                    continue

                if field[row + i][col + j].state == 1:
                    neighbours += 1

        if self.state == 1:
            if neighbours <= 1 or neighbours >= 4:
                self.temp_state = 0
                self.color = WHITE
        else:
            if neighbours == 3:
                self.temp_state = 1
                self.color = YELLOW
