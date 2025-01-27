import pygame
from data.code.Button import MenuButton


class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper2 (ai-hd).png')
        self.separator1 = pygame.image.load('data/textures/ui1.png').subsurface((229, 505, 362, 32))
        self.separator2 = pygame.image.load('data/textures/ui1.png').subsurface((229, 505, 362, 32))

        self.mistake_upgrade = MenuButton(55, 136, 174, 102, 'data/textures/ui1.png', '-1 ошибка', 30,
                                          crop=(283, 129, 102, 57))
        self.letter_upgrade = MenuButton(240, 136, 174, 102, 'data/textures/ui1.png', '+1 буква', 30,
                                         crop=(283, 129, 102, 57))
        self.game_upgrade = MenuButton(54, 244, 174, 102, 'data/textures/ui1.png', 'Игра', 30, crop=(283, 129, 102, 57))

        self.button_custom = MenuButton(93, 428, 174, 102, 'data/textures/ui1.png', 'Кнопки', 30,
                                        crop=(283, 129, 102, 57))
        self.detail_custom = MenuButton(260, 428, 174, 102, 'data/textures/ui1.png', 'Детали', 30,
                                        crop=(283, 129, 102, 57))
        self.letter_custom = MenuButton(420, 428, 174, 102, 'data/textures/ui1.png', 'Буквы', 30,
                                        crop=(283, 129, 102, 57))
        self.background_custom = MenuButton(460, 550, 102, 70, 'data/textures/ui1.png', 'Фон', 30,
                                            crop=(283, 129, 102, 57))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        self.screen.blit(self.separator1, (36, 118))
        self.screen.blit(self.separator2, (36, 414))
        self.screen.blit(*self.mistake_upgrade.get_rect_coord())

        self.screen.blit(*self.letter_upgrade.get_rect_coord())
        self.screen.blit(*self.game_upgrade.get_rect_coord())

        self.screen.blit(*self.button_custom.get_rect_coord())
        self.screen.blit(*self.detail_custom.get_rect_coord())
        self.screen.blit(*self.letter_custom.get_rect_coord())
        self.screen.blit(*self.background_custom.get_rect_coord())

    def on_click(self, event):
        if self.active:
            for button in [self.letter_upgrade, self.game_upgrade, self.button_custom,
                           self.detail_custom, self.letter_custom]:
                if button.is_clicked(event):
                    return button
        else:
            return False