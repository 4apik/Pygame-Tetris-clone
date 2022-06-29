import pygame.font

class Scoreboard:
    def __init__(self,  game_settings, screen, play_area):
        self.screen = screen
        self.play_area = play_area
        self.area_rect = play_area.rect
        self.text_color = game_settings.text_color
        self.bg_color = game_settings.bg_color
        self.score = 0

        self.font = pygame.font.SysFont(None, 48)

        self.prep_top_score()
        self.prep_score()
        self.prep_button()

    def prep_score(self):
        # Turn the score into a rendered image
        score_str = "Score: " + "{:,}".format(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score below the top score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = self.top_rect.bottom
        self.score_rect.left = self.area_rect.left

    def prep_top_score(self):
        with open("top_score.txt") as file:
            top_is = file.read()
        self.top_score = top_is
        # Turn the top score into a rendered image
        top_str = "Top was: " + self.top_score
        self.top_image = self.font.render(top_str, True, self.text_color)

        # Display the score at the top left of the screen
        self.top_rect = self.top_image.get_rect()
        self.top_rect.top = self.area_rect.top
        self.top_rect.left = self.area_rect.left

    def prep_button(self):
        self.button_image = self.font.render("New Game", True, self.text_color)
        self.button_rect = self.button_image.get_rect()
        self.button_rect.right = self.area_rect.right
        self.button_rect.top = self.area_rect.top

    def show_stuff(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.top_image, self.top_rect)
        self.screen.blit(self.button_image, self.button_rect)
