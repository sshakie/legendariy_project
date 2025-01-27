import pygame
from data.code.Button import *


def main():
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)

    money = 0
    menu_window = Menu(screen, active=True)
    shop_window = Shop(screen)
    game_window = Game(screen)

    running = True
    fps = 60
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if menu_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'Играть':
                    print(1)
                    pass  # TODO Логика при нажатии кнопки играть
                elif butt_text == 'Ларёк':
                    pass  # TODO Логика при нажатии кнопки ларек
                elif butt_text == 'Настройки':
                    pass  # TODO Логика при нажатии кнопки настройки
                else:
                    running = False
                    # Нажата кнопка выхода

            elif shop_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == '-1 ошибка':
                    pass
                elif butt_text == '+1 буква':
                    pass
                elif butt_text == 'Игра':
                    pass
                elif butt_text == 'Кнопки':
                    pass
                elif butt_text == 'Детали':
                    pass
                elif butt_text == 'Буквы':
                    pass
                elif butt_text == 'Фон':
                    pass

        # Логика переключения окон
        if menu_window.active:
            menu_window.render()
        elif shop_window.active:
            shop_window.render()
        elif game_window.active:
            game_window.render()

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper1 (hd).png')
        self.title = pygame.image.load('data/textures/ui1.png')
        self.play_button = MenuButton(175, 250, 250, 62, 'data/textures/ui1.png', 'Играть', 50, crop=(3, 77, 250, 62))
        self.shop_button = MenuButton(175, 325, 250, 58, 'data/textures/ui1.png', 'Ларёк', 50, crop=(3, 155, 250, 58))
        self.settings_button = MenuButton(175, 400, 250, 58, 'data/textures/ui1.png', 'Настройки', 50,
                                          crop=(3, 155, 250, 58))
        self.exit_button = MenuButton(175, 475, 250, 60, 'data/textures/ui1.png', '', 50, crop=(3, 226, 250, 60))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))

        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.settings_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())

    def on_click(self, event):
        if self.active:
            for button in [self.play_button, self.shop_button, self.settings_button, self.exit_button]:
                if button.is_clicked(event):
                    return button
        else:
            return False


class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper2 (ai-hd).png')

        self.mistake_upgrade = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', '-1 ошибка', 15,
                                          crop=(283, 129, 102, 57))
        self.letter_upgrade = MenuButton(250, 375, 100, 25, 'data/textures/ui1.png', '+1 буква', 15,
                                         crop=(283, 129, 102, 57))
        self.game_upgrade = MenuButton(250, 450, 100, 25, 'data/textures/ui1.png', 'Игра', 15, crop=(283, 129, 102, 57))

        self.button_custom = MenuButton(400, 300, 100, 25, 'data/textures/ui1.png', 'Кнопки', 15,
                                        crop=(283, 129, 102, 57))
        self.detail_custom = MenuButton(400, 375, 100, 25, 'data/textures/ui1.png', 'Детали', 15,
                                        crop=(283, 129, 102, 57))
        self.letter_custom = MenuButton(400, 450, 100, 25, 'data/textures/ui1.png', 'Буквы', 15, )
        self.background_custom = MenuButton(400, 525, 100, 25, 'data/textures/ui1.png', 'Фон', 15,
                                            crop=(283, 129, 102, 57))

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))

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


if __name__ == '__main__':
    main()
