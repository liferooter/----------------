import pygame as pg

from app import config
from app.utils.types import Vector
from app.game.sprite import VectoredSprite


class Platform(VectoredSprite):
    """
    Platform sprite
    """

    def __init__(self, pos: Vector, width: (float, int), *groups):
        """
        Initialize Platform
        """
        super(Platform, self).__init__(Vector(pos),
                                       Vector(width, config.PLATFORM_HEIGHT),
                                       *groups)

        self.image.fill(config.PLATFORM_BG)
        pg.draw.rect(self.image, config.PLATFORM_BORDER,
                     self.image.get_bounding_rect(), 1)
