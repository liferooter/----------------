import pygame as pg
from time import time
from math import sin, cos

from app import config
from app.utils.vector import Vector
from app.game.sprite import VectoredSprite


class Walker(VectoredSprite):
    """
    Walker sprite
    """

    def __init__(self, pos: Vector, size: Vector, platforms, *groups):
        """
        Initialize walker sprited
        """
        super(Walker, self).__init__(pos, size,
                                     *groups)

        self.speed = Vector()

        self.platforms = platforms

        self.last_time = time()
        self.dt = 0

        self.on_land = False

    def update_dt(self):
        """
        Update delta-time to apply tick
        """
        now = time()
        self.dt = now - self.last_time
        self.last_time = now

    def update(self):
        """
        Update walker sprite
        """
        self.update_dt()

        self.on_land = False

        # Apply speed
        self.pos += self.speed * self.dt

        # Apply gravity
        self.speed.y += config.GRAVITY * self.dt
        self.pos.y += (config.GRAVITY * self.dt ** 2) / 2

        # Apply edges

        # Floor
        if self.bottom > config.GAME_SIZE.y:
            self.on_land = True
            self.pos.y = config.GAME_SIZE.y - self.size.y
            self.speed.y = min(0, self.speed.y)

        # Ceil
        if self.top < 0:
            self.pos.y = 0
            self.speed.y = max(0, self.speed.y)

        # Right
        if self.right > config.GAME_SIZE.x:
            self.pos.x = config.GAME_SIZE.x - self.size.x
            self.speed.x = min(0, self.speed.x)

        # Left
        if self.left < 0:
            self.pos.x = 0
            self.speed.x = max(0, self.speed.x)

        # Platforms
        for platform in pg.sprite.spritecollide(self, self.platforms, False):
            if platform.top < self.bottom and self.speed.y >= 0:
                self.on_land = True
                self.speed.y = min(0, self.speed.y)
                self.pos.y = platform.top - self.size.y

        # Stop if on land
        if self.on_land:
            self.speed.x = 0


class Player(Walker):
    """
    Player sprite
    """

    def __init__(self, pos, color, platforms, keys, *groups):
        """
        Initialize Player sprite
        """
        super(Player, self).__init__(pos, config.PLAYER_SIZE,
                                     platforms, *groups)

        self.image.fill(color)

        self.speed = Vector(100, -500)
        self.direction = 1

        self.keys = keys

        self.shoot_from = 0

    def update(self):
        """
        Update Player sprite
        """

        pressed = pg.key.get_pressed()
        if pressed[self.keys['UP']] and self.on_land:
            self.speed.y = min(
                self.speed.y, -config.PLAYER_JUMP)
        if pressed[self.keys['RIGHT']] and not pressed[self.keys['LEFT']]:
            self.speed.x = config.PLAYER_SPEED
        if not pressed[self.keys['RIGHT']] and pressed[self.keys['LEFT']]:
            self.speed.x = -config.PLAYER_SPEED

        # Calculate direction
        if self.speed.x > 0:
            self.direction = 1
        elif self.speed.x < 0:
            self.direction = -1

        if pressed[self.keys['SHOOT']] and self.shoot_from <= time():
            self.groups()[0].add(
                Bullet(self.platforms,
                       self.topleft if self.direction == -1 else self.topright + config.BULLET_SIZE,
                       self.direction,
                       self.groups()[1]))
            self.shoot_from = time() + config.SHOOT_COOLDOWN

        super(Player, self).update()


class Bullet(Walker):
    """
    Bullet sprite
    """

    def __init__(self, platforms, pos, direction, players, *groups):
        """
        Initialize bullet
        """
        super(Bullet, self).__init__(pos, config.BULLET_SIZE, platforms)

        self.players = players

        self.image.fill(config.BULLET_COLOR)

        self.speed = Vector(config.BULLET_SPEED
                            * direction
                            * cos(config.SHOOT_ANGLE),
                            -config.BULLET_SPEED
                            * sin(config.SHOOT_ANGLE))

    def update(self):
        """
        Update bullet
        """
        super(Bullet, self).update()

        pg.sprite.spritecollide(self, self.players, True)

        if self.on_land:
            self.kill()
