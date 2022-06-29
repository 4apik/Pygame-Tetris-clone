import pygame
class Play_area:
    def __init__(self, game_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = game_settings.bg_color
        self.settings = game_settings

        # Create an area's rect and center it on the screen
        self.rect = pygame.Rect(0, 0, 600, 900)
        self.rect.center = self.screen_rect.center

        self.make_frame()

    def show_area(self):
        pygame.draw.rect(self.screen, self.bg_color, self.frame_top)
        pygame.draw.rect(self.screen, self.bg_color, self.frame_left)
        pygame.draw.rect(self.screen, self.bg_color, self.frame_right)
        pygame.draw.rect(self.screen, self.bg_color, self.frame_bottom)

    def make_frame(self):
        self.frame_top = pygame.Rect(0, 0, self.rect.width, self.settings.square_size + 3)
        self.frame_left = pygame.Rect(0, 0, 2, self.rect.height)
        self.frame_right = pygame.Rect(0, 0, 2, self.rect.height)
        self.frame_bottom = pygame.Rect(0, 0, self.rect.width, 2)

        # And place it
        self.frame_top.top = self.rect.top
        self.frame_top.left = self.rect.left

        self.frame_left.top = self.rect.top
        self.frame_left.right = self.rect.left

        self.frame_right.top = self.rect.top
        self.frame_right.left = self.rect.right

        self.frame_bottom.top = self.rect.bottom
        self.frame_bottom.left = self.rect.left
