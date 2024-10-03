import sys

import pygame

WINDOW_SIZE = (800, 600)
WINDOW_CAPTION = "Other Life"

COLOR_BOARD = (255, 253, 208)
COLOR_LINE = (225, 223, 178)
COLOR_CELL = (125, 100, 255)

SCROLL_SPEED = 5

CELL_SIZE = 10
UVX_DIR = 1
UVY_DIR = -1


class Board:
    __dx = 0
    __dy = 0

    def __init__(self, screen):
        self.__screen = screen

    def transform_to_cell(self, uv, x, y):
        uvx, uvy = uv
        i = UVX_DIR * (x + self.__dx - uvx) // CELL_SIZE
        j = UVY_DIR * (y + self.__dy - uvy) // CELL_SIZE
        return i, j

    def transform_to_screen(self, uv, i, j):
        uvx, uvy = uv
        x = (uvx + UVX_DIR * i * CELL_SIZE) - self.__dx
        y = (uvy + UVY_DIR * j * CELL_SIZE) - self.__dy
        return x, y

    @staticmethod
    def srange(i, j):
        return range(min(i, j), max(i, j) + 1)

    def draw(self, cells):
        width, height = pygame.display.get_surface().get_size()

        uv = width // 2, height // 2

        vpx1, vpy1 = 0, 0
        vpx2, vpy2 = width, height

        i1, j1 = self.transform_to_cell(uv, vpx1, vpy1)
        i2, j2 = self.transform_to_cell(uv, vpx2, vpy2)

        ri = self.srange(i1, i2)
        rj = self.srange(j1, j2)

        self.__screen.fill(COLOR_BOARD)

        for i in ri:
            x, y = self.transform_to_screen(uv, i, 0)
            pygame.draw.line(
                self.__screen,
                COLOR_LINE,
                (x - CELL_SIZE // 2, 0),
                (x - CELL_SIZE // 2, height),
            )
        for j in rj:
            x, y = self.transform_to_screen(uv, 0, j)
            pygame.draw.line(
                self.__screen,
                COLOR_LINE,
                (0, y - CELL_SIZE // 2),
                (width, y - CELL_SIZE // 2),
            )

        for c in cells:
            x, y = self.transform_to_screen(uv, c[0], c[1])
            pygame.draw.circle(
                self.__screen,
                COLOR_CELL,
                (x, y),
                0.9 * CELL_SIZE // 2,
            )

    def draw_cell(self, cell_x, cell_y, cell_size, width, height):
        pygame.draw.line(
            self.__screen,
            COLOR_LINE,
            (cell_x - cell_size // 2, 0),
            (cell_x - cell_size // 2, height),
        )

        pygame.draw.line(
            self.__screen,
            COLOR_LINE,
            (0, cell_y - cell_size // 2),
            (width, cell_y - cell_size // 2),
        )

    def move(self, dx, dy):
        self.__dx += dx * SCROLL_SPEED
        self.__dy -= dy * SCROLL_SPEED


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    board = Board(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                board.move(event.x, event.y)

        board.draw([(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5)])

        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color("black"))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(240)


if __name__ == "__main__":
    main()
