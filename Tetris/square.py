import pygame
from pygame.sprite import Sprite

class Square(Sprite):
    """A class to represent squares that figures are made out of"""

    def __init__(self, game_settings, screen, color):
        super(Square, self).__init__()
        self.screen = screen
        self.size = game_settings.square_size
        self.color = color

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.a_part = True
        self.connections = [] # Remembers where it was attached, required for shape rotation

    def draw_square(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
