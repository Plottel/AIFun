# Test comment

import pygame
from pygame.rect import Rect
from Renderer import Renderer
from TileInteractor import TileInteractor
import Input


class Entity:
    path = []
    speed = 1
    dx = 0
    dy = 0
    x = 0
    y = 0
    width = 25
    height = 25
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

        # COLLISION CHECKS

        # Try Left - check top left / bottom left
        if self.dx < 0:
            if TileInteractor.tile_at(self.x + self.dx, self.y).passable:                                   # Top left corner
                if TileInteractor.tile_at(self.x + self.dx, self.y + self.height).passable:                 # Bottom left corner
                    self.x += self.dx
        else: # Try Right - check top right / bottom right
            if TileInteractor.tile_at(self.x + self.dx + self.width, self.y).passable:                      # Top right corner
                if TileInteractor.tile_at(self.x + self.dx + self.width, self.y + self.height).passable:    # Bottom right corner
                    self.x += self.dx

        # Try Up - check top left / top right
        if self.dy < 0:
            if TileInteractor.tile_at(self.x, self.y + self.dy).passable:                                   # Top left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy).passable:                  # Top right corner
                    self.y += self.dy
        else: # Try Down - check bottom left / bottom right
            if TileInteractor.tile_at(self.x, self.y + self.dy + self.height).passable:                     # Bottom left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy + self.height).passable:    # Bottom right corner
                    self.y += self.dy


    def render(self):
        pygame.draw.rect(Renderer.SCREEN, self.color, self.rect, 0)



