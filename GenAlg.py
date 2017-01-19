from Renderer import Renderer
from Population import *
import math
import random
from random import shuffle
import Input
import pygame
from Entity import Dir
import time

CURRENT_GENERATION = 0

# Variables determining the scope of the simulation
POPULATION_SIZE = 150
MAX_MOVES = 100
TICK_RATE = 0.048888888888
MUTATION_CHANCE = 0.05
FRAMES_PER_MOVE = math.ceil(60 / TICK_RATE)
FRAMES_PER_GENERATION = MAX_MOVES * (FRAMES_PER_MOVE)

# When calculating weightings, division = good score, multiplication = penalty.
# Number of frames the simulation ran for * MAX_MOVES
MAX_TILES_REVISITED_PENALTY = FRAMES_PER_GENERATION
TILES_VISITED_WEIGHTING = 0.001

MAX_STAND_STILL_SCORE = MAX_MOVES / TICK_RATE
MAX_STAND_STILL_WEIGHTING = 0.09

MAX_TIME_SPENT_AT_GOAL = MAX_TILES_REVISITED_PENALTY
TIME_SPENT_AT_GOAL_WEIGHTING = 0.9

MAX_DIRECTION_CHANGE_PENALTY = MAX_MOVES
DIRECTION_CHANGE_WEIGHTING = 0.009

# Parent selection constants
PCNT_BEST_CHOSEN = 20
PARENTS_CHOSEN = 70

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

def calculate_time_spent_at_end_node(entity):
    if entity.time_spent_at_end > MAX_TIME_SPENT_AT_GOAL:
        print("End node max WRONG")

    return (entity.time_spent_at_end / MAX_TIME_SPENT_AT_GOAL) / TIME_SPENT_AT_GOAL_WEIGHTING

def calculate_successful_move_score(entity):
    if entity.successful_moves > MAX_STAND_STILL_SCORE:
        print("Stand still score max WRONG")

    return (entity.successful_moves / MAX_STAND_STILL_SCORE) / MAX_STAND_STILL_WEIGHTING

def calculate_revisited_tiles_penalty(entity):
    result = 0
    total_tile_score = 0

    for col in entity.tiles_visited:
        for row in col:
            result += math.pow(row, 2)

    total_tile_score += result

    if total_tile_score > MAX_TILES_REVISITED_PENALTY:
        print("Tile revisit score max WRONG. Score: " + str(total_tile_score) + " Max: " + str(MAX_TILES_REVISITED_PENALTY))

    return (result / MAX_TILES_REVISITED_PENALTY) * TILES_VISITED_WEIGHTING


def calculate_direction_change_penalty(entity):

    result = (entity.direction_changes / MAX_DIRECTION_CHANGE_PENALTY) * DIRECTION_CHANGE_WEIGHTING

    if result > MAX_DIRECTION_CHANGE_PENALTY:
        print("Direction change penalty WRONG. Score: " + str(result) + " Max: " + str(MAX_DIRECTION_CHANGE_PENALTY))

    return result


# Calculates fitness based on pythagoras distance from end node. Higher fitness is better.
# Also returns the fitness value to be used to get total population fitness.
def calculate_fitness(entity):
    fitness = calculate_revisited_tiles_penalty(entity)
    fitness += calculate_successful_move_score(entity)
    fitness += calculate_time_spent_at_end_node(entity)
    fitness += calculate_direction_change_penalty(entity)

    entity.fitness = fitness * 100
    return entity.fitness


# Creates an entity at the co-ordinates of the start node
def create_entity():
    return Entity(start_node.x, start_node.y)


def get_full_move_sequence():
    return {
        Dir.Left: False,
        Dir.Up: False,
        Dir.Right: False,
        Dir.Down: False
    }

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
    selection_threshold = random.uniform(0, total_fitness)
    cur_selection = 0

    while (selection_threshold > cur_selection):
        # Entities who reach the goal are automatically chosen as parents
        if population.entities[cur_selection].time_spent_at_end > 0:
            return population.entities.pop(cur_selection)

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
    global population

    parents = []

    population.sort_entities()

    number_of_best = math.floor(POPULATION_SIZE * (PCNT_BEST_CHOSEN / 100))

    # Select the best possible parents
    for i in range(number_of_best):
        parents.append(population.entities.pop(i))

    number_of_parents = math.floor((POPULATION_SIZE * (PARENTS_CHOSEN / 100)) - number_of_best)

    random.shuffle(population.entities)
    total_fitness = get_pop_fitness()

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
    number_of_children = math.floor(POPULATION_SIZE / 4)
    children = []

    for i in range(POPULATION_SIZE - len(parents)):
        child = create_entity()
        mum = parents[random.randint(0, math.floor(len(parents) / 2))]
        dad = parents[random.randint(math.floor(len(parents) / 2), len(parents) - 1)]

        get_inherited_movement_sequence((mum, dad), child)

        children.append(child)

    return children


def mutate():
    for entity in population.entities:

        if random.random() <= MUTATION_CHANCE:
            mutated_moves = []

            while not random.randint(0, 3) == 0:
                index_to_mutate = random.randint(0, MAX_MOVES - 1)

                while index_to_mutate in mutated_moves:
                    index_to_mutate = random.randint(0, MAX_MOVES - 1)

                mutated_moves.append(index_to_mutate)

                entity.movement_sequence[index_to_mutate] = get_random_movement_sequence()

def print_fitness_data():
    best_entity = None
    best_fitness_score = 0
    for entity in population.entities:
        if entity.fitness >= best_fitness_score:
            best_entity = entity
            best_fitness_score = entity.fitness

    print("Highest Fitness: " + str(best_entity.fitness))
    print("Population Length: " + str(len(population.entities)))


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
        entity.clear_tiles_visited()

    # Add children to the new generation
    for entity in children:
        next_generation.append(entity)

    # Copy new generation to population list
    population.entities = next_generation

    # Mutate
    mutate()

    population.sort_entities()

    for i in range(POPULATION_SIZE):
        population.entities[i].color = (255 - i, 0, 0)

    # Reset entity values
    for entity in population.entities:
        entity.x = start_node.x
        entity.y = start_node.y
        entity.successful_moves = 0
        entity.time_spent_at_end = 0
        entity.fitness = 0
        entity.direction_changes = 0

    global CURRENT_GENERATION
    CURRENT_GENERATION += 1

    print(CURRENT_GENERATION)


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
            entity.movement_sequence.append(get_full_move_sequence())

        population.entities.append(entity)

    global ready
    ready = True

    # constant_moving_entity = create_entity()
    # constant_moving_entity.color = Renderer.COLOR_RED

    # for i in range(MAX_MOVES):
    #     constant_moving_entity.movement_sequence.append({Dir.Left: False, Dir.Up: True, Dir.Right: True, Dir.Down: False})

    # population.entities.append(constant_moving_entity)


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