from NeuralNets import NeuralNet
from Renderer import Renderer
import pygame
from pygame.rect import Rect


class Entity:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    # Four directions are rubbish but it'll do.
    def move(self):
        self.ate_food = False

        self.x += self.d_right
        self.x -= self.d_left
        self.y += self.d_down
        self.y -= self.d_up

        # Wrap around screen
        if self.x > Renderer.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = Renderer.SCREEN_WIDTH

        if self.y > Renderer.SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = Renderer.SCREEN_HEIGHT

        # Check collision with closest food
        if self.rect.colliderect(self.closest_food.rect):
            self.fitness += 1
            self.ate_food = True

    def __init__(self):
        self.brain = NeuralNet()
        self.closest_food = None
        self.food_index = 0
        self.ate_food = False
        self.x = 0
        self.y = 0
        self.size = 10
        self.d_left = 0
        self.d_right = 0
        self.d_up = 0
        self.d_down = 0
        self.fitness = 0

    def render(self, color):
        pygame.draw.rect(Renderer.SCREEN, color, self.rect, 0)