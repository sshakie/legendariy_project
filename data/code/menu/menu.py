import pygame
from data.code.Button import MenuButton


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper1 (hd).png')
        self.title = pygame.image.load('data/textures/ui1.png').subsurface((0, 0, 200, 75))
        self.play_button = MenuButton(175, 250, 250, 62, 'data/textures/ui1.png', 'Играть', 50, crop=(3, 77, 250, 62))
        self.shop_button = MenuButton(175, 325, 250, 58, 'data/textures/ui1.png', 'Ларёк', 50, crop=(3, 155, 250, 58))
        self.settings_button = MenuButton(175, 400, 250, 58, 'data/textures/ui1.png', 'Настройки', 50,
                                          crop=(3, 155, 250, 58))
        self.exit_button = MenuButton(175, 475, 250, 60, 'data/textures/ui1.png', '', 50, crop=(3, 226, 250, 60))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        self.screen.blit(self.title, (200, 150))
        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.settings_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())

    def on_click(self, event):
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                if button.is_clicked(event):
                    return button
        else:
            return False
