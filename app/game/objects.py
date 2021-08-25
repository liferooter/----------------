import pygame as pg
from pygame.math import Vector2

from time import time
from math import sin, cos, pi, sqrt
from random import random
from enum import Enum, auto

from app import config
from app.utils.functions import distance, sign, collide_rect
from app.game.sprite import VectoredSprite

# Directions

RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1

class CollideDirection(Enum):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()

# Coordinates
X = 0
Y = 1

class MaterialObject(VectoredSprite):
    """
    Basic class of material object sprite.
    Moves, affected by gravity,
    stops when falls on an edge or on a platform.
    """

    def __init__(self,
                 game: "Game object",
                 pos: Vector2,
                 size: Vector2,
                 gravity: int,
                 *groups: list[pg.sprite.Group]):
        """
        Initialize sprite
        """
        super().__init__(pos, size, game.material_objects, *groups)

        # Save game object
        self.game: "Game object" = game

        # Initialize object's speed
        self.speed: Vector2 = Vector2(0, 0)

        # Track collide direction
        self.collide_direction: CollideDirection = None

        # Save gravity value
        self.gravity: int = gravity

        # Initialize delta-time mechanizm
        self.last_tick: float = time()
        self.dt = 0

        # Initialize some fields used by child classes
        self.on_edge: bool = False

    def update_dt(self):
        """
        Update delta-time to apply tick
        """
        now: float = time()
        self.dt: float = now - self.last_tick
        self.last_tick = now

    def update(self):
        """
        Update sprite
        """
        super().update()

        self.update_dt()

        # Initialize variables to look if X or Y delta can be applied
        x_can_move: bool = True
        y_can_move: bool = True

        has_collision = False

        # Apply speed and gravity
        new_pos: Vector2 = Vector2(self.pos)
        new_speed: Vector2 = Vector2(self.speed)

        new_pos += self.speed * self.dt

        new_speed.y += self.gravity * self.dt
        new_pos.y += (self.gravity * self.dt ** 2) / 2

        # Collide with edges

        # Floor
        if new_pos.y + self.size.y > config.GAME_SIZE.y:
            new_pos.y = config.GAME_SIZE.y - self.size.y
            self.on_edge = True
            y_can_move = False
            has_collision = True

        # Ceil
        if new_pos.y < 0:
            new_pos.y = 0
            self.on_edge = True
            y_can_move = False
            has_collision = True

        # Right
        if new_pos.x + self.size.x > config.GAME_SIZE.x:
            new_pos.x = config.GAME_SIZE.x - self.size.x
            self.on_edge = True
            x_can_move = False
            has_collision = True

        # Left
        if new_pos.x < 0:
            new_pos.x = 0
            self.on_edge = True
            x_can_move = False
            has_collision = True

        movement_direction: (int, int) = (
            sign(new_pos.x - self.pos.x),
            sign(new_pos.y - self.pos.y)
        )

        # Platforms

        for platform in self.game.platforms:
            new_x_collide, new_y_collide = collide_rect(platform.rect, pg.sprite.Rect(*new_pos, *self.size))
            old_x_collide, old_y_collide = collide_rect(platform.rect, pg.sprite.Rect(*self.pos, *self.size))
            if not (new_x_collide and new_y_collide):
                continue

            has_collision = True

            if movement_direction[X] == LEFT:
                if old_y_collide:
                    x_can_move = False
                    self.pos.x = platform.pos.x + platform.size.x
            if movement_direction[X] == RIGHT:
                if old_y_collide:
                    x_can_move = False
                    self.pos.x = platform.pos.x - self.size.x
            if movement_direction[Y] == DOWN:
                if old_x_collide:
                    y_can_move = False
                    self.pos.y = platform.pos.y - self.size.y
            if movement_direction[Y] == UP:
                if old_x_collide:
                    y_can_move = False
                    self.pos.y = platform.pos.y + platform.size.y

            self.on_collide()

        # Apply changes
        if not x_can_move:
            self.speed.x = 0
        else:
            self.speed.x = new_speed.x
            self.pos.x = new_pos.x

        if not y_can_move:
            self.speed.y = 0
        else:
            self.speed.y = new_speed.y
            self.pos.y = new_pos.y

        if not y_can_move and movement_direction[Y] == DOWN:
            self.collide_direction = CollideDirection.BOTTOM
        elif not y_can_move and movement_direction[Y] == UP:
            self.collide_direction = CollideDirection.TOP
        elif not x_can_move and movement_direction[X] == RIGHT:
            self.collide_direction = CollideDirection.RIGHT
        elif not x_can_move and movement_direction[X] == LEFT:
            self.collide_direction = CollideDirection.LEFT
        elif not has_collision:
            self.collide_direction = None

        if self.on_land:
            self.speed.x = 0
            self.speed.y = 0

    @property
    def on_land(self):
        return self.collide_direction == CollideDirection.BOTTOM

    def on_collide(self):
        pass


