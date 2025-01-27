import pygame


class Game:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper3 (hd).png')
        self.attempts = 5
        self.font = pygame.font.Font(None, 30)

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (255, 255, 255))
        self.screen.blit(attempt_label, (100, 50))

    def reset(self):
        self.attempts = 5
