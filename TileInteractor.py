from Tileset import Tileset


class TileInteractor:
    tileset = None

    @staticmethod
    def is_at(x, y):
        return TileInteractor.tileset.is_at(x, y)

    @staticmethod
    def tile_at(x, y):
        return TileInteractor.tileset.tile_at(x, y)

    @staticmethod
    def index_at(x, y):
        return TileInteractor.tileset.index_at(x, y)