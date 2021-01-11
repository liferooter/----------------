from app import config
from app.utils.vector import Vector
from app.game.platform import Platform


def import_map():
    """
    Import map from file
    """
    map_file = open(config.MAP_FILE)
    for y, line in enumerate(map_file):
        for x, sign in enumerate(line):
            if sign == '-':
                yield Platform(Vector(config.MAP_CELL.x * x,
                                      config.MAP_CELL.y * y),
                               config.MAP_CELL.x)
