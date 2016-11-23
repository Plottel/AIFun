from Renderer import Renderer
import pygame
Rect = pygame.Rect


class Tile:
    x = 0
    y = 0
    width = Renderer.TILE_SIZE
    height = Renderer.TILE_SIZE

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, Renderer.COLOR_BLACK, Rect(self.x, self.y, self.width, self.height), 1)
