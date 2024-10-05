import sys

import pygame

WINDOW_SIZE = (800, 600)
WINDOW_CAPTION = "Other Life"

COLOR_BOARD = (255, 253, 208)
COLOR_LINE = (225, 223, 178)
COLOR_CELL = (125, 100, 255)

SCROLL_SPEED = 3
ZOOM_SPEED = 0.1

TURN_DELAY_MS = 1000

CELL_SIZE = 10
UVX_DIR = 1
UVY_DIR = -1


class Board:
    __dx = 0
    __dy = 0
    __zoom_factor = 1.0

    def __init__(self, screen):
        self.__screen = screen

    def __cell_size(self):
        return max(1, int(CELL_SIZE * self.__zoom_factor))

    def transform_to_cell(self, uv, x, y):
        uvx, uvy = uv
        i = UVX_DIR * (x + self.__dx - uvx) // self.__cell_size()
        j = UVY_DIR * (y + self.__dy - uvy) // self.__cell_size()
        return i, j

    def transform_to_screen(self, uv, i, j):
        uvx, uvy = uv
        x = (uvx + UVX_DIR * i * self.__cell_size()) - self.__dx
        y = (uvy + UVY_DIR * j * self.__cell_size()) - self.__dy
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
                (x - self.__cell_size() // 2, 0),
                (x - self.__cell_size() // 2, height),
            )
        for j in rj:
            x, y = self.transform_to_screen(uv, 0, j)
            pygame.draw.line(
                self.__screen,
                COLOR_LINE,
                (0, y - self.__cell_size() // 2),
                (width, y - self.__cell_size() // 2),
            )

        for c in cells:
            x, y = self.transform_to_screen(uv, c[0], c[1])
            pygame.draw.circle(
                self.__screen,
                COLOR_CELL,
                (x, y),
                0.9 * self.__cell_size() // 2,
            )

    def move(self, dx, dy):
        self.__dx += dx * SCROLL_SPEED
        self.__dy -= dy * SCROLL_SPEED

    def zoom(self, y):
        if y < 0:
            self.__zoom_factor += ZOOM_SPEED
        else:
            self.__zoom_factor = max(self.__zoom_factor - ZOOM_SPEED, 3 / CELL_SIZE)


class Game1:
    def __init__(self):
        self.__state = [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5)]

    def get_state(self):
        return self.__state

    def turn(self):
        new_state = []
        for c in self.__state:
            i, j = c
            new_state.append((-j, i))
        self.__state = new_state


def render_text(text, font, color, surface, x, y):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 16)

    board = Board(screen)
    game = Game1()

    time_since_last_turn = 0
    while True:
        dt = clock.tick(240)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    board.zoom(event.y)
                else:
                    board.move(event.x, event.y)

        board.draw(game.get_state())

        time_since_last_turn += dt
        if time_since_last_turn >= TURN_DELAY_MS:
            game.turn()
            time_since_last_turn = 0

        fps = clock.get_fps()
        text = f"fps: {int(fps)}"
        render_text(text, font, (0, 0, 0), screen, 10, 10)

        pygame.display.flip()


if __name__ == "__main__":
    main()
