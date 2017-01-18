from Renderer import Renderer

class GenAlg:
    end_node = None

    def __init__(self, end):
        self.end_node = end

    def calculate_fitness(self, entity):
        x_offset = fabs(entity.x - (end_node.x + Renderer.TILE_SIZE / 2))
        y_offset = fabs(entity.y - (end_node.y + Renderer.TILE_SIZE / 2))