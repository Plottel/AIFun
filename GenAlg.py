from Renderer import Renderer
from Population import *
import math
import random
import Input
import pygame
from Entity import Dir
import time


# Variables determining the scope of the simulation
POPULATION_SIZE = 40
MAX_MOVES = 40
TICK_RATE = 0.15
MUTATION_CHANCE = 0.05

# Forward declaration for the current generation of entities
population = None

start_node = None
end_node = None
node_distance = 0
min_fitness = 250

# Whether or not the simulation should run
ready = False

# Delta time
start_time = time.time()

# Calculates fitness based on pythagoras distance from end node. Higher fitness is better.
# Also returns the fitness value to be used to get total population fitness.
def calculate_fitness(entity):
    x_offset = math.fabs(entity.x - (end_node.x + Renderer.TILE_SIZE / 2))
    y_offset = math.fabs(entity.y - (end_node.y + Renderer.TILE_SIZE / 2))

    distance = math.floor(math.sqrt((x_offset * x_offset) + (y_offset * y_offset)))
    fitness = node_distance - distance + min_fitness

    if fitness < 0:
        fitness = 0

    entity.fitness = fitness + (entity.distance_travelled * 10)
    return entity.fitness


# Creates an entity at the co-ordinates of the start node
def create_entity():
    return Entity(start_node.x, start_node.y)


# Returns a dictionary containing a boolean value for each movement direction
def get_random_movement_sequence():
    return {
        Dir.Left: random.randint(0, 1) > 0.5,
        Dir.Up: random.randint(0, 1) > 0.5,
        Dir.Right: random.randint(0, 1) > 0.5,
        Dir.Down: random.randint(0, 1) > 0.5
    }


def get_inherited_movement_sequence(parents, child):

    for i in range(MAX_MOVES):
        child.movement_sequence.append(parents[random.randint(0, 1)].movement_sequence[i])


#####                                           #####
#####       START REGION PARENT SELECTION       #####
#####                                           #####


# Picks a random number between 0 and the fitness of the population.
# Loops through each index, subtracting the fitness of each entity from the threshold.
# When the threshold reaches zero, the current index is chosen as the parent.
# This method gives fitter individuals a higher chance to be selected,
# but does not guarantee the selection of any particular individual.
def get_parent(total_fitness):
    selection_threshold = random.randint(0, total_fitness)
    cur_selection = 0

    while (selection_threshold > cur_selection):
        selection_threshold -= population.entities[cur_selection].fitness
        cur_selection += 1


    return population.entities.pop(cur_selection - 1)


# Calculates the fitness of each Entity in the population.
# Also calculates the entire fitness of the population.
def get_pop_fitness():
    total_fitness = 0

    for entity in population.entities:
        total_fitness += GenAlg.calculate_fitness(entity)

    return total_fitness


def select_parents():
    number_of_parents = math.floor(POPULATION_SIZE / 2)
    total_fitness = get_pop_fitness()

    parents = []

    # Select parents to fill half of the next generation
    for i in range(number_of_parents):
        parent = get_parent(total_fitness)
        parents.append(parent)

        total_fitness -= parent.fitness

    return parents


#####                                           #####
#####       END REGION PARENT SELECTION         #####
#####                                           #####


def make_children(parents):
    number_of_children = math.floor(POPULATION_SIZE / 2)
    children = []


    for i in range(number_of_children):
        child = create_entity()
        mum = parents[random.randint(0, math.floor(len(parents) / 2))]
        dad = parents[random.randint(math.floor(len(parents) / 2), len(parents) - 1)]

        get_inherited_movement_sequence((mum, dad), child)

        children.append(child)

    return children


def mutate():
    for entity in population.entities:
        if random.random() <= MUTATION_CHANCE:
            while not random.randint(0, 1):
                entity.movement_sequence[random.randint(0, MAX_MOVES - 1)] = get_random_movement_sequence()


def evolve():
    # Reset back to the beginning of the movement sequence
    population.movement_index = 0

    # Declare lists for use in evolution
    next_generation = []
    parents = []

    parents = select_parents()

    children = make_children(parents)

    # Add parents to the new generation
    for entity in parents:
        next_generation.append(entity)

    # Add children to the new generation
    for entity in children:
        next_generation.append(entity)

    # Copy new generation to population list
    population.entities = next_generation

    # Mutate
    mutate()

    # Reset entity positions
    for entity in population.entities:
        entity.x = start_node.x
        entity.y = start_node.y


# First time setup for the genetic algorithm.
# Creates the first population by giving them random movement sequences
def init():
    global population
    global node_distance

    population = Population()

    # Calculate distance between start and end nodes.
    # This is used in fitness calculations
    x_offset = math.fabs((start_node.x + Renderer.TILE_SIZE / 2) - (end_node.x + Renderer.TILE_SIZE / 2))
    y_offset = math.fabs((start_node.y + Renderer.TILE_SIZE / 2) - (end_node.y + Renderer.TILE_SIZE / 2))

    node_distance = math.floor(math.sqrt((x_offset * x_offset) + (y_offset * y_offset)))

    # Make individuals for the population
    for x in range(POPULATION_SIZE):
        entity = create_entity()

        for i in range(MAX_MOVES):
            entity.movement_sequence.append(get_random_movement_sequence())

        population.entities.append(entity)

    global ready
    ready = True


# Runs the genetic algorithm
def run():
    global population
    global start_time

    if population.movement_index == MAX_MOVES:
        evolve()

    population.move()

    if time.time() - start_time > TICK_RATE:
        population.tick()
        start_time = time.time()

    population.render()