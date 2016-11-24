import pygame


class Renderer:
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    # This is the surface used as the first argument for most drawing methods
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    TILE_SIZE = 32
    COLOR_BLACK = 0, 0, 0
    COLOR_WHITE = 255, 255, 255
    COLOR_BLUE = 0, 0, 255

    @staticmethod
    def clear_screen():
        Renderer.SCREEN.fill(Renderer.COLOR_WHITE)