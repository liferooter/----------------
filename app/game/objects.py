import pygame as pg
from pygame.math import Vector2

from time import time
from math import sin, cos, pi
from random import random

from app import config
from app.utils.functions import distance, sign, collide_rect
from app.game.sprite import VectoredSprite

# Directions
RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1

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
        self.speed: Vector2 = Vector2()

        # Save gravity value
        self.gravity: int = gravity

        # Initialize delta-time mechanizm
        self.last_tick: float = time()

        # Initialize some fields used by child classes
        self.on_land: bool = False
        self.on_edge: bool = False

    def calculate_dt(self) -> float:
        """
        Update delta-time to apply tick
        """
        now: float = time()
        dt: float = now - self.last_tick
        self.last_tick = now

        return dt

    def update(self):
        """
        Update sprite
        """
        super().update()

        dt: float = self.calculate_dt()

        self.on_land = False

        # Initialize variables to look if X or Y delta can be applied
        x_can_move: bool = True
        y_can_move: bool = True

        # Apply speed and gravity
        new_pos: Vector2 = Vector2(self.pos)
        new_speed: Vector2 = Vector2(self.speed)

        new_pos += self.speed * dt

        new_speed.y += self.gravity * dt
        new_pos.y += (self.gravity * dt ** 2) / 2

        # Collide with edges

        # Floor
        if new_pos.y + self.size.y > config.GAME_SIZE.y:
            new_pos.y = config.GAME_SIZE.y - self.size.y
            self.on_land = True
            self.on_edge = True
            y_can_move = False

        # Ceil
        if new_pos.y < 0:
            new_pos.y = 0
            self.on_edge = True
            y_can_move = False

        # Right
        if new_pos.x + self.size.x > config.GAME_SIZE.x:
            new_pos.x = config.GAME_SIZE.x - self.size.x
            self.on_edge = True
            x_can_move = False

        # Left
        if new_pos.x < 0:
            new_pos.x = 0
            self.on_edge = True
            x_can_move = False

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

            self.on_collide()

            if movement_direction[Y] == DOWN:
                if old_x_collide:
                    y_can_move = False
                    self.on_land = True
                    self.pos.y = platform.pos.y - self.size.y
            if movement_direction[Y] == UP:
                if old_x_collide:
                    y_can_move = False
                    self.pos.y = platform.pos.y + platform.size.y
            if movement_direction[X] == LEFT:
                if old_y_collide:
                    x_can_move = False
                    self.pos.x = platform.pos.x + platform.size.x
            if movement_direction[X] == RIGHT:
                if old_y_collide:
                    x_can_move = False
                    self.pos.x = platform.pos.x - self.size.x

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

        if self.on_land:
            self.speed.x = 0
            self.speed.y = 0

    def on_collide(self):
        pass


class Player(MaterialObject):
    """
    Player sprite
    """

    def __init__(self,
                 game: "Game object",
                 pos: Vector2,
                 color: str,
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

    def update(self):
        """
        Update Player sprite
        """
        self.handle_controls()
        super().update()

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

        if pressed[self.shortcuts['DROP']]:
            self.drop_bomb()

    def shoot(self):
        """
        Shoot action
        """
        # Be affected by shoot timeout
        if not self.shoot_from_time <= time():
            return
        self.shoot_from_time = time() + config.SHOOT_COOLDOWN

        Bullet(
            self.game,
            self
        )

    def drop_bomb(self):
        if not self.shoot_from_time <= time():
            return
        self.shoot_from_time = time() + config.SHOOT_COOLDOWN

        Bomb(self.game,
             Vector2(self.pos))


class Projectile(MaterialObject):

    def __init__(self,
                 game: "Game object",
                 color: str,
                 pos: Vector2,
                 size: Vector2,
                 speed: Vector2,
                 gravity: int,
                 is_killing: bool,
                 can_lie: bool):
        super().__init__(game, pos, size, gravity)

        # Fill surface with color
        self.image.fill(color)

        # Set speed
        self.speed = speed

        # Save whether to kill players
        self.is_killing: bool = is_killing

        # Save whether can lie
        self.can_lie = can_lie


    def update(self):
        super().update()

        if self.on_edge:
            self.when_on_edge()
        if self.on_land:
            self.when_on_land()

        if self.is_killing:
            pg.sprite.spritecollide(self, self.game.players, True)

    def when_on_edge(self):
        if not self.can_lie:
            self.kill()

    def when_on_land(self):
        if not self.can_lie:
            self.kill()

    def on_collide(self):
        if self.can_lie:
            self.kill()


class Bullet(Projectile):

    def __init__(self,
                 game: "Game object",
                 shooter: Player):
        super().__init__(game,
                         config.BULLET_COLOR,
                         shooter.rect.topleft - Vector2(config.BULLET_SIZE.x + 1, 0)
                            if shooter.direction == LEFT
                            else shooter.rect.topright + Vector2(1, 0),
                         config.BULLET_SIZE,
                         Vector2(config.BULLET_SPEED * shooter.direction, 0).rotate(config.SHOOT_ANGLE * -shooter.direction),
                         config.BULLET_GRAVITY,
                         True,
                         False)


class FireParticle(Projectile):
    """
    Fire particle sprite
    """

    def __init__(self,
                 game: "Game object",
                 pos: Vector2,
                 angle: int):
        super().__init__(game,
                         config.PARTICLE_COLOR,
                         pos,
                         config.PARTICLE_SIZE,
                         Vector2(-config.PARTICLE_SPEED, 0).rotate_rad(angle),
                         config.PARTICLE_GRAVITY,
                         True,
                         False)

class Bomb(Projectile):

    def __init__(self,
                 game: "Game object",
                 pos: Vector2):
        super().__init__(game,
                         config.BOMB_COLOR,
                         pos,
                         config.BOMB_SIZE,
                         Vector2(0, -config.BOMB_SPEED),
                         config.BOMB_GRAVITY,
                         False,
                         True)

    def when_on_land(self):

        for i in range(config.N_PARTICLES):
            FireParticle(self.game,
                         self.pos - Vector2(0, self.size.y),
                         random() * pi)
        self.kill()
