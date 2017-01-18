import pygame
from pygame.rect import Rect
from Renderer import Renderer
from TileInteractor import TileInteractor
import Input



class Move:
    left = False
    right = False
    up = False
    down = False

    def __init__(self, move_sequence):
        self.left = move_sequence[0] > 0.5
        self.up = move_sequence[1] > 0.5
        self.right = move_sequence[2] > 0.5
        self.down = move_sequence[3] > 0.5


class Entity:
    movement_sequence = []

    fitness = 0
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


    def move(self, movement_index):
        # VERTICAL MOVEMENT
        if self.movement_sequence[movement_index].up:
            self.dy = -self.speed

        if self.movement_sequence[movement_index].down:
            self.dy = self.speed

        if self.movement_sequence[movement_index].up & self.movement_sequence[movement_index].down:
            self.dy = 0

        if (not self.movement_sequence[movement_index].up) & (not self.movement_sequence[movement_index].down):
            self.dy = 0

        # HORIZONTAL MOVEMENT
        if self.movement_sequence[movement_index].left:
            self.dx = -self.speed

        if self.movement_sequence[movement_index].right:
            self.dx = self.speed

        if self.movement_sequence[movement_index].left & self.movement_sequence[movement_index].right:
            self.dx = 0

        if (not self.movement_sequence[movement_index].left) & (not self.movement_sequence[movement_index].right):
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



def spawn_entity(entity, spawn_node):
    entity.x = spawn_node.x
    entity.y = spawn_node.y