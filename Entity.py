import pygame
from pygame.rect import Rect
from Renderer import Renderer
import Input


class Entity:
    path = []
    speed = 1
    dx = 0
    dy = 0
    x = 0
    y = 0
    width = Renderer.TILE_SIZE
    height = Renderer.TILE_SIZE
    color = Renderer.COLOR_BLUE

    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        # VERTICAL MOVEMENT
        if Input.key_down(pygame.K_w):
            self.dy = -self.speed

        if Input.key_down(pygame.K_s):
            self.dy = self.speed

        if Input.key_down(pygame.K_w) & Input.key_down(pygame.K_s):
            self.dy = 0

        if (not Input.key_down(pygame.K_w)) & (not Input.key_down(pygame.K_s)):
            self.dy = 0

        # HORIZONTAL MOVEMENT
        if Input.key_down(pygame.K_a):
            self.dx = -self.speed

        if Input.key_down(pygame.K_d):
            self.dx = self.speed

        if Input.key_down(pygame.K_d) & Input.key_down(pygame.K_a):
            self.dx = 0

        if (not Input.key_down(pygame.K_a)) & (not Input.key_down(pygame.K_d)):
            self.dx = 0

        self.x += self.dx
        self.y += self.dy


    def render(self):
        pygame.draw.rect(Renderer.SCREEN, self.color, self.rect, 0)



