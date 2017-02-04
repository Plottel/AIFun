import math

num_inputs = 8
num_hidden_layers = 1
neurons_per_hidden_layer = 6
num_outputs = 2
bias = -1
activation_response = 1
population_size = 30
num_food = 20
num_ponds = 1
MAX_TURN_SPEED = 0.3
mutation_rate = 0.1
mutation_power = 0.6
crossover_rate = 0.7
FRAMES_TO_STARVE = 1000
FRAMES_TO_DEHYDRATION = 400
FOOD_REFILL_AMOUNT = math.floor(FRAMES_TO_STARVE / 1)#math.floor(FRAMES_TO_STARVE / 20)
POND_REFILL_AMOUNT = math.floor(FRAMES_TO_DEHYDRATION / 400)

