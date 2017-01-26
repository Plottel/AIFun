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

        # Loop for number of ticks in each generation
            # Update neural net
            # Move entities

        # Pass GenAlg population and get it to update brains for each Entity

        if Input.key_down(pygame.K_w):
            Renderer.SCREEN.fill((255, 255, 255))

        pygame.display.flip()