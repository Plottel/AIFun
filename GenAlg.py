from Renderer import Renderer
from Population import *
from Entity import Move
import math
import random
import Input
import pygame

POPULATION_SIZE = 1
MAX_MOVES = 50

start_node = None
end_node = None

population = None

ready = False

def calculate_fitness(entity):
    x_offset = fabs(entity.x - (end_node.x + Renderer.TILE_SIZE / 2))
    y_offset = fabs(entity.y - (end_node.y + Renderer.TILE_SIZE / 2))

    entity.fitness = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

def create_entity():
    return Entity(start_node.x, start_node.y)


def get_random_movement_sequence():
    return random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)


def init_move_sequence(entity):
    for i in range(MAX_MOVES):
        entity.movement_sequence[i] = Move(get_movement_sequence())


# First time setup for the genetic algorithm.
# Creates the first population.
def init():
    global population
    population = Population()

    # Make individuals for the population
    for p in range(POPULATION_SIZE):
        entity = create_entity()

        # Get move sequences for each individual
        for x in range(MAX_MOVES):
            entity.movement_sequence.append(Move(get_random_movement_sequence()))

        # Add the individual to the population
        population.entities.append(entity)

    global ready
    ready = True


# Runs the genetic algorithm
def run():
    global population

    population.move()

    if Input.key_typed(pygame.K_t):
        population.tick()

    population.render()