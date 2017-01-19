import pygame
from pygame.rect import Rect
from Renderer import Renderer
from TileInteractor import TileInteractor
import Input
from enum import Enum
import GenAlg

class Dir(Enum):
    Left = 1
    Up = 2
    Right = 3
    Down = 4
    NE = 5
    SE = 6
    SW = 7
    NW = 8
    Still = 9


class Entity:
    movement_sequence = []
    last_dir = None

    fitness = 0
    speed = 8
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


    def clear_tiles_visited(self):
        for col in range(TileInteractor.tileset.cols):
            for row in range(TileInteractor.tileset.rows):
                self.tiles_visited[col][row] = 0

    def populate_tiles_visited(self):
        for col in range(TileInteractor.tileset.cols):
            new_col = []
            for row in range(TileInteractor.tileset.rows):
                new_col.append(0)

            self.tiles_visited.append(new_col)


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement_sequence = []
        self.tiles_visited = []
        self.populate_tiles_visited()
        self.successful_moves = 0
        self.direction_changes = 0
        self.time_spent_at_end = 0
        self.last_dir = Dir.Still


    def check_collisions(self):
        # COLLISION CHECKS

        # Try Left - check top left / bottom left
        if self.dx < 0:
            if TileInteractor.tile_at(self.x + self.dx, self.y).passable:  # Top left corner
                if TileInteractor.tile_at(self.x + self.dx, self.y + self.height).passable:  # Bottom left corner
                    self.x += self.dx
        else:  # Try Right - check top right / bottom right
            if TileInteractor.tile_at(self.x + self.dx + self.width, self.y).passable:  # Top right corner
                if TileInteractor.tile_at(self.x + self.dx + self.width,
                                          self.y + self.height).passable:  # Bottom right corner
                    self.x += self.dx

        # Try Up - check top left / top right
        if self.dy < 0:
            if TileInteractor.tile_at(self.x, self.y + self.dy).passable:  # Top left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy).passable:  # Top right corner
                    self.y += self.dy
        else:  # Try Down - check bottom left / bottom right
            if TileInteractor.tile_at(self.x, self.y + self.dy + self.height).passable:  # Bottom left corner
                if TileInteractor.tile_at(self.x + self.width,
                                          self.y + self.dy + self.height).passable:  # Bottom right corner
                    self.y += self.dy


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

        self.check_collisions()

        index = TileInteractor.index_at(self.x + (Renderer.TILE_SIZE / 2), self.y + (Renderer.TILE_SIZE / 2))
        if index == TileInteractor.index_at(GenAlg.end_node.x, GenAlg.end_node.y):
            self.time_spent_at_end += 1
        else:
            self.tiles_visited[index[0]][index[1]] += 1

        # If actually moving
        self.successful_moves += not (self.dx == 0 and self.dy == 0)

        if self.last_dir != self.get_dir():
            self.direction_changes += 1

        self.last_dir = self.get_dir()


    def render(self):
        pygame.draw.rect(Renderer.SCREEN, self.color, self.rect, 0)

    def get_dir(self):
        if self.dy > 0: # Either SE, S, SW
            if self.dx > 0: # SE
                return Dir.SE
            elif self.dx < 0: #SW
                return Dir.SW
            else:
                return Dir.Down
        elif self.dy < 0: # Either NE, N, NW
            if self.dx > 0: # NE
                return Dir.NE
            elif self.dx < 0: # NW
                return Dir.NW
            else:
                return Dir.Up
        else: # DY = 0, therefore Left or Right or no movement
            if self.dx > 0: # Right
                return Dir.Right
            elif self.dx < 0: # Left
                return Dir.Left
            else:
                return Dir.Still



def spawn_entity(entity, spawn_node):
    entity.x = spawn_node.x
    entity.y = spawn_node.y