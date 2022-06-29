import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from scoreboard import Scoreboard
from play_area import Play_area
from shape import Shape
from mixer import Mixer

def run_game():
    pygame.init()
    game_settings = Settings()

    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption('Tetris')

    # Make a play area and a scoreboard. The "New Game" button is in sb
    play_area = Play_area(game_settings, screen)
    sb = Scoreboard(game_settings, screen, play_area)

    mix = Mixer()
    mix.play_bg_music()

    squares = Group()
    # Make the first shape
    shape = Shape(screen, play_area, game_settings)
    while True:
        gf.check_events(game_settings, shape, squares, sb, mix)
        if game_settings.game_active:
            gf.check_shape(shape, play_area, squares, game_settings, sb, mix)
        gf.update_screen(screen, game_settings, sb, play_area, squares, shape)


if __name__ == '__main__':
    run_game()
