from Entity import *
from GenAlg import *
from Renderer import Renderer

class Population:
    entities = []
    movement_index = 0

    def get_pop_fitness(self):
        for entity in entities:
            GenAlg.calculate_fitness(entity)


    def move(self):
        for entity in self.entities:
            entity.move(self.movement_index)


    def tick(self):
        self.movement_index += 1


    def render(self):
        for entity in self.entities:
            entity.render()