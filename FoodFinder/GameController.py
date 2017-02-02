import math
import random
import time
import pygame

import Params
import Input
from Entity import Entity
from NeuralNets import NeuralNet
from Pickups import Food
from Renderer import Renderer

import GenAlg

FAST_FORWARD = False

start_time = time.time()
CURRENT_GENERATION = 1

population = []
all_food = []

lowest_output = 0
highest_output = 0

def sort_by_fitness():
    global population
    i = len(population) - 1

    while i >= 0:
        j = 0

        while j < i:
            first_fitness = population[j].fitness
            second_fitness = population[j + 1].fitness

            if first_fitness < second_fitness:
                temp = population[j + 1]

                population[j + 1] = population[j]
                population[j] = temp

            j += 1

        i -= 1

# Create random brains for first generation
def init():
    for i in range(Params.population_size):
        new_entity = Entity()
        new_entity.brain = NeuralNet()
        new_entity.x = random.randint(0, Renderer.SCREEN_WIDTH)
        new_entity.y = random.randint(0, Renderer.SCREEN_HEIGHT)
        population.append(new_entity)

    for i in range(Params.num_food):
        all_food.append(Food())

# Compares the locations of each food with the passed in entity.
# Returns whichever food is closest diagonally.
def get_closest_food(entity):
    result = all_food[0]
    index = 0
    closest_distance = math.pow(math.fabs(entity.x - result.x), 2) + math.pow(math.fabs(entity.y - result.y), 2)

    for i in range(Params.num_food):
        temp_distance = math.pow(math.fabs(entity.x - all_food[i].x), 2) + math.pow(math.fabs(entity.y - all_food[i].y), 2)

        if temp_distance < closest_distance:
            closest_distance = temp_distance
            result = all_food[i]
            index = i

    entity.closest_food = result
    entity.food_index = index
    return result

def render():
    for f in all_food:
        f.render()

    for entity in population:
        entity.render((50 + (entity.fitness * 5), 0, 0))

    #for i in range(len(population)):
       # if i < 5:
          #  population[i].render((255, 0, 0))
       # else:
           # population[i].render((0, 0, 255))


def reset_population():
    global population
    for entity in population:
        entity.x = random.randint(0, Renderer.SCREEN_WIDTH)
        entity.y = random.randint(0, Renderer.SCREEN_HEIGHT)
        entity.fitness = 0
        entity.heading = 0

def tick():
    global population
    global all_food

    global lowest_output
    global highest_output

    cur_ent = 0

    for entity in population:
        get_closest_food(entity)
        inputs = []

        entity.get_vector_to_closest_food()

        # Inputs are 2 Vectors - 1 is current vector, 2 is required vector to nearest food
        # Can be positive or negative (not math.abs())
        inputs.append(entity.dx)
        inputs.append(entity.dy)
        inputs.append(entity.closest_food_vector[0])
        inputs.append(entity.closest_food_vector[1])

        outputs = entity.brain.update(inputs)

        #if cur_ent == 0:
         #   lowest_output = min(outputs)
          #  highest_output = max(outputs)
        #else:
         #   if min(outputs) < lowest_output:
          #      lowest_output = min(outputs)

           # if max(outputs) > highest_output:
            #    highest_output = max(outputs)

        # Get net angle change from outputs.
        # Change entity movement vector based on the change
        left_change = outputs[0] * Params.MAX_ANGLE_CHANGE
        right_change = outputs[1] * Params.MAX_ANGLE_CHANGE

        net_angle_change = right_change - left_change

        entity.change_angle(net_angle_change)
        entity.move()

        if entity.ate_food:
            all_food[entity.food_index] = Food()

    # Replenish any food that has been eaten
    for i in range(Params.population_size - len(population)):
        all_food.append(Food())


def get_avg_fitness():
    tot_fitness = 0
    for i in range(len(population)):
        tot_fitness += population[i].fitness

    return tot_fitness / len(population)

def get_highest_fitness():
    highest_fitness = 0
    for i in range(len(population)):
        if population[i].fitness > highest_fitness:
            highest_fitness = population[i].fitness

    return highest_fitness


def evolve():
    global start_time
    global population
    global all_food
    global CURRENT_GENERATION
    CURRENT_GENERATION += 1
    start_time = time.time()

    global population
    print("Gen " + str(CURRENT_GENERATION) + " Highest Fitness: " + str(get_highest_fitness()) + " Average Fitness: " + str(get_avg_fitness()))
    population = GenAlg.evolve(population)
    sort_by_fitness()

    reset_population()

    global all_food
    all_food = []
    for i in range(Params.num_food):
        all_food.append(Food())

def run():
    global FAST_FORWARD

    if Input.key_typed(pygame.K_s):
        FAST_FORWARD = not FAST_FORWARD

    if not FAST_FORWARD:
        if time.time() - start_time > Params.generation_length:
            evolve()

        tick()
        render()
    else:
        for i in range(Params.ticks_per_generation):
            tick()
        evolve()


