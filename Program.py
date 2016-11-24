import pygame, sys
from pygame.locals import *
from Renderer import Renderer
from Input import Input
from Tileset import Tileset
from pygame.rect import Rect
from TileInteractor import TileInteractor
from Entity import Entity
from Pathfinder import Pathfinder

# This is used for framerate
clock = pygame.time.Clock()

# This initialises pygame
pygame.init()

# This initialises keyboard and mouse input
Input.init()

if __name__ == "__main__":
    tileset = Tileset(50, 50, 10, 10)
    TileInteractor.tileset = tileset
    entity = Entity(tileset.x, tileset.y)

    # path = Pathfinder.get_path(entity, tileset.tiles[5][5])

    while 1:
        # This is how we get our 60 FPS
        clock.tick(60)

        # This is SwinGame.ProcessEvents()
        Input.process_events()

        entity.move()

        # Add column to Tileset
        if Input.key_typed(pygame.K_c):
            tileset.add_columns(1)

        # Add row to Tileset
        if Input.key_typed(pygame.K_r):
            tileset.add_rows(1)

        # Make Tile at mouse position not passable
        if Input.left_mouse_down:
            if tileset.is_at(Input.mouse_x(), Input.mouse_y()):
                tileset.tile_at(Input.mouse_x(), Input.mouse_y()).passable = False

        # Make Tile at mosue position passable
        if Input.right_mouse_down:
            if tileset.is_at(Input.mouse_x(), Input.mouse_y()):
                tileset.tile_at(Input.mouse_x(), Input.mouse_y()).passable = True

        # This is SwinGame.ClearScreen(Color.White)
        Renderer.clear_screen()

        tileset.render()
        entity.render()

        # This is SwinGame.RefreshScreen()
        pygame.display.flip()



