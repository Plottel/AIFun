import random
import Params

    ###############################################
    ###               NEURON CLASS              ###
    ###############################################

# Represents an individual node in the Neural Network.
# Receives a number of inputs with corresponding weights.
class Neuron:
    # Creates randomised value representing input weights.
    # When a Neuron is created, its inputs are randomised.
    def randomise_inputs(self):
        # 1 extra input represents the threshold value.
        # This way allows the threshold to be built into the weights,
        # simplifying the math and allowing the GA to easily manipulate it.
        for i in range(self.num_inputs + 1):
            self.input_weights.append(random.uniform(-1, 1))

    def __init__(self, num_inputs):
        # Member variables
        self.num_inputs = num_inputs
        self.input_weights = []

        self.randomise_inputs()


        ###############################################
        ###               NEURON LAYER CLASS        ###
        ###############################################

# Represents a collection of Neurons - a layer in the Neural Network.
# Used for both Hidden layers and Output layer.
class NeuronLayer:
    # Initialises neuron list
    def populate_neurons(self):
        for i in range(self.num_neurons):
            self.neurons.append(Neuron(self.num_inputs_per_neuron))

    def __init__(self, num_neurons, num_inputs_per_neuron):
        # Member variables
        self.num_neurons = num_neurons
        self.num_inputs_per_neuron = num_inputs_per_neuron
        self.neurons = []

        self.populate_neurons()


            ###############################################
            ###               NEURAL NET CLASS          ###
            ###############################################

# Co-ordinates the Neural Network
# Stores each layer of neurons
# Replaces weights after each iteration
class NeuralNet:
    num_inputs = Params.num_inputs
    num_outputs = Params.num_outputs
    num_hidden_layers = Params.num_hidden_layers
    neurons_per_hidden_layer = Params.neurons_per_hidden_layer
    layers = []

    # Sets up each layer of the neural network.
    # Initialises weights to random values between -1 and 1.
    def create_net(self):
        # Create first hidden layer.
        # This receives its input from the input layer,
        # therefore its num_inputs == NeuralNet.num_inputs
        self.layers.append(NeuronLayer(self.neurons_per_hidden_layer, self.num_inputs))

        # Create remaining hidden layers
        # These receive input from another hidden layer,
        # therefore its num_inputs == NeuralNet.neurons_per_hidden_layer
        for i in range(self.num_hidden_layers - 1):
            self.layers.append(NeuronLayer(self.neurons_per_hidden_layer, self.neurons_per_hidden_layer))

        # Create output layer.
        # Its num_neurons == NeuralNet.num_outputs
        self.layers.append(NeuronLayer(self.num_outputs, self.neurons_per_hidden_layer))

    def __init__(self):
        self.layers = []
        self.create_net()






