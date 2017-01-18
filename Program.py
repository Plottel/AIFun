import pygame, sys
import Input
from pygame.locals import *
from Renderer import Renderer
from Tileset import Tileset
from pygame.rect import Rect
from TileInteractor import TileInteractor
from Entity import Entity
from Pathfinder import Pathfinder
import GenAlg

# TileInteractor and Renderer and Pathfinder don't need to be classes
# Refactor
# Them
# Just
# Like
# I
# Refactored
# Input


# Clean up collision code - copy from FreedomFighter


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
            tile.color = Renderer.COLOR_WHITE

    if Input.key_typed(pygame.K_q):
        if tileset.is_at(Input.mouse_x(), Input.mouse_y()):
            tile.passable = True
            tile.color = Renderer.COLOR_GREEN
            GenAlg.start_node = tile

    if Input.key_typed(pygame.K_e):
        if tileset.is_at_mouse_pos():
            tile.passable = True
            tile.color = Renderer.COLOR_RED
            GenAlg.end_node = tile

    if Input.key_typed(pygame.K_g):
        GenAlg.init()


# This is used for framerate
clock = pygame.time.Clock()

# This initialises pygame
pygame.init()

# This initialises keyboard and mouse input
Input.init()

if __name__ == "__main__":
    tileset = Tileset(10, 10, 40, 40)
    tileset.make_border()
    TileInteractor.tileset = tileset

    # path = Pathfinder.get_path(entity, tileset.tiles[5][5])


    while not GenAlg.ready:
        clock.tick(60)
        Input.process_events()
        handle_mouse_input(tileset)
        Renderer.clear_screen()
        tileset.render()
        pygame.display.flip()

    while 1:
        # This is how we get our 60 FPS
        clock.tick(60)

        # This is SwinGame.ProcessEvents()
        Input.process_events()

        handle_mouse_input(tileset)

        # This is SwinGame.ClearScreen(Color.White)
        Renderer.clear_screen()

        tileset.render()

        GenAlg.run()

        # This is SwinGame.RefreshScreen()
        pygame.display.flip()



