import pygame
from data.code.Button import *


def main():
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)

    money = 0
    menu_window = Menu(screen)
    shop_window = Shop(screen, active=True)
    game_window = Game(screen)

    running = True
    fps = 60
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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


main()
