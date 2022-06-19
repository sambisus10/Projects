import pygame
import random
import main

DARK_GREY = (200, 200, 200)
LIGHT_GREY = (230, 230, 230)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline,
                             (self.x - 2, self.y - 2, self.width + 4,
                              self.height + 4), 0)

        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True

        return False


class Star:
    def __init__(self):
        self.x = random.randint(1, 799)
        self.y = random.randint(1, 599)
        self.size = random.randint(1, 2)

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255),
                         (self.x, self.y, self.size, self.size))


def check_event(play_button: Button, quit_button: Button):
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_over(pos):
                main.main()

            if quit_button.is_over(pos):
                pygame.quit()
                quit()

        if event.type == pygame.MOUSEMOTION:
            play_button.color = \
                LIGHT_GREY if play_button.is_over(pos) else DARK_GREY

            quit_button.color = \
                LIGHT_GREY if quit_button.is_over(pos) else DARK_GREY


def main_menu():
    pygame.init()
    win = pygame.display.set_mode((main.WIN_WIDTH,
                                   main.WIN_HEIGHT))
    logo = pygame.transform.scale(pygame.image.load("logo.jpg"), (350, 256))
    play_button = Button((200, 200, 200), 300, 300, 200, 70, "Start Game")
    quit_button = Button((200, 200, 200), 300, 400, 200, 70, "Quit")

    stars = [Star() for _ in range(70)]
    while True:
        win.fill((0, 0, 0))
        play_button.draw(win, (0, 0, 0))
        quit_button.draw(win, (0, 0, 0))
        win.blit(logo, (225, 10))

        for i in range(len(stars)):
            stars[i].draw(win)

        check_event(play_button, quit_button)
        pygame.display.update()
