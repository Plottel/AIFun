import pygame, sys
from pygame.locals import *
from Renderer import Renderer
from Input import Input
from Tileset import Tileset

Rect = pygame.Rect
clock = pygame.time.Clock()

pygame.init()
Input.init()


if __name__ == "__main__":
    rect = Rect(50, 50, 50, 50)
    dx = 0
    dy = 0
    speed = 1

    tileset = Tileset(50, 50, 5, 5)

    while 1:
        clock.tick(60)
        Input.process_events()

        # VERTICAL MOVEMENT
        if Input.key_down(pygame.K_w):
            dy = -speed

        if Input.key_down(pygame.K_s):
            dy = speed

        if Input.key_down(pygame.K_w) & Input.key_down(pygame.K_s):
            dy = 0

        if (not Input.key_down(pygame.K_w)) & (not Input.key_down(pygame.K_s)):
            dy = 0

        # HORIZONTAL MOVEMENT
        if Input.key_down(pygame.K_a):
            dx = -speed

        if Input.key_down(pygame.K_d):
            dx = speed

        if Input.key_down(pygame.K_d) & Input.key_down(pygame.K_a):
            dx = 0

        if (not Input.key_down(pygame.K_a)) & (not Input.key_down(pygame.K_d)):
            dx = 0

        if Input.key_typed(pygame.K_c):
            tileset.add_columns(1)

        if Input.key_typed(pygame.K_r):
            tileset.add_rows(1)

        if Input.left_mouse_down:
            rect.x = Input.mouse_x()
            rect.y = Input.mouse_y()

        rect.x += dx
        rect.y += dy

        Renderer.clear_screen()

        tileset.render()
        pygame.draw.rect(Renderer.SCREEN, Renderer.COLOR_BLACK, rect, 0)

        pygame.display.flip()



