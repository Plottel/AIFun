import pygame, sys
import Input
from pygame.locals import *
from Renderer import Renderer
from Tileset import Tileset
from pygame.rect import Rect
from TileInteractor import TileInteractor
from Entity import Entity
import GenAlg

from Pathfinder import Pathfinder

# TileInteractor and Renderer and Pathfinder don't need to be classes
# Refactor
# Them
# Just
# Like
# I
# Refactored
# Input


# Clean up collision code - copy from FreedomFighter


# Parses maze.
# Make sure string matches grid
def parse_maze(tileset, maze):
    i = 0
    for row in range(tileset.rows):
        for col in range(tileset.cols):
            # Keep looping through indexes until we find an X or an O
            while maze[i] != "X" and maze[i] != "-":
                i += 1

            if maze[i] == "X":
                tileset.tiles[col][row].color = Renderer.COLOR_BLACK
                tileset.tiles[col][row].passable = False
            elif maze[i] == "-":
                tileset.tiles[col][row].color = (128, 128, 128)
                tileset.tiles[col][row].passable = True

            i += 1

def handle_mouse_input(tileset):
    tile = None

    if tileset.is_at_mouse_pos():
        tile = tileset.tile_at_mouse_pos()

    # Add column to Tileset
    if Input.key_typed(pygame.K_c):
        tileset.add_columns(1)

    # Add row to Tileset
    if Input.key_typed(pygame.K_r):
        tileset.add_rows(1)

    # Make Tile at mouse position not passable
    if Input.left_mouse_down:
        if tileset.is_at_mouse_pos():
            tile.passable = False
            tile.color = Renderer.COLOR_BLACK

    # Make Tile at mouse position passable
    if Input.right_mouse_down:
        if tileset.is_at_mouse_pos():
            tile.passable = True
            tile.color = (128, 128, 128)

    if Input.key_typed(pygame.K_q):
        if tileset.is_at(Input.mouse_x(), Input.mouse_y()):
            tile.passable = True
            tile.color = Renderer.COLOR_GREEN
            GenAlg.start_node = tile
            TileInteractor.start_node = tile

    if Input.key_typed(pygame.K_e):
        if tileset.is_at_mouse_pos():
            tile.passable = True
            tile.color = Renderer.COLOR_RED
            GenAlg.end_node = tile
            TileInteractor.end_node = tile

    if Input.key_typed(pygame.K_g):
        GenAlg.init()


# This is used for framerate
clock = pygame.time.Clock()

# This initialises pygame
pygame.init()
pygame.font.init()

# This initialises keyboard and mouse input
Input.init()

if __name__ == "__main__":
    tileset = Tileset(10, 10, 40, 25)
    tileset.make_border()
    TileInteractor.tileset = tileset

    maze = """
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

    print(maze)

    parse_maze(tileset, maze)

    # path = Pathfinder.get_path(entity, tileset.tiles[5][5])


    while not GenAlg.ready:
        clock.tick(60)
        Input.process_events()
        handle_mouse_input(tileset)
        Renderer.clear_screen()
        tileset.render()
        pygame.display.flip()

    font = pygame.font.Font(None, 30)


    while 1:
        # This is how we get our 60 FPS
        clock.tick(60)

        # This is SwinGame.ProcessEvents()
        Input.process_events()

        handle_mouse_input(tileset)

        # This is SwinGame.ClearScreen(Color.White)
        Renderer.clear_screen()

        tileset.render()


        text = font.render("Generation: " + str(GenAlg.CURRENT_GENERATION), 1, (255, 255, 255))
        GenAlg.run()
        Renderer.SCREEN.blit(text, (15, 15))

        # This is SwinGame.RefreshScreen()
        pygame.display.flip()



