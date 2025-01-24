import pygame
from data.code.Button import *


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.title = pygame.image.load('data/textures/ui1.png')
        self.play_button = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'Играть', 30, screen)
        self.shop_button = MenuButton(250, 375, 100, 25, 'data/textures/ui1.png', 'Ларёк', 30, screen)
        self.settings_button = MenuButton(250, 450, 100, 25, 'data/textures/ui1.png', 'Настройки', 30, screen)
        self.exit_button = MenuButton(250, 525, 100, 25, 'data/textures/ui1.png', 'Выйти', 30, screen)


class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.upgrade_title = pygame.image.load('data/textures/ui1.png')
        self.customization_title = pygame.image.load('data/textures/ui1.png')
        self.separator1 = pygame.image.load('data/textures/ui1.png')
        self.separator2 = pygame.image.load('data/textures/ui1.png')
        self.separator3 = pygame.image.load('data/textures/ui1.png')
        # self.hardcore_button = pygame.draw.rect(screen)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)

    menu_window = Menu(screen, active=True)
    shop_window = Menu(screen)
    running = True
    v, fps = 100, 15
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