class Player(MaterialObject):
    """
    Player sprite
    """

    def __init__(self,
                 game: "Game object",
                 pos: Vector2,
                 color: (int, int, int),
                 shortcuts: dict[str, int]):
        """
        Initialize Player sprite
        """
        super().__init__(game,
                         pos,
                         config.PLAYER_SIZE,
                         config.PLAYER_GRAVITY,
                         game.players)

        # Fill image with color and save color
        self.image.fill(color)
        self.color = color

        # Set default direction
        self.direction = RIGHT

        # Save shortcuts
        self.shortcuts = shortcuts

        # Initialize shoot timeout mechanizm
        self.shoot_from_time = 0

        self.bombs = []

    def update(self):
        """
        Update Player sprite
        """
        super().update()
        self.handle_controls()

    def handle_controls(self):
        """
        Handle player controls
        """
        pressed = pg.key.get_pressed()
        if pressed[self.shortcuts['JUMP']] and self.on_land:
            self.speed.y = config.PLAYER_JUMP * UP
        if pressed[self.shortcuts['RIGHT']] and not pressed[self.shortcuts['LEFT']]:
            self.speed.x = config.PLAYER_SPEED * RIGHT
        if not pressed[self.shortcuts['RIGHT']] and pressed[self.shortcuts['LEFT']]:
            self.speed.x = config.PLAYER_SPEED * LEFT

        # Calculate direction
        if self.speed.x > 0:
            self.direction = RIGHT
        elif self.speed.x < 0:
            self.direction = LEFT

        if pressed[self.shortcuts['SHOOT']]:
            self.shoot()

        if pressed[self.shortcuts['BOMB']]:
            self.launch_rocket()

    def shoot(self):
        """
        Shoot action
        """
        # Be affected by shoot timeout
        if not self.shoot_from_time <= time():
            return
        self.shoot_from_time = time() + config.SHOOT_COOLDOWN

        self.bombs.append(Bullet(
            self.game,
            self
        ))

    def launch_rocket(self):
        if not self.shoot_from_time <= time():
            return
        self.shoot_from_time = time() + config.SHOOT_COOLDOWN

        self.bombs.append(Rocket(
            self.game,
            self
        ))

    def kill(self):
        super().kill()
        while self.bombs:
            self.bombs.pop().boom()


class Projectile(MaterialObject):

    def __init__(self,
                 game: "Game object",
                 color: (int, int, int),
                 pos: Vector2,
                 size: Vector2,
                 speed: Vector2,
                 gravity: int,
                 is_killing: bool,
                 can_lie: bool,
                 shooter: Player):
        super().__init__(game, pos, size, gravity)

        # Fill surface with color
        self.image.fill(color)

        # Set speed
        self.speed = speed

        # Save whether to kill players
        self.is_killing: bool = is_killing

        # Save whether can lie
        self.can_lie = can_lie

        self.shooter = shooter

    def update(self):
        super().update()

        if self.on_edge:
            self.when_on_edge()
        if self.on_land:
            self.when_on_land()

        for player in pg.sprite.spritecollide(self, self.game.players, False):
            self.on_collide_player(player)

    def when_on_edge(self):
        if not self.can_lie:
            self.kill()

    def when_on_land(self):
        if not self.can_lie:
            self.kill()

    def on_collide(self):
        if not self.can_lie:
            self.kill()

    def on_collide_player(self, player: Player):
        if self.is_killing and player != self.shooter:
            player.kill()


