from NeuralNets import NeuralNet
from Renderer import Renderer
import pygame
import math
from pygame.rect import Rect


class Entity:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def get_vector_to_closest_food(self):
        x_offset = self.closest_food.x - (self.x + (self.size / 2))
        y_offset = self.closest_food.y - (self.y + (self.size / 2))

        vector_length = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

        if x_offset == 0 or vector_length == 0:
            x_vel = 0
        else:
            x_vel = x_offset / vector_length

        if y_offset == 0 or vector_length == 0:
            y_vel = 0
        else:
            y_vel = y_offset / vector_length



        return (x_vel, y_vel)

    def change_angle(self, amount_to_change):
        self.heading += amount_to_change
        self.dx = math.cos(math.radians(self.heading))
        self.dy = math.sin(math.radians(self.heading))

    # Four directions are rubbish but it'll do.
    def move(self):
        self.ate_food = False

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

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
        self.heading = 0
        self.dx = 0
        self.dy = 0
        self.change_angle(0)
        self.speed = 1.5
        self.fitness = 0

    def render(self, color):
        pygame.draw.rect(Renderer.SCREEN, color, self.rect, 0)
        pygame.draw.line(Renderer.SCREEN, (255, 0, 0), (self.x, self.y), (self.closest_food.x, self.closest_food.y), 1)