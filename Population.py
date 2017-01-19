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

    def sort_entities(self):
        i = len(self.entities) - 1

        while i >= 0:
            j = 0

            while j < i:
                first_fitness = self.entities[j].fitness
                second_fitness = self.entities[j + 1].fitness

                if first_fitness < second_fitness:
                    temp = self.entities[j + 1]
                    temp.fitness = 12

                    self.entities[j + 1] = self.entities[j]
                    self.entities[j] = temp

                j += 1

            i -= 1