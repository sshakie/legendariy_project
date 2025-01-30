import pygame
from data.code.Button import Button
from data.code.class_config import Config


class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper2.png')
        self.no_problems = pygame.image.load('data/textures/ui.png').subsurface((810, 0, 600, 800))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((135, 0, 33, 30))
        self.font = pygame.font.Font(None, 30)
        self.config = Config()
        self.money = self.config.money
        self.money_label = self.font.render(self.money[6:], True, (100, 0, 0))
        self.separator1 = pygame.image.load('data/textures/ui.png').subsurface((169, 0, 600, 40))
        self.separator2 = pygame.image.load('data/textures/ui.png').subsurface((169, 0, 600, 40))
        self.upgrade_text = pygame.image.load('data/textures/ui.png').subsurface((299, 130, 294, 57))
        self.customization_text = pygame.image.load('data/textures/ui.png').subsurface((299, 188, 335, 56))

        self.mistake_upgrade = Button(29, 197, 134, 75, 'data/textures/ui.png', 'право на ошибку', 20,
                                      crop=(0, 0, 134, 75))
        self.letter_upgrade = Button(189, 196, 134, 75, 'data/textures/ui.png', 'раскрыть букву', 20,
                                     crop=(0, 0, 134, 75))
        self.game_upgrade = Button(29, 277, 134, 75, 'data/textures/ui.png', 'игра-капча', 20, crop=(0, 0, 134, 75))

        self.button_custom = Button(111, 427, 134, 75, 'data/textures/ui.png', 'кнопки', 30,
                                    crop=(0, 0, 134, 75))
        self.detail_custom = Button(271, 427, 134, 75, 'data/textures/ui.png', 'детали', 30,
                                    crop=(0, 0, 134, 75))
        self.letter_custom = Button(431, 427, 134, 75, 'data/textures/ui.png', 'буквы', 30,
                                    crop=(0, 0, 134, 75))
        self.background_custom = Button(472, 512, 86, 59, 'data/textures/ui.png', 'фон', 30,
                                        crop=(0, 76, 86, 59))

        self.exit_button = Button(46, 657, 509, 75, 'data/textures/ui.png', '<- назад', 0, crop=(174, 41, 509, 75))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        self.screen.blit(self.no_problems, (0, 0))
        self.screen.blit(self.coin, (551, 17))
        self.screen.blit(self.money_label, (535, 24))
        self.screen.blit(self.separator1, (0, 160))
        self.screen.blit(self.separator2, (0, 390))
        self.screen.blit(self.upgrade_text, (143, 119))
        self.screen.blit(self.customization_text, (125, 360))

        self.screen.blit(*self.mistake_upgrade.get_rect_coord())
        self.screen.blit(*self.letter_upgrade.get_rect_coord())
        self.screen.blit(*self.game_upgrade.get_rect_coord())

        self.screen.blit(*self.button_custom.get_rect_coord())
        self.screen.blit(*self.detail_custom.get_rect_coord())
        self.screen.blit(*self.letter_custom.get_rect_coord())
        self.screen.blit(*self.background_custom.get_rect_coord())

        self.screen.blit(*self.exit_button.get_rect_coord())

    def on_click(self, event):
        if self.active:
            for button in [self.letter_upgrade, self.game_upgrade, self.button_custom,
                           self.detail_custom, self.letter_custom, self.exit_button]:
                if button.is_clicked(event):
                    return button
        else:
            return False