import math
import random
from Renderer import Renderer
import pygame
from pygame.rect import Rect


class Food:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 9

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, (10, 255, 100), self.rect, 0)


class Pond:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def __init__(self):
        self.x = random.randint(0, Renderer.SCREEN_WIDTH)
        self.y = random.randint(0, Renderer.SCREEN_HEIGHT)
        self.size = 125

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, (0, 100, 255), self.rect, 0)
