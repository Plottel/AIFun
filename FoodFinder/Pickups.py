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

    def __init__(self):
        self.x = random.randint(0, Renderer.SCREEN_WIDTH)
        self.y = random.randint(0, Renderer.SCREEN_HEIGHT)
        self.size = 3

    def render(self):
        pygame.draw.rect(Renderer.SCREEN, (10, 10, 10), self.rect, 0)