class Bomb(Projectile):
    def boom(self):
        super().kill()
        for i in range(config.N_PARTICLES):
            FireParticle(self.game,
                         self.pos + (
                            Vector2(0, self.size.y)
                                if self.collide_direction == CollideDirection.TOP else
                            Vector2(0, -self.size.y)
                                if self.collide_direction == CollideDirection.BOTTOM else
                            Vector2(-self.size.x, 0)
                                if self.collide_direction == CollideDirection.RIGHT else
                            Vector2(self.size.x, 0)
                                if self.collide_direction == CollideDirection.LEFT else
                            Vector2(0)
                         ),
                         random() * pi
                            if self.collide_direction == CollideDirection.BOTTOM else
                         random() * pi + pi
                            if self.collide_direction == CollideDirection.TOP else
                         random() * pi + pi / 2
                            if self.collide_direction == CollideDirection.RIGHT else
                         random() * pi - pi / 2
                            if self.collide_direction == CollideDirection.LEFT else
                         random() * 2 * pi,
                         self.shooter
            )


class Bullet(Bomb):

    def __init__(self,
                 game: "Game object",
                 shooter: Player):
        super().__init__(game,
                         tuple(map(lambda x: x * 0.6, list(shooter.color))),
                         shooter.rect.topleft - Vector2(config.BULLET_SIZE.x + 1, 0)
                            if shooter.direction == LEFT
                            else shooter.rect.topright + Vector2(1, 0),
                         config.BULLET_SIZE,
                         Vector2(config.BULLET_SPEED * shooter.direction, 0).rotate(config.SHOOT_ANGLE * -shooter.direction),
                         config.BULLET_GRAVITY,
                         True,
                         False,
                         shooter)

    def kill(self):
        self.boom()


class FireParticle(Projectile):
    """
    Fire particle sprite
    """

    def __init__(self,
                 game: "Game object",
                 pos: Vector2,
                 angle: int,
                 shooter: Player):
        super().__init__(game,
                         config.PARTICLE_COLOR,
                         pos,
                         config.PARTICLE_SIZE,
                         Vector2(-config.PARTICLE_SPEED, 0).rotate_rad(angle),
                         config.PARTICLE_GRAVITY,
                         True,
                         False,
                         shooter)

class Rocket(Bomb):

    def __init__(self,
                 game: "Game object",
                 shooter: Player):
        super().__init__(game,
                         config.ROCKET_COLOR,
                         Vector2(shooter.pos),
                         config.ROCKET_SIZE,
                         Vector2(config.ROCKET_SPEED, 0),
                         0,
                         False,
                         False,
                         shooter)
        self.shooter: Player = shooter

        self.speed.rotate_ip(self.speed.angle_to(self.get_target_direction()))

    def get_target_direction(self):
        min_distance: Vector2 = None
        nearest_player: Player = None
        for player in self.game.players:
            if player == self.shooter:
                continue
            if nearest_player == None \
                or min_distance.length() > distance(self, player).length():
                min_distance = distance(player, self)
                nearest_player = player

        return min_distance

    def update(self):
        super().update()

        angle: float = self.get_target_direction().angle_to(Vector2(1, 0)) \
                            - self.speed.angle_to(Vector2(1, 0))
        if 180 >= angle % 360 > 0:
            self.image.fill((255, 0, 0))
            self.speed.rotate_ip(-config.ROCKET_ROTATION * self.dt)
        elif 180 < angle % 360:
            self.image.fill((0, 0, 255))
            self.speed.rotate_ip(config.ROCKET_ROTATION * self.dt)

    def on_collide_player(self, player: Player):
        if player != self.shooter:
            self.kill()

    def kill(self):
        self.boom()
