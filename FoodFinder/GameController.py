import math
import random
import time
import pygame

import Params
import Input
from Entity import Entity
from NeuralNets import NeuralNet
from Pickups import Food
from Pickups import Pond
from Renderer import Renderer

import GenAlg

FAST_FORWARD = False

start_time = time.time()
CURRENT_GENERATION = 1
CURRENT_TICK = 0
ENTITIES_STILL_ALIVE = True
NUM_DEAD_ENTITIES = 0

population = []
all_food = []
ponds = []

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

    for i in range(Params.num_ponds):
        ponds.append(Pond())

    for i in range(Params.num_food):
        x = random.randint(0, Renderer.SCREEN_WIDTH)
        y = random.randint(0, Renderer.SCREEN_HEIGHT)

        # Keep picking random food locations until a valid point is chosen
        while point_in_pond(x, y):
            x = random.randint(0, Renderer.SCREEN_WIDTH)
            y = random.randint(0, Renderer.SCREEN_HEIGHT)

        all_food.append(Food(x, y))



# Compares the locations of each entity with the passed in entity.
# Returns whichever entity is closest diagonally.
def get_closest_entity(entity):
    result = population[0]

    if result is entity:
        result = population[1]

    closest_distance = math.pow(math.fabs(entity.rect.centerx - result.rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - result.rect.centery), 2)

    for i in range(Params.population_size):
        if population[i].alive:
            temp_distance = math.pow(math.fabs(entity.rect.centerx - population[i].rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - population[i].rect.centery), 2)

            if temp_distance < closest_distance and population[i] is not entity:
                closest_distance = temp_distance
                result = population[i]

    entity.closest_entity = result


# Compares the locations of each pond with the passed in entity.
# Returns whichever pond is closest diagonally
def get_closest_pond(entity):
    result = ponds[0]
    closest_distance = math.pow(math.fabs(entity.rect.centerx - result.rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - result.rect.centery), 2)

    for i in range(Params.num_ponds):
        temp_distance = math.pow(math.fabs(entity.rect.centerx - ponds[i].rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - ponds[i].rect.centery), 2)

        if temp_distance < closest_distance:
            closest_distance = temp_distance
            result = ponds[i]

    entity.closest_pond = result


# Compares the locations of each food with the passed in entity.
# Returns whichever food is closest diagonally.
def get_closest_food(entity):
    result = all_food[0]
    index = 0
    closest_distance = math.pow(math.fabs(entity.rect.centerx - result.rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - result.rect.centery), 2)

    for i in range(Params.num_food):
        temp_distance = math.pow(math.fabs(entity.rect.centerx - all_food[i].rect.centerx), 2) + math.pow(math.fabs(entity.rect.centery - all_food[i].rect.centery), 2)

        if temp_distance < closest_distance:
            closest_distance = temp_distance
            result = all_food[i]
            index = i

    entity.closest_food = result
    entity.food_index = index


def point_in_pond(x, y):
    for pond in ponds:
        if pond.rect.collidepoint(x, y):
            return True

    return False


def render():
    for p in ponds:
        p.render()

    for f in all_food:
        f.render()

    for entity in population:
        if entity.alive:
            red = (entity.quenched / Params.FRAMES_TO_DEHYDRATION) * 255
            entity.render((255 - red, 0, 0))

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
        entity.fullness = Params.FRAMES_TO_STARVE
        entity.quenched = Params.FRAMES_TO_DEHYDRATION
        entity.heading = 0


def tick():
    global population
    global all_food

    global lowest_output
    global highest_output

    global CURRENT_TICK
    CURRENT_TICK += 1

    cur_ent = 0

    for entity in population:
        if entity.alive:
            #get_closest_entity(entity)
            get_closest_food(entity)
            get_closest_pond(entity)
            entity.get_vector_to_closest_food()
            entity.get_vector_to_closest_pond()
            inputs = []

            # Store Entity position as it's used for many inputs.
            #center_x = entity.rect.centerx
            #center_y = entity.rect.centery

            # Entity vector
            inputs.append(entity.dx)
            inputs.append(entity.dy)
            # Distance to food
            inputs.append(entity.closest_food_vector[0])
            inputs.append(entity.closest_food_vector[1])
            # Distance to pond
            inputs.append(entity.closest_pond_vector[0])
            inputs.append(entity.closest_pond_vector[1])
            # percentage food satisfaction
            inputs.append(entity.fullness / Params.FRAMES_TO_STARVE)
            # percentage water satisfaction
            inputs.append(entity.quenched / Params.FRAMES_TO_DEHYDRATION)

            outputs = entity.brain.update(inputs)
            entity.change_angle(outputs[0], outputs[1])

            entity.move()

            # If entity died this frame
            if entity.fullness == 0 or entity.quenched == 0:
                entity.fitness = CURRENT_TICK
                entity.alive = False
                global NUM_DEAD_ENTITIES
                NUM_DEAD_ENTITIES += 1
                if NUM_DEAD_ENTITIES == Params.population_size:
                    global ENTITIES_STILL_ALIVE
                    ENTITIES_STILL_ALIVE = False

            if entity.ate_food:
                x = random.randint(0, Renderer.SCREEN_WIDTH)
                y = random.randint(0, Renderer.SCREEN_HEIGHT)

                while point_in_pond(x, y):
                    x = random.randint(0, Renderer.SCREEN_WIDTH)
                    y = random.randint(0, Renderer.SCREEN_HEIGHT)

                all_food[entity.food_index].x = x
                all_food[entity.food_index].y = y

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
    global NUM_DEAD_ENTITIES
    NUM_DEAD_ENTITIES = 0
    global ENTITIES_STILL_ALIVE
    ENTITIES_STILL_ALIVE = True

    global CURRENT_TICK
    CURRENT_TICK = 0

    start_time = time.time()

    global population
    print("Gen " + str(CURRENT_GENERATION) + " Highest Fitness: " + str(get_highest_fitness()) + " Average Fitness: " + str(get_avg_fitness()))
    population = GenAlg.evolve(population)
    #sort_by_fitness()

    reset_population()

    #global all_food
    #all_food = []

    #for i in range(Params.num_food):
     #   all_food.append(Food())

def run():
    global FAST_FORWARD

    if Input.key_typed(pygame.K_s):
        FAST_FORWARD = not FAST_FORWARD

    if not FAST_FORWARD:
        if not ENTITIES_STILL_ALIVE:
            evolve()

        tick()
        render()
    else:
        while ENTITIES_STILL_ALIVE:
            tick()
        evolve()


