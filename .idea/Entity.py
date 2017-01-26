from NeuralNets import Neuron
from NeuralNets import NeuronLayer
from NeuralNets import NeuralNet
from Renderer import Renderer

class Entity:
    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Wrap around screen
        if self.x > Renderer.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = Renderer.SCREEN_WIDTH

        if self.y > Renderer.SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = Renderer.SCREEN_HEIGHT

    def __init__(self):
        self.brain = None
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.fitness = 0