import sys
import pygame
import pygame.gfxdraw

WINDOW_SIZE = (800, 600)
WINDOW_CAPTION = "Other Life"

COLOR_BOARD = (0, 0, 0)  # (255, 255, 255)
COLOR_LINE = (0, 0, 100)  # (200, 200, 255)
COLOR_CELL = (200, 200, 255)


def normalize_coordinates(uv, screen_size):
    u, v = uv
    screen_width, screen_height = screen_size
    x = int((u + 1) * 0.5 * screen_width)
    y = int((v + 1) * 0.5 * screen_height)
    return x, y


def normalize_size(size, screen_size):
    screen_width, screen_height = screen_size
    return int(size * min(screen_width, screen_height) * 0.5)


class Board:
    __cell_size = 10
    __line_width = 1

    def __init__(self, screen):
        self.__screen = screen

    def draw(self):
        self.__screen.fill(COLOR_BOARD)
        width, height = pygame.display.get_surface().get_size()

        pygame.draw.circle(
            self.__screen,
            COLOR_CELL,
            normalize_coordinates((0, 0), (width, height)),
            normalize_size(0.5, (width, height)),
        )


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    board = Board(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            board.draw()

            pygame.display.flip()


if __name__ == "__main__":
    main()
