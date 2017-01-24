import pygame, sys
from Renderer import Renderer
import Input

clock = pygame.time.Clock()

pygame.init()
Input.init()

if __name__ == "__main__":
    while True:
        clock.tick(60)
        Input.process_events()
        Renderer.clear_screen()
        pygame.display.flip()