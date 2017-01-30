from NeuralNets import Neuron
from NeuralNets import NeuronLayer
from NeuralNets import NeuralNet
from Entity import Entity
import math
import Params
import random

PCNT_BEST_CHOSEN = 20
PARENTS_CHOSEN = 50
MUTATION_CHANCE = 0.2

entities = []

def get_pop_fitness():
    total_fitness = 0

    for entity in entities:
        total_fitness += entity.fitness

    return total_fitness



def sort_entities():
    global entities
    i = len(entities) - 1

    while i >= 0:
        j = 0

        while j < i:
            first_fitness = entities[j].fitness
            second_fitness = entities[j + 1].fitness

            if first_fitness < second_fitness:
                temp = entities[j + 1]

                entities[j + 1] = entities[j]
                entities[j] = temp

            j += 1

        i -= 1

# Picks a random number between 0 and the fitness of the population.
# Loops through each index, subtracting the fitness of each entity from the threshold.
# When the threshold reaches zero, the current index is chosen as the parent.
# This method gives fitter individuals a higher chance to be selected,
# but does not guarantee the selection of any particular individual.
def get_parent(total_fitness):
    selection_threshold = random.uniform(0, total_fitness)
    cur_selection = 0

    while selection_threshold > cur_selection:
        selection_threshold -= entities[cur_selection].fitness
        cur_selection += 1


    return entities.pop(cur_selection - 1)

def select_parents():
    global entities

    parents = []

    number_of_best = math.floor(Params.population_size * (PCNT_BEST_CHOSEN / 100))

    # Select the best possible parents
    for i in range(number_of_best):
        parents.append(entities.pop(i))

    number_of_parents = math.floor((Params.population_size * (PARENTS_CHOSEN / 100)) - number_of_best)

    total_fitness = get_pop_fitness()

    # Select parents to fill half of the next generation
    for i in range(number_of_parents):
        parent = get_parent(total_fitness)
        parents.append(parent)
        total_fitness -= parent.fitness

    return parents

def make_children(parents):
    children = []

    for i in range(Params.population_size - len(parents)):
        child = Entity()
        mum = parents[random.randint(0, len(parents) - 1)]
        dad = parents[random.randint(0, len(parents) - 1)]

        # Keep fetching a new parent until there are 2 separate parents
        while dad == mum:
            dad = parents[random.randint(0, len(parents) - 1)]

        parent_weights = (mum.brain.get_weights(), dad.brain.get_weights())
        new_weights = []

        # Choose randomly between mum and dad for each weight
        for i in range(dad.brain.get_number_of_weights()):
            new_weights.append(parent_weights[random.randint(0, 1)][i])

        child.brain.replace_weights(new_weights)
        children.append(child)

    return children

def mutate(entities):
    for entity in entities:
            weights = entity.brain.get_weights()

            for weight in weights:
                if random.uniform(0, 1) > MUTATION_CHANCE:
                    weight += 0.3 * random.uniform(-1, 1)

            entity.brain.replace_weights(weights)

def evolve(pop):
    global entities
    entities = pop

    sort_entities()

    next_generation = []
    parents = select_parents()
    children = make_children(parents)

    entities = next_generation

    # Add parents to the new generation
    for entity in parents:
        next_generation.append(entity)

    # Add children to the new generation
    for entity in children:
        next_generation.append(entity)

    mutate(entities)

    return entities


