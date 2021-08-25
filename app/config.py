from typing import Any
from pygame.math import Vector2
import pygame as pg

from app.utils.maps import game_size

TITLE: str = "Cuban Jumper"

BG_COLOR: str = '#FFDDDD'

PLAYER_SIZE: Vector2 = Vector2(14, 20)

PLAYERS: list[dict] = [
    {
        'COLOR': (0, 0, 255),
        'POSITION': Vector2(0, 50),
        'SHORTCUTS': {
            'RIGHT': pg.K_d,
            'LEFT': pg.K_a,
            'JUMP': pg.K_w,
            'SHOOT': pg.K_e,
            'BOMB': pg.K_q
        }
    },
    {
        'COLOR': (255, 0, 0),
        'POSITION': Vector2(1400, 50),
        'SHORTCUTS': {
            'RIGHT': pg.K_RIGHT,
            'LEFT': pg.K_LEFT,
            'JUMP': pg.K_UP,
            'SHOOT': pg.K_DOWN,
            'BOMB': pg.K_RSHIFT
        }
    },
    {
        'COLOR': (0, 255, 0),
        'POSITION': Vector2(600, 50),
        'SHORTCUTS': {
            'RIGHT': pg.K_j,
            'LEFT': pg.K_g,
            'JUMP': pg.K_y,
            'SHOOT': pg.K_h,
            'BOMB': pg.K_SPACE
        }
    }
]

N_PLAYERS: int = 3

PLAYER_SPEED: int = 300
PLAYER_GRAVITY: int = 2000
PLAYER_JUMP: int = 700

BULLET_SIZE: int = Vector2(5, 5)
BULLET_COLOR: int = '#FFFF00'
BULLET_SPEED: int = 1000
BULLET_GRAVITY: int = 250

ROCKET_SIZE: int = Vector2(6, 6)
ROCKET_COLOR: int = '#000000'
ROCKET_SPEED: int = 400
ROCKET_ROTATION: int = 360

PARTICLE_SIZE: int = Vector2(4, 4)
PARTICLE_COLOR: int = '#AA9900'
PARTICLE_SPEED: int = 400
PARTICLE_GRAVITY: int = 500
N_PARTICLES = 8

SHOOT_COOLDOWN: float = 0.7
# Shoot angle in degrees
SHOOT_ANGLE: int = 3

PLATFORM_BG: str = '#8888AA'
PLATFORM_HEIGHT: int = 15

UPS: int = 240
UPDATES_PER_FRAME: int = 4

MAP_FILE: str = "./maps/default.map"
MAP_CELL: Vector2 = Vector2(150, 80)

DRAW_COLOR: str = PLATFORM_BG

# DO NOT EDIT!
# IDK WHY THIS IS IN CONFIG
GAME_SIZE: Vector2 = Vector2(game_size())
