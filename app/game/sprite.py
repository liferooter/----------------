import pygame as pg

from app.utils.types import Vector


class VectoredSprite(pg.sprite.Sprite):
    def __init__(self, pos: Vector, size: Vector, *groups):
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

    @property
    def topleft(self) -> Vector:
        """
        Get position of top left corner
        """
        return self.pos

    @property
    def topright(self) -> Vector:
        """
        Get position of top right corner
        """
        return self.pos + Vector(self.size.x, 0)

    @property
    def bottomleft(self) -> Vector:
        """
        Get position of bottom left corner
        """
        return self.pos + Vector(0, self.size.y)

    @property
    def bottomright(self) -> Vector:
        """
        Get position of top left corner
        """
        return self.pos + self.size

    @property
    def top(self):
        """
        Get Y cooordinate of sprite's top edge
        """
        return self.pos.y

    @property
    def bottom(self):
        """
        Get Y cooordinate of sprite's bottom edge
        """
        return self.pos.y + self.size.y

    @property
    def left(self):
        """
        Get X cooordinate of sprite's left edge
        """
        return self.pos.x

    @property
    def right(self):
        """
        Get X cooordinate of sprite's right edge
        """
        return self.pos.x + self.size.x
