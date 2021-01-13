import pygame as pg
from pygame.math import Vector2
from time import time
from math import sin, cos

from app import config
from app.utils.functions import distance, sign
from app.game.sprite import VectoredSprite


class Walker(VectoredSprite):
    """
    Walker sprite
    """

    def __init__(self,
                 pos: Vector2,
                 size: Vector2,
                 platforms,
                 *groups,
                 gravity=config.GRAVITY):
        """
        Initialize walker sprited
        """
        super(Walker, self).__init__(pos, size,
                                     *groups)

        self.platform = None

        self.speed = Vector2()

        self.gravity = gravity

        self.platforms = platforms

        self.last_time = time()
        self.dt = 0

        self.on_land = False
        self.on_edge = False
        self.in_platform = False

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

        self.before_update()

        self.update_dt()

        self.on_land = False
        self.platform = None

        # Apply speed
        self.pos += self.speed * self.dt

        # Apply gravity
        self.speed.y += self.gravity * self.dt
        self.pos.y += (self.gravity * self.dt ** 2) / 2

        # Apply edges

        # Floor
        if self.rect.bottom >= config.GAME_SIZE.y:
            self.on_land = True
            self.on_edge = True
            self.pos.y = config.GAME_SIZE.y - self.size.y
            self.speed.y = min(0, self.speed.y)

        # Ceil
        if self.rect.top <= 0:
            self.on_edge = True
            self.pos.y = 0
            self.speed.y = max(0, self.speed.y)

        # Right
        if self.rect.right >= config.GAME_SIZE.x:
            self.on_edge = True
            self.pos.x = config.GAME_SIZE.x - self.size.x
            self.speed.x = min(0, self.speed.x)

        # Left
        if self.rect.left <= 0:
            self.on_edge = True
            self.pos.x = 0
            self.speed.x = max(0, self.speed.x)

        # Platforms
        collided_platforms = pg.sprite.spritecollide(
            self, self.platforms, False)

        for platform in collided_platforms:
            if platform.rect.top < self.rect.bottom \
                and self.speed.y >= 0 \
                    and not self.in_platform:
                self.on_land = True
                self.platform = platform
                self.speed.y = min(0, self.speed.y)
                self.pos.y = platform.rect.top - self.size.y
        self.in_platform = not len(collided_platforms) == 0

        # Stop if on land
        if self.on_land:
            self.speed.x = 0

        self.after_update()

    def before_update(self):
        """
        Before update hook
        """

    def after_update(self):
        """
        After update hook
        """


class Player(Walker):
    """
    Player sprite
    """

    def __init__(self, pos, color, platforms, keys={}, *groups):
        """
        Initialize Player sprite
        """
        super(Player, self).__init__(pos, config.PLAYER_SIZE,
                                     platforms, *groups)

        self.image.fill(color)
        self.color = color

        self.direction = 1

        self.keys = keys

        self.shoot_from = 0

    def update(self):
        """
        Update Player sprite
        """

        super(Player, self).update()

    def before_update(self):
        self.handle_controls()

    def handle_controls(self):
        """
        Handle player controls
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

        if pressed[self.keys['SHOOT']]:
            self.shoot()

    def shoot(self):
        """
        Shoot action
        """
        if not self.shoot_from <= time():
            return
        self.groups()[0].add(
            Bullet(self.platforms,
                   self.rect.topleft
                   if self.direction == -1
                   else self.rect.topright,
                   self.direction,
                   self.groups()[1]))
        self.shoot_from = time() + config.SHOOT_COOLDOWN


class Bot(Player):
    def __init__(self, pos, color, platforms, *groups):
        super(Bot, self).__init__(pos, color, platforms, {}, *groups)

        self.target = None

    def handle_controls(self):
        """
        Run bot strategy
        """
        players = list(self.groups()[0])

        new_target = players[0]
        for player in players:
            if player is not self \
                and distance(self, player).length() < \
                    distance(self, new_target).length():
                new_target = player
        self.target = new_target
        target_distance = distance(self, self.target)
        if target_distance.length() < config.GAME_SIZE.length() / 2:
            if target_distance.x < -config.PLAYER_SIZE.x * 5:
                self.speed.x = config.PLAYER_SPEED
            elif target_distance.x > config.PLAYER_SIZE.x * 5:
                self.speed.x = -config.PLAYER_SPEED

            if (-config.PLAYER_SIZE.y / 2 > target_distance.y
                or target_distance.y > config.PLAYER_SIZE.y / 2)\
                    and self.on_land:
                self.speed.y = -config.PLAYER_JUMP

        # Calculate direction
        if self.speed.x > 0:
            self.direction = 1
        elif self.speed.x < 0:
            self.direction = -1

        if abs(target_distance.y) < config.PLAYER_SIZE.y:
            self.shoot()

    @property
    def state(self):
        return self.states[-1]


class Bullet(Walker):
    """
    Bullet sprite
    """

    def __init__(self, platforms, pos, direction, players, *groups):
        """
        Initialize bullet
        """
        super(Bullet, self).__init__(pos, config.BULLET_SIZE,
                                     platforms, gravity=config.BULLET_GRAVITY)

        self.players = players

        self.image.fill(config.BULLET_COLOR)

        self.speed = Vector2(config.BULLET_SPEED
                             * direction
                             * cos(config.SHOOT_ANGLE),
                             -config.BULLET_SPEED
                             * sin(config.SHOOT_ANGLE))

    def update(self):
        """
        Update bullet
        """
        super(Bullet, self).update()

        if self.on_land or self.on_edge:
            self.kill()

        pg.sprite.spritecollide(self, self.players, True)
