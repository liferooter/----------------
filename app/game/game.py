import pygame as pg
from pygame.math import Vector2

from app import config
from app.game.objects import Player
from app.utils.maps import import_map


class Game(object):
    def __init__(self):
        """
        Initialize Game object
        """
        # Set self.is_pending_quit
        self.is_pending_quit = False

        # Initialize pygame and its window
        pg.init()

        self.surface: pg.Surface = pg.display.set_mode(list(map(int, config.GAME_SIZE)))

        pg.display.set_caption(config.TITLE)

        self.bg: pg.Surface = pg.Surface(self.surface.get_size())
        self.bg.fill(config.BG_COLOR)

        self.bg = self.bg.convert()

        self.surface.blit(self.bg, (0, 0))

        # Initialize sprite groups
        self.material_objects: pg.sprite.Group = pg.sprite.Group()
        self.players: pg.sprite.Group = pg.sprite.Group()
        self.platforms: pg.sprite.Group = pg.sprite.Group(
            *import_map()
        )

        # Initialize players
        for player in config.PLAYERS[:config.N_PLAYERS]:
            Player(
                self,
                player['POSITION'],
                player['COLOR'],
                player['SHORTCUTS']
            )

    def run(self) -> int:
        """
        Run game loop
        """
        # Create clock object
        clock = pg.time.Clock()

        updates_counter = 0

        # Run main loop
        while True:
            update_frame = updates_counter == config.UPDATES_PER_FRAME
            if update_frame:
                updates_counter = 1
            else:
                updates_counter += 1

            # Quit if needed
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0
            if self.is_pending_quit and pg.key.get_pressed()[pg.K_ESCAPE]:
                return 0

            if len(self.players) > 1:
                self.update()

            if update_frame:
                self.produce_frame()

            # Tick clock
            clock.tick(config.UPS)

        # Return non-zero when program fails
        return 1

    def update(self):
        """
        Update all game objects
        """
        self.material_objects.update()

    def produce_frame(self):
        # Draw background
        self.surface.blit(self.bg, (0, 0))

        if len(self.players) > 1:
            # Draw if there are more players than one
            self.material_objects.draw(self.surface)
            self.platforms.draw(self.surface)

        else:
            # Else draw big circle and set is_pending_quit to True
            pg.draw.circle(self.surface, list(self.players)[0].color,
                           (config.GAME_SIZE / 2), 200)
            self.is_pending_quit = True

        # Flip display
        pg.display.flip()
