import pygame, sys
from pygame.locals import *
from InputMan import InputMan

Rect = pygame.Rect
clock = pygame.time.Clock()

pygame.init()
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

black = 0, 0, 0
white = 255, 255, 255

if __name__ == "__main__":
    rect = Rect(50, 50, 50, 50)
    dx = 0
    dy = 0
    speed = 1

    while 1:
        clock.tick(60)
        InputMan.process_events()

        # VERTICAL MOVEMENT
        if InputMan.w_down:
            dy = -speed

        if InputMan.s_down:
            dy = speed

        if InputMan.w_down & InputMan.s_down:
            dy = 0

        if (not InputMan.w_down) & (not InputMan.s_down):
            dy = 0

        # HORIZONTAL MOVEMENT
        if InputMan.a_down:
            dx = -speed

        if InputMan.d_down:
            dx = speed

        if InputMan.a_down & InputMan.d_down:
            dx = 0

        if (not InputMan.a_down) & (not InputMan.d_down):
            dx = 0

        if InputMan.left_mouse_down:
            rect.x = InputMan.mouse_x
            rect.y = InputMan.mouse_y

        rect.x += dx
        rect.y += dy


        SCREEN.fill(white)
        pygame.draw.rect(SCREEN, black, rect, 1)
        pygame.display.flip()



