from Entity import *


class Population:
    entities = []

    def move(self):
        for entity in self.entities:
            entity.move()

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

                    self.entities[j + 1] = self.entities[j]
                    self.entities[j] = temp

                j += 1

            i -= 1