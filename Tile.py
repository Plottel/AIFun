from Renderer import Renderer
import pygame
from pygame.rect import Rect


class Tile:
    x = 0
    y = 0
    passable = True
    width = Renderer.TILE_SIZE
    height = Renderer.TILE_SIZE

    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, Tile.width, Tile.height)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Last argument in draw call is border width
    # 0 border with fills the rectangle, rather than drawing an outline
    def render(self):
        if self.passable:
            pygame.draw.rect(Renderer.SCREEN, Renderer.COLOR_BLACK, self.rect, 1)
        else:
            pygame.draw.rect(Renderer.SCREEN, Renderer.COLOR_BLACK, self.rect, 0)
