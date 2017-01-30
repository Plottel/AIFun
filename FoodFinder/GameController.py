import math
import time
import pygame

import Params
import Input
from Entity import Entity
from NeuralNets import NeuralNet
from Pickups import Food
from Renderer import Renderer

from FoodFinder import GenAlg

FAST_FORWARD = False

start_time = time.time()
CURRENT_GENERATION = 1

population = []
all_food = []

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
                temp.fitness = 12

                population[j + 1] = population[j]
                population[j] = temp

            j += 1

        i -= 1

# Create random brains for first generation
def init():
    for i in range(Params.population_size):
        new_entity = Entity()
        new_entity.brain = NeuralNet()
        new_entity.x = Renderer.SCREEN_WIDTH / 2
        new_entity.y = Renderer.SCREEN_HEIGHT / 2
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

    for i in range(len(population)):
        if i < 5:
            population[i].render((255, 0, 0))
        else:
            population[i].render((0, 0, 255))

def reset_population():
    global population
    for entity in population:
        entity.x = Renderer.SCREEN_WIDTH / 2
        entity.y = Renderer.SCREEN_HEIGHT / 2
        entity.fitness = 0

def tick():
    global population
    global all_food

    for entity in population:
        get_closest_food(entity)
        inputs = []

        # Inputs are just x / y distances between Entity and Closest Food.
        # Can be positive or negative (not math.abs())
        inputs.append(entity.x + 5 - entity.closest_food.x)
        inputs.append(entity.y + 5 - entity.closest_food.y)
        #inputs.append(entity.closest_food.x)
        #inputs.append(entity.closest_food.y)

        outputs = entity.brain.update(inputs)

        entity.d_left = outputs[0]
        entity.d_right = outputs[1]
        entity.d_up = outputs[2]
        entity.d_down = outputs[3]

        entity.move()

        if entity.ate_food:
            all_food[entity.food_index] = Food()

    # Replenish any food that has been eaten
    for i in range(Params.population_size - len(population)):
        all_food.append(Food())

def evolve():
    global start_time
    global population
    global all_food
    global CURRENT_GENERATION
    CURRENT_GENERATION += 1
    print(str(CURRENT_GENERATION))
    start_time = time.time()

    global population
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
        FAST_FORWARD = True

    if not FAST_FORWARD:
        if time.time() - start_time > Params.generation_length:
            evolve()

        tick()
        render()
    else:
        for i in range(10):
            for i in range(Params.ticks_per_generation):
                tick()
            evolve()

        FAST_FORWARD = False


