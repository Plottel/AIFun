from Entity import *
import GenAlg
from Renderer import Renderer

class Population:
    entities = []
    movement_index = 0


    def move(self):
        for entity in self.entities:
            entity.move(self.movement_index)

    # Increments the movement index, telling Entities to move to the next set of inputs in their sequence
    def tick(self):
        self.movement_index += 1


    def render(self):
        for entity in self.entities:
            entity.render()