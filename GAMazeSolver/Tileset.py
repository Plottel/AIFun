import math
import pygame
from pygame.rect import Rect
from Renderer import Renderer
from Tile import Tile
import Input


class Tileset:
    # 2 dimensional list
    # 1st dimension = columns
    # 2nd dimension = rows
    tiles = []
    x = 0
    y = 0
    __cols = 0
    __rows = 0
    show_grid = False

    # Read-only property. Columns can only be added via add_columns()
    @property
    def cols(self):
        return self.__cols

    # Read-only property. Rows can only be added via add_rows()
    @property
    def rows(self):
        return self.__rows

    # Read-only property. Width is derived from number of columns
    @property
    def width(self):
        return self.cols * Renderer.TILE_SIZE - 1

    # Read-only property. Height is derived from number of rows
    @property
    def height(self):
        return self.rows * Renderer.TILE_SIZE - 1

    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    # Initialises the Tileset and adds columns and rows
    def __init__(self, x, y, cols, rows):
        self.x = x
        self.y = y
        self.add_rows(rows)
        self.add_columns(cols)


    def make_border(self):
        for col in range(self.cols):
            for row in range(self.rows):
                if col == 0 or col == self.cols - 1 or row == 0 or row == self.rows - 1:
                    self.tiles[col][row].passable = False
                    self.tiles[col][row].color = Renderer.COLOR_BLACK


    # Returns the Tile at the given coordinates
    def tile_at(self, x, y):
        col = math.floor((x - self.x) / Renderer.TILE_SIZE)
        row = math.floor((y - self.y) / Renderer.TILE_SIZE)

        return self.tiles[col][row]

    # Returns the column and row values of the tile at x, y.
    def index_at(self, x, y):
        col = math.floor((x - self.x) / Renderer.TILE_SIZE)
        row = math.floor((y - self.y) / Renderer.TILE_SIZE)

        return col, row

    # Specifies if the Tileset is at the given coordinates
    # This should always be used before tile_at to prevent clicking outside the grid
    def is_at(self, x, y):
        return self.rect.collidepoint(x, y)

    # Specifies if the Tileset is at the current mouse position
    def is_at_mouse_pos(self):
        return self.is_at(Input.mouse_x(), Input.mouse_y())


    # Returns the Tile at the current mouse position
    def tile_at_mouse_pos(self):
        return self.tile_at(Input.mouse_x(), Input.mouse_y())

    # Adds the number of columns passed in to the Tiles
    # This is done by adding a new list equal to the length of rows
    def add_columns(self, amount_to_add):
        # For each column to be added
        for col in range(amount_to_add):
            new_col = []

            # For each row in the newly created column
            for row in range(self.rows):
                x = self.x + (self.cols * Renderer.TILE_SIZE)
                y = self.y + (row * Renderer.TILE_SIZE)

                # Add new Tile to new column
                new_col.append(Tile(x, y))

            # Add new column to Tiles
            self.tiles.append(new_col)
            self.__cols += 1

    # Adds the number of rows passed in to the Tiles
    # This is done by adding Tiles to the end of each column list
    def add_rows(self, amount_to_add):
        # For each row to be added
        for row in range(amount_to_add):
            # For each column to have a new row added to it
            for col in range(self.cols):
                x = self.x + (col * Renderer.TILE_SIZE)
                y = self.y + (self.rows * Renderer.TILE_SIZE)

                # Add new Tile to the column
                self.tiles[col].append(Tile(x, y))

            self.__rows += 1

    # Renders each Tile in the grid
    def render(self):
        for col in range(self.cols):
            for row in range(self.rows):
                self.tiles[col][row].render()

                if self.show_grid:
                    pygame.draw.rect(Renderer.SCREEN, Renderer.COLOR_BLACK, self.tiles[col][row].rect, 1)
