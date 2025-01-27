import pygame
from data.code.Button import *

class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper1 (hd).png')
        self.title = pygame.image.load('data/textures/ui1.png')
        self.play_button = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'Играть', 30, указать координаты облбасти с изображением кнопки)
        self.shop_button = MenuButton(250, 375, 100, 25, 'data/textures/ui1.png', 'Ларёк', 30, указать координаты облбасти с изображением кнопки)
        self.settings_button = MenuButton(250, 450, 100, 25, 'data/textures/ui1.png', 'Настройки', 30, указать координаты облбасти с изображением кнопки)
        self.exit_button = MenuButton(250, 525, 100, 25, 'data/textures/ui1.png', 'Выйти', 30, указать координаты облбасти с изображением кнопки)

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))

        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.settings_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())

class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper2 (ai-hd).png')

        self.mistake_upgrade = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', '-1 ошибка', 15, указать координаты облбасти с изображением кнопки)
        self.letter_upgrade = MenuButton(250, 375, 100, 25, 'data/textures/ui1.png', '+1 буква', 15, указать координаты облбасти с изображением кнопки)
        self.game_upgrade = MenuButton(250, 450, 100, 25, 'data/textures/ui1.png', 'Игра', 15, указать координаты облбасти с изображением кнопки)

        self.button_custom = MenuButton(400, 300, 100, 25, 'data/textures/ui1.png', 'Кнопки', 15, указать координаты облбасти с изображением кнопки)
        self.detail_custom = MenuButton(400, 375, 100, 25, 'data/textures/ui1.png', 'Детали', 15, указать координаты облбасти с изображением кнопки)
        self.letter_custom = MenuButton(400, 450, 100, 25, 'data/textures/ui1.png', 'Буквы', 15, )
        self.background_custom = MenuButton(400, 525, 100, 25, 'data/textures/ui1.png', 'Фон', 15, указать координаты облбасти с изображением кнопки)

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))

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


if __name__ == '__main__':
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
