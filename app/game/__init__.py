import pygame as pg
from pygame.math import Vector2

from app import config
from app.game.walkers import Player, Bot, Bullet
from app.utils.maps import import_map


class Game(object):
    def __init__(self):
        """
        Initialize Game object
        """
        pg.init()

        self.surface = pg.display.set_mode(list(map(int, config.GAME_SIZE)))

        pg.display.set_caption(config.TITLE)

        self.bg = pg.Surface(self.surface.get_size())
        self.bg.fill(config.BG_COLOR)
        self.bg = self.bg.convert()

        self.surface.blit(self.bg, (0, 0))

        self.walkers = pg.sprite.Group()
        self.players = pg.sprite.Group()

        self.platforms = pg.sprite.Group(
            *import_map()
        )

        self.player1 = Player(config.PLAYER_START[0],
                              '#FF0000',
                              self.platforms,
                              {
                                  'RIGHT': pg.K_RIGHT,
                                  'LEFT': pg.K_LEFT,
                                  'UP': pg.K_UP,
                                  'SHOOT': pg.K_DOWN,
        },
            self.walkers, self.players)

        # self.player2 = Player(config.PLAYER_START[1],
        #                       '#0000FF',
        #                       self.platforms,
        #                       {
        #                           'RIGHT': pg.K_d,
        #                           'LEFT': pg.K_a,
        #                           'UP': pg.K_w,
        #                           'SHOOT': pg.K_s,
        # },
        #     self.walkers, self.players)

        self.bot1 = Bot(Vector2(500, 500),
                        '#00FF00',
                        self.platforms,
                        self.walkers, self.players)

    def run(self) -> int:
        """
        Run game loop
        """
        clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0

            self.surface.blit(self.bg, (0, 0))

            if len(self.players) > 1:
                self.update()
            else:
                pg.draw.circle(self.surface, list(self.players)[0].color,
                               (config.GAME_SIZE / 2), 200)

            pg.display.flip()
            clock.tick(config.FPS)
        return 1

    def update(self):
        """
        Update and draw all game objects
        """
        self.walkers.update()
        self.walkers.draw(self.surface)

        self.platforms.draw(self.surface)
