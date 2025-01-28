import pygame

from data.code.Button import KeyboardButton


class Game:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper3.png')
        self.exit_button = KeyboardButton(8, 6, 134, 39, (255, 255, 255), 'выйти', border_radius=2)
        self.line = pygame.image.load('data/textures/ui.png').subsurface((0, 557, 601, 93))
        self.attempts = 5
        self.font = pygame.font.Font(None, 50)

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))
        self.screen.blit(attempt_label, (289, 52))
        self.screen.blit(*self.exit_button.get_rect_coord())
        self.screen.blit(self.line, (0, 543))

    def reset(self):
        self.attempts = 5
