import pygame
from pygame.rect import Rect
from Renderer import Renderer
from TileInteractor import TileInteractor
import Input
from enum import Enum

class Dir(Enum):
    Left = 1
    Up = 2
    Right = 3
    Down = 4


class Entity:
    movement_sequence = []

    fitness = 0
    speed = 4
    dx = 0
    dy = 0
    x = 0
    y = 0
    width = Renderer.TILE_SIZE / 2
    height = Renderer.TILE_SIZE / 2
    color = Renderer.COLOR_BLUE

    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement_sequence = []
        self.distance_travelled = 0


    def move(self, movement_index):
        # VERTICAL MOVEMENT
        if self.movement_sequence[movement_index][Dir.Up]:
            self.dy = -self.speed

        if self.movement_sequence[movement_index][Dir.Down]:
            self.dy = self.speed

        if self.movement_sequence[movement_index][Dir.Up] & self.movement_sequence[movement_index][Dir.Down]:
            self.dy = 0

        if (not self.movement_sequence[movement_index][Dir.Up]) & (not self.movement_sequence[movement_index][Dir.Down]):
            self.dy = 0

        # HORIZONTAL MOVEMENT
        if self.movement_sequence[movement_index][Dir.Left]:
            self.dx = -self.speed

        if self.movement_sequence[movement_index][Dir.Right]:
            self.dx = self.speed

        if self.movement_sequence[movement_index][Dir.Left] & self.movement_sequence[movement_index][Dir.Right]:
            self.dx = 0

        if (not self.movement_sequence[movement_index][Dir.Left]) & (not self.movement_sequence[movement_index][Dir.Right]):
            self.dx = 0

        # COLLISION CHECKS

        # Try Left - check top left / bottom left
        if self.dx < 0:
            if TileInteractor.tile_at(self.x + self.dx, self.y).passable:                                   # Top left corner
                if TileInteractor.tile_at(self.x + self.dx, self.y + self.height).passable:                 # Bottom left corner
                    self.x += self.dx
                    self.distance_travelled += self.speed
        else: # Try Right - check top right / bottom right
            if TileInteractor.tile_at(self.x + self.dx + self.width, self.y).passable:                      # Top right corner
                if TileInteractor.tile_at(self.x + self.dx + self.width, self.y + self.height).passable:    # Bottom right corner
                    self.x += self.dx
                    self.distance_travelled += self.speed

        # Try Up - check top left / top right
        if self.dy < 0:
            if TileInteractor.tile_at(self.x, self.y + self.dy).passable:                                   # Top left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy).passable:                  # Top right corner
                    self.y += self.dy
                    self.distance_travelled += self.speed
        else: # Try Down - check bottom left / bottom right
            if TileInteractor.tile_at(self.x, self.y + self.dy + self.height).passable:                     # Bottom left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy + self.height).passable:    # Bottom right corner
                    self.y += self.dy
                    self.distance_travelled += self.speed


    def render(self):
        pygame.draw.rect(Renderer.SCREEN, self.color, self.rect, 0)



def spawn_entity(entity, spawn_node):
    entity.x = spawn_node.x
    entity.y = spawn_node.y