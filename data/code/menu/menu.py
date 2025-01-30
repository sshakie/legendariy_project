import pygame
from data.code.Button import Button
from data.code.class_config import Config


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper1.png')
        self.title = pygame.image.load('data/textures/ui.png').subsurface((0, 136, 298, 108))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((135, 0, 33, 30))
        self.font = pygame.font.Font(None, 30)
        self.config = Config()
        self.money = self.config.money
        self.money_label = self.font.render(self.money[6:], True, (100, 0, 0))
        self.play_button = Button(101, 380, 404, 118, 'data/textures/ui.png', 'Играть', 50, crop=(0, 245, 404, 118), selected_coords=(405, 245))
        self.shop_button = Button(101, 506, 403, 94, 'data/textures/ui.png', 'Ларёк', 50, crop=(0, 364, 403, 94), selected_coords=(404, 364))
        self.exit_button = Button(101, 623, 403, 97, 'data/textures/ui.png', '', 50, crop=(0, 459, 403, 97), selected_coords=(404, 459))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        self.screen.blit(self.title, (143, 76))
        self.screen.blit(self.coin, (551, 17))
        self.screen.blit(self.money_label, (535, 24))
        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())

    def on_click(self, event):
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                if button.is_clicked(event):
                    return button
        else:
            return False

    def selecting_button(self):
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                button.selecting()