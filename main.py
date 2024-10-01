import sys
import pygame

WINDOW_SIZE = (800, 600)
WINDOW_CAPTION = "Other Life"

COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            width, height = pygame.display.get_surface().get_size()

            screen.fill((255, 255, 255))
            pygame.draw.circle(screen, COLOR_BLUE, (width // 2, height // 2), 50)

            pygame.display.flip()


if __name__ == "__main__":
    main()
