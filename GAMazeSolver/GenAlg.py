from Renderer import Renderer
from Population import *
import math
import random
from random import shuffle
import Input
import pygame

from Entity import GeneData
from Entity import Dir
from Entity import Entity
import time

CURRENT_GENERATION = 0

# Variables determining the scope of the simulation
POPULATION_SIZE = 100
PATH_SEQUENCE_LENGTH = 10
MAX_MOVES = 100
TICK_RATE = 0.048888888888
GEN_LIFETIME = 15
FASTEST_TICK_RATE = 0.04888888888
SLOWEST_TICK_RATE = 2

MIN_SPEED = 1
MAX_SPEED = 8

MUTATION_CHANCE = 0.03
FRAMES_PER_MOVE = math.ceil(60 / TICK_RATE)
FRAMES_PER_GENERATION = 60 * GEN_LIFETIME

# When calculating weightings, division = good score, multiplication = penalty.
# Number of frames the simulation ran for * MAX_MOVES
MAX_TILES_REVISITED_PENALTY = math.pow(FRAMES_PER_GENERATION, 2)
TILES_VISITED_WEIGHTING = 0.5

MAX_STAND_STILL_SCORE = MAX_MOVES / TICK_RATE
MAX_STAND_STILL_WEIGHTING = 0

MAX_TIME_SPENT_AT_GOAL = MAX_TILES_REVISITED_PENALTY
TIME_SPENT_AT_GOAL_WEIGHTING = 0.5

MAX_DIRECTION_CHANGE_PENALTY = MAX_MOVES
DIRECTION_CHANGE_WEIGHTING = 0

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
    #fitness += calculate_successful_move_score(entity)
    fitness += calculate_time_spent_at_end_node(entity)
    #fitness += calculate_direction_change_penalty(entity)

    entity.fitness = fitness * 100
    return entity.fitness


# Creates an entity at the co-ordinates of the start node
def create_entity():
    return Entity(start_node.x + 1, start_node.y + 1)


def get_full_move_sequence():
    return {
        Dir.Left: False,
        Dir.Up: False,
        Dir.Right: False,
        Dir.Down: False
    }

# Generate random percentile chances that the
# individual will choose the direction to move in
def get_random_move_tendencies():
    return {
        Dir.Left: random.uniform(0, 1),
        Dir.Right: random.uniform(0, 1),
        Dir.Up: random.uniform(0, 1),
        Dir.Down: random.uniform(0, 1),
        Dir.NE: random.uniform(0, 1),
        Dir.SE: random.uniform(0, 1),
        Dir.SW: random.uniform(0, 1),
        Dir.NW: random.uniform(0, 1),
        Dir.Still: random.uniform(0, 1)
    }


# Returns a random set of gene data. Used in the initial population.
def get_random_gene_data():
    result = GeneData()
    result.sequence_length = PATH_SEQUENCE_LENGTH

    #result.path_sequence.append(Dir.Right)
    #result.path_sequence.append(Dir.Down)
    #result.path_sequence.append(Dir.Left)
    #result.path_sequence.append(Dir.Down)
    #result.path_sequence.append(Dir.Left)

    for x in range(result.sequence_length):
        result.path_sequence.append(random.randint(0, 1) > 0.5)

    return result


def get_inherited_gene_data(parents, child):
    # Pick each move sequence randomly from parent
    # Something in here about length
    child.genes = GeneData()
    child.genes.sequence_length = PATH_SEQUENCE_LENGTH

    # Get a direction for each index in the list.
    # Check if mum and dad still have indexes in that range.
    # If neither of them do, generate a random dir.
    for i in range(PATH_SEQUENCE_LENGTH):
        # If both parents still have indexes, pick a random parent.
        if parents[0].genes.sequence_length > i and parents[1].genes.sequence_length > i:
            child.genes.path_sequence.append(parents[random.randint(0, 1)].genes.path_sequence[i])
        else:
            if parents[0].genes.sequence_length > i:
                child.genes.path_sequence.append(parents[0].genes.path_sequence[i])
            elif parents[1].genes.sequence_length > i:

                child.genes.path_sequence.append(parents[1].genes.path_sequence[i])
            else:
                # If neither parent has indexes left, generate random True or False
                child.genes.path_sequence.append(random.randint(0, 1) > 0.5)

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
    children = []

    for i in range(POPULATION_SIZE - len(parents)):
        child = create_entity()
        mum = parents[random.randint(0, len(parents) - 1)]
        dad = parents[random.randint(0, len(parents) - 1)]

        # Keep fetching a new parent until there are 2 separate parents
        while dad == mum:
            dad = parents[random.randint(0, len(parents) - 1)]

        get_inherited_gene_data((mum, dad), child)

        children.append(child)

    return children


def mutate():
    for entity in population.entities:
        if random.random() <= MUTATION_CHANCE:
            # Change a random index in path sequence to a random direction.
            index_to_change = random.randint(0, entity.genes.sequence_length - 1)
            entity.genes.path_sequence[index_to_change] = random.randint(0, 1) > 0.5


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
    # Declare lists for use in evolution
    next_generation = []
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
        entity.x = start_node.x + 1
        entity.y = start_node.y + 1
        entity.successful_moves = 0
        entity.time_spent_at_end = 0
        entity.fitness = 0
        entity.direction_changes = 0
        entity.cur_tile_index = (0, 0)

    global CURRENT_GENERATION
    CURRENT_GENERATION += 1

    # Increment sequence length every 5 generations
    if CURRENT_GENERATION % 5 == 0:
        global PATH_SEQUENCE_LENGTH
        PATH_SEQUENCE_LENGTH += 1

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
        entity.genes = get_random_gene_data()

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

    # If the length of the simulation has been reached,
    # evolve to the next generation
    if time.time() - start_time > GEN_LIFETIME:
        evolve()
        start_time = time.time()

    population.move()

    population.render()