from NeuralNets import NeuralNet
from Renderer import Renderer
import pygame
import math
from pygame.rect import Rect
import Params


class Entity:
    # Read-only property. Rect is derived from x, y, width, height
    @property
    def rect(self):
        return Rect(self.x, self.y, self.size, self.size)

    def get_vector_to_closest_pond(self):
        x_offset = self.closest_pond.rect.centerx - self.rect.centerx
        y_offset = self.closest_pond.rect.centery - self.rect.centery

        vector_length = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

        if x_offset == 0 or vector_length == 0:
            x_vel = 0
        else:
            x_vel = x_offset / vector_length

        if y_offset == 0 or vector_length == 0:
            y_vel = 0
        else:
            y_vel = y_offset / vector_length

        self.closest_pond_vector = x_vel, y_vel

    def get_vector_to_closest_food(self):
        x_offset = self.closest_food.rect.centerx - self.rect.centerx
        y_offset = self.closest_food.rect.centery - self.rect.centery

        vector_length = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

        if x_offset == 0 or vector_length == 0:
            x_vel = 0
        else:
            x_vel = x_offset / vector_length

        if y_offset == 0 or vector_length == 0:
            y_vel = 0
        else:
            y_vel = y_offset / vector_length

        self.closest_food_vector = x_vel, y_vel

    def change_angle(self, left, right):
        # How far to change angle
        angle_change = left - right

        # Clamp angle to within MAX_TURN_SPEED
        if angle_change < -Params.MAX_TURN_SPEED:
            angle_change = -Params.MAX_TURN_SPEED
        if angle_change > Params.MAX_TURN_SPEED:
            angle_change = Params.MAX_TURN_SPEED

        # Change the angle
        self.heading += angle_change

        # Net speed to move at this frame
        self.speed = left + right

        # Assign new movement vector
        self.dx = math.cos(self.heading)
        self.dy = math.sin(self.heading)

    # Four directions are rubbish but it'll do.
    def move(self):
        self.ate_food = False

        # Get a little bit hungrier
        self.fullness -= 1

        # Get a little bit thirstier
        self.quenched -= 1

        self.x += self.dx * self.speed * 2.5
        self.y += self.dy * self.speed * 2.5

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
            self.ate_food = True
            self.fullness += Params.FOOD_REFILL_AMOUNT

            # Can't overfill belly
            if self.fullness > Params.FRAMES_TO_STARVE:
                self.fullness = Params.FRAMES_TO_STARVE

        # Check collision with pond
        if self.rect.colliderect(self.closest_pond.rect):
            self.quenched += Params.POND_REFILL_AMOUNT

            # Can't do a Tiddalick
            if self.quenched > Params.FRAMES_TO_DEHYDRATION:
                self.quenched = Params.FRAMES_TO_DEHYDRATION


    def __init__(self):
        self.brain = NeuralNet()
        self.alive = True
        self.closest_food = None
        self.closest_food_vector = 0, 0
        self.food_index = 0
        self.closest_pond = None
        self.closest_pond_vector = 0, 0
        self.closest_entity = None
        self.ate_food = False
        self.fullness = Params.FRAMES_TO_STARVE
        self.quenched = Params.FRAMES_TO_DEHYDRATION
        self.x = 0
        self.y = 0
        self.size = 10
        self.heading = 0
        self.dx = 0
        self.dy = 0
        self.speed = 0
        self.fitness = 0

    def render(self, color):
        pygame.draw.rect(Renderer.SCREEN, color, self.rect, 0)

        # Line to nearest entity
        #pygame.draw.line(Renderer.SCREEN, (0, 255, 0), (self.rect.centerx, self.rect.centery), (self.closest_entity.rect.centerx, self.closest_entity.rect.centery), 1)

        # Line to nearest food
        #pygame.draw.line(Renderer.SCREEN, (255, 0, 0), (self.x + self.size / 2, self.y + self.size / 2), (self.closest_food.x + 3, self.closest_food.y + 3), 1)

        # Line following movement vector
        #start_line = self.x + self.size / 2, self.y + self.size / 2
        #end_line = self.x + (self.size / 2) + (60 * self.closest_food_vector[0]), self.y + (self.size / 2) + (60 * self.closest_food_vector[1])
        #moving_line_start = self.x + (self.size / 2), self.y + (self.size / 2)
        #moving_line_end = moving_line_start[0] + (20 * self.dx), moving_line_start[1] + (20 * self.dy)
        #pygame.draw.line(Renderer.SCREEN, (0, 255, 0), moving_line_start, moving_line_end, 1)

        #pygame.draw.line(Renderer.SCREEN, (0, 255, 0), start_line, end_line, 1)