from pygame.math import Vector2

from app import config
from app.game.platform import Platform

def game_size():
    map_file = open(config.MAP_FILE)
    lines = list(map_file)
    return (config.MAP_CELL.x * max([len(line) - 1 for line in lines]),
            config.MAP_CELL.y * len(lines))

def import_map():
    """
    Import map from file
    """
    map_file = open(config.MAP_FILE)
    for y, line in enumerate(map_file):
        for x, sign in enumerate(line):
            if sign == '-':
                yield Platform(Vector2(config.MAP_CELL.x * x,
                                       config.MAP_CELL.y * y),
                               config.MAP_CELL.x)
