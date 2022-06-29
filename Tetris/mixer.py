import pygame.mixer


class Mixer():
    "A class for playing music and sound effects."
    def __init__(self):
        pygame.mixer.init()
        self.landed = pygame.mixer.Sound('sounds/Single-clap-sound-effect.mp3')
        self.rotate = pygame.mixer.Sound('sounds/robot-movement-sound-effects.mp3')
        self.lost = pygame.mixer.Sound('sounds/Duck-quack.mp3')
        self.bg_music = pygame.mixer.Sound('sounds/dark-intro-synth.mp3')
        pygame.mixer.Sound.set_volume(self.bg_music, 0.5)

    def play_landed(self):
        pygame.mixer.Sound.play(self.landed)

    def play_rotate(self):
        pygame.mixer.Sound.play(self.rotate, maxtime=100)

    def play_lost(self):
        pygame.mixer.Sound.play(self.lost, maxtime=300)

    def play_bg_music(self):
        pygame.mixer.Sound.play(self.bg_music, loops=-1)
