from TileInteractor import TileInteractor
from Tile import Tile
import math

# Data structure used on top of the Tile grid to provide A* info
class Node:
    parent = None
    tile = None
    f_score = 0

    def __init__(self, tile):
        self.tile = tile


class Pathfinder:

    # Returns the node in the open list with the lowest f score
    @staticmethod
    def get_next_current_node(open_list):
        result = None
        lowest_f_score = float('inf')

        for node in open_list:
            if node.f_score < lowest_f_score:
                result = node
                lowest_f_score = node.f_score

        return result

    @staticmethod
    def get_f_score(node, target_node):
        return Pathfinder.get_g_score(node) + Pathfinder.get_h_score(node, target_node)

    @staticmethod
    def get_g_score(node):
        g_score = 0
        n = node

        while n.parent is not None:
            g_score += n.parent.f_score
            n = n.parent

        return g_score

    @staticmethod
    def get_h_score(node, target_node):
        x_offset = math.fabs(node.tile.x - target_node.tile.x)
        y_offset = math.fabs(node.tile.y - target_node.tile.y)

        return math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

    # Gets the nodes in the four compass directions from passed in node
    @staticmethod
    def get_adjacent_nodes(node):
        result = []

        if TileInteractor.tileset.is_at(node.tile.x - 1, node.tile.y):  # West
            result.append(Node(TileInteractor.tileset.tile_at(node.tile.x - 1, node.tile.y)))

        if TileInteractor.tileset.is_at(node.tile.x, node.tile.y - 1):  # North
            result.append(Node(TileInteractor.tileset.tile_at(node.tile.x, node.tile.y - 1)))

        if TileInteractor.tileset.is_at(node.tile.x + 33, node.tile.y): # East
            result.append(Node(TileInteractor.tileset.tile_at(node.tile.x + 33, node.tile.y)))

        if TileInteractor.tileset.is_at(node.tile.x, node.tile.y + 33): # South
            result.append(Node(TileInteractor.tileset.tile_at(node.tile.x, node.tile.y + 33)))

        return result


    @staticmethod
    def get_path(entity, target):
        target_node = Node(target)
        starting_node = Node(TileInteractor.tileset.tile_at(entity.x, entity.y))
        current_node = starting_node
        open_list = []
        closed_list = []

        closed_list.append(current_node)

        while target_node not in open_list:
            for node in Pathfinder.get_adjacent_nodes(current_node):
                if (node.tile.passable) & (node not in closed_list) & (node not in open_list):
                    node.parent = current_node
                    node.f_score = Pathfinder.get_f_score(node, target_node)
                    open_list.append(node)

            if current_node in open_list:
                open_list.remove(current_node)
            closed_list.append(current_node)
            current_node = Pathfinder.get_next_current_node(open_list)

        target_node.parent = current_node
        current_node = target_node

        result = []
        result.add(current_node.tile)

        while current_node.parent is not None:
            result.insert(0, current_node.parent.tile)
            current_node = current_node.parent

        return result