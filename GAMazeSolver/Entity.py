import pygame
from pygame.rect import Rect
from Renderer import Renderer
from TileInteractor import TileInteractor
import Input
import math

from enum import Enum
import time
import random

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


class GeneData:
    path_sequence = []
    cur_path_index = 0
    sequence_length = 0
    speed = 4

    def __init__(self):
        self.path_sequence = []
        self.cur_path_index = 0
        self.sequence_length = 0
        self.speed = 4

    def next_index(self):
        if self.cur_path_index == self.sequence_length - 1:
            self.cur_path_index = 0
        else:
            self.cur_path_index += 1


class Entity:
    last_dir = None
    adjacent_tiles = {}

    fitness = 0
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
        self.fitness = 0
        self.genes = GeneData()
        self.cur_tile_index = (0, 0)
        self.tiles_visited = []
        self.populate_tiles_visited()
        self.successful_moves = 0
        self.direction_changes = 0
        self.time_spent_at_end = 0
        self.last_dir = Dir.Left
        self.adjacent_tiles = {}

    def check_collisions(self):
        # COLLISION CHECKS
        # This can be cleaned up by measuring position from centre of square.
        # Then it's even no matter which side... current pos + 1/2 size + DX / DY

        # Try Left - check top left / bottom left
        if self.dx < 0:
            if TileInteractor.tile_at(self.x + self.dx, self.y).passable:  # Top left corner
                if TileInteractor.tile_at(self.x + self.dx, self.y + self.height).passable:  # Bottom left corner
                    self.x += self.dx
        else:  # Try Right - check top right / bottom right
            if TileInteractor.tile_at(self.x + self.dx + self.width, self.y).passable:  # Top right corner
                if TileInteractor.tile_at(self.x + self.dx + self.width, self.y + self.height).passable:  # Bottom right corner
                    self.x += self.dx

        # Try Up - check top left / top right
        if self.dy < 0:
            if TileInteractor.tile_at(self.x, self.y + self.dy).passable:  # Top left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy).passable:  # Top right corner
                    self.y += self.dy
        else:  # Try Down - check bottom left / bottom right
            if TileInteractor.tile_at(self.x, self.y + self.dy + self.height).passable:  # Bottom left corner
                if TileInteractor.tile_at(self.x + self.width, self.y + self.dy + self.height).passable:  # Bottom right corner
                    self.y += self.dy

    # Map the movement selection to velocities.
    # This should be a dictionary but is just elif branches to get it up and running.
    def assign_move_velocity(self, dir):
        if dir == Dir.Left:
            self.dx = -self.genes.speed
            self.dy = 0
        elif dir == Dir.Up:
            self.dx = 0
            self.dy = -self.genes.speed
        elif dir == Dir.Right:
            self.dx = self.genes.speed
            self.dy = 0
        elif dir == Dir.Down:
            self.dx = 0
            self.dy = self.genes.speed

    def get_adjacent_tiles(self, cur_tile_index):
        self.adjacent_tiles = {
            Dir.Left: TileInteractor.tileset.tiles[cur_tile_index[0] - 1][cur_tile_index[1]],
            Dir.Right: TileInteractor.tileset.tiles[cur_tile_index[0] + 1][cur_tile_index[1]],
            Dir.Up: TileInteractor.tileset.tiles[cur_tile_index[0]][cur_tile_index[1] - 1],
            Dir.Down: TileInteractor.tileset.tiles[cur_tile_index[0]][cur_tile_index[1] + 1]
        }

    def get_opposite_dir(self):
        if self.last_dir == Dir.Left:
            return Dir.Right
        elif self.last_dir == Dir.Right:
            return Dir.Left
        elif self.last_dir == Dir.Up:
            return Dir.Down
        elif self.last_dir == Dir.Down:
            return Dir.Up

    def check_opp_axis_tiles(self):
        # If moving on X Axis
        if self.last_dir == Dir.Left or self.last_dir == Dir.Right:
            if self.adjacent_tiles[Dir.Up].passable and self.genes.path_sequence[self.genes.cur_path_index]:
                self.genes.next_index()
                return Dir.Up

            # If first opp_axis_tile is no good, move to next index
            self.genes.next_index()

            if self.adjacent_tiles[Dir.Down].passable and self.genes.path_sequence[self.genes.cur_path_index]:
                return Dir.Down

            # If second opp_axis_tile is no good, move to next index and
            # tell calling function to check other tiles
            self.genes.next_index()
            return None

        # If moving on Y axis
        if self.last_dir == Dir.Up or self.last_dir == Dir.Down:
            if self.adjacent_tiles[Dir.Left].passable and self.genes.path_sequence[self.genes.cur_path_index]:
                return Dir.Left

            # If first opp_axis_tile is no good, move to next index
            self.genes.next_index()

            if self.adjacent_tiles[Dir.Right].passable and self.genes.path_sequence[self.genes.cur_path_index]:
                return Dir.Right

            # If second opp_axis_tile is no good, move to next index and
            # tell calling function to check other tiles
            self.genes.next_index()
            return None

    def handle_path_selection(self):
        # Check opposite axis tiles
        new_dir = self.check_opp_axis_tiles()

        # If opp_axis_tiles are no good
        if new_dir is None:
            # Check current direction.
            # Don't need to increment path index because you're following current direction.
            if self.adjacent_tiles[self.last_dir].passable:
                self.assign_move_velocity(self.last_dir)
            # If current direction is blocked, turn around.
            # Don't need to increment path index because turning around does not count as a new path
            else:
                self.assign_move_velocity(self.get_opposite_dir())
        # If we've found a new path to take, travel in that direction
        else:
            self.assign_move_velocity(new_dir)

    # Check if moving Entity size + 1 in each direction still keeps you in the same tile index.
    def fully_in_tile(self, cur_tile_index):
        # West
        if cur_tile_index != TileInteractor.index_at(self.x - 1, self.y):
            return False

        # East
        if cur_tile_index != TileInteractor.index_at(self.x + self.width + 1, self.y):
            return False

        # North
        if cur_tile_index != TileInteractor.index_at(self.x, self.y - 1):
            return False

        # South
        if cur_tile_index != TileInteractor.index_at(self.x, self.y + self.height + 1):
            return False

        return True

    def move(self):
        # If the entity has moved to a new tile, then:
        #   - Get adjacent tiles and handle path selection logic
        #   - Increment the number of times the current tile has been visited
        if self.cur_tile_index != TileInteractor.index_at(self.x, self.y):
            if self.fully_in_tile(TileInteractor.index_at(self.x, self.y)):
                self.cur_tile_index = TileInteractor.index_at(self.x, self.y)
                self.get_adjacent_tiles(self.cur_tile_index)

            # Entity is now on a new tile. Check if a new path is available.
            # If it is, handle the logic for it.
            self.handle_path_selection()

        # If current tile is the end tile, get points.
        # Otherwise, increment the number of times the tile has been visited
        if self.cur_tile_index == TileInteractor.index_at(TileInteractor.end_node.x, TileInteractor.end_node.y):
            self.time_spent_at_end += 1
        else:
            # Don't penalise Entity for standing on the end tile
            # Only move if not currently at the end tile
            self.tiles_visited[self.cur_tile_index[0]][self.cur_tile_index[1]] += 1
            self.check_collisions()

        # If actually moving
        self.successful_moves += not (self.dx == 0 and self.dy == 0)

        if self.last_dir != self.get_dir():
            self.direction_changes += 1

        self.last_dir = self.get_dir()

        if self.dx == 0 and self.dy == 0: #and (not self.cur_tile_index == TileInteractor.index_at(TileInteractor.end_node.x, TileInteractor.end_node.y)):
            print("IM NOT MOVING AND IM NOT ON THE END NODE")

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