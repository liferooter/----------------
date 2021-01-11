import sys

from app.game import Game

global game
game = Game()
sys.exit(game.run())
