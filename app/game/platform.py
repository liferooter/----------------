import pygame as pg
from pygame.math import Vector2

from app import config
from app.game.sprite import VectoredSprite


class Platform(VectoredSprite):
    """
    Platform sprite
    """

    def __init__(self, pos: Vector2, width: (float, int), *groups):
        """
        Initialize Platform
        """
        super(Platform, self).__init__(Vector2(pos),
                                       Vector2(width, config.PLATFORM_HEIGHT),
                                       *groups)

        self.image.fill(config.PLATFORM_BG)
        pg.draw.rect(self.image, config.PLATFORM_BG,
                     self.image.get_bounding_rect(), 0)
