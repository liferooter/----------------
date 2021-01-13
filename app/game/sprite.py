import pygame as pg
from pygame.math import Vector2


class VectoredSprite(pg.sprite.Sprite):
    def __init__(self, pos: Vector2, size: Vector2, *groups):
        """
        Initialize VectoredSprite by its position, size and groups
        """
        super(VectoredSprite, self).__init__(*groups)

        self.pos = pos
        self.size = size

        self.image = pg.surface.Surface(self.rect.size)

    @property
    def rect(self) -> pg.sprite.Rect:
        """
        Get sprite rectangle
        """
        return pg.sprite.Rect(*self.pos, *self.size)
