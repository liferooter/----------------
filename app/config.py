from typing import Any
from pygame.math import Vector2
import pygame as pg

TITLE: str = "Cuban Jumper"

BG_COLOR: str = '#347AFD'

PLAYER_SIZE: Vector2 = Vector2(14, 20)

PLAYERS: list[dict] = [
    {
        'COLOR': '#0000FF',
        'POSITION': Vector2(0, 0),
        'SHORTCUTS': {
            'RIGHT': pg.K_d,
            'LEFT': pg.K_a,
            'JUMP': pg.K_w,
            'SHOOT': pg.K_e,
            'BOMB': pg.K_q
        }
    },
    {
        'COLOR': '#FF0000',
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
        'COLOR': '#00FF00',
        'POSITION': Vector2(600, 750),
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
BULLET_GRAVITY: int = 300

BOMB_SIZE: int = Vector2(6, 6)
BOMB_COLOR: int = '#000000'
BOMB_SPEED: int = 100
BOMB_GRAVITY: int = 500

PARTICLE_SIZE: int = Vector2(4, 4)
PARTICLE_COLOR: int = '#FF0000'
PARTICLE_SPEED: int = 250
PARTICLE_GRAVITY: int = 500
N_PARTICLES = 8

SHOOT_COOLDOWN: float = 0.7
# Shoot angle in degrees
SHOOT_ANGLE: int = 2

PLATFORM_BG: str = '#FF7700'
PLATFORM_BORDER: str = '#000000'
PLATFORM_HEIGHT: str = 15

GAME_SIZE: Vector2 = Vector2(1500, 800)

UPS: int = 600
UPDATES_PER_FRAME: int = 10

MAP_FILE: str = "./maps/default.map"
MAP_CELL: Vector2 = Vector2(150, 80)
