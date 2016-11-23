import pygame, sys
from pygame.locals import *
from Input import Input

Rect = pygame.Rect
clock = pygame.time.Clock()

pygame.init()
Input.init()
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

        if Input.left_mouse_down:
            rect.x = Input.mouse_x()
            rect.y = Input.mouse_y()

        rect.x += dx
        rect.y += dy


        SCREEN.fill(white)
        pygame.draw.rect(SCREEN, black, rect, 1)
        pygame.display.flip()



