import pygame

class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 0
        self.screen_height = 0
        # Other stuff
        self.bg_color = (0, 0, 0)

        self.text_color = (220, 222, 220)

        self.bg_image = pygame.image.load("images/space_right.jpg")

        self.square_size = 60

        self.shape_speed = 1

        self.game_active = False
