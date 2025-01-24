import pygame
from data.code.Button import *


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper1 (hd).png')
        self.title = pygame.image.load('data/textures/ui1.png')
        self.play_button = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'Играть', 30, screen)
        self.shop_button = MenuButton(250, 375, 100, 25, 'data/textures/ui1.png', 'Ларёк', 30, screen)
        self.settings_button = MenuButton(250, 450, 100, 25, 'data/textures/ui1.png', 'Настройки', 30, screen)
        self.exit_button = MenuButton(250, 525, 100, 25, 'data/textures/ui1.png', 'Выйти', 30, screen)


class Shop:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper2 (ai-hd).png')
        self.upgrade_title = pygame.image.load('data/textures/ui1.png')
        self.customization_title = pygame.image.load('data/textures/ui1.png')
        self.separator1 = pygame.image.load('data/textures/ui1.png')
        self.separator2 = pygame.image.load('data/textures/ui1.png')
        self.separator3 = pygame.image.load('data/textures/ui1.png')
        # self.hardcore_button = pygame.draw.rect(screen)
        
        self.mistake_upgrade = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', '-1 ошибка', 15, screen)
        self.letter_upgrade = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', '+1 буква', 15, screen)
        self.game_upgrade = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'игра', 15, screen)
        
        self.button_custom = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'кнопки', 15, screen)
        self.detail_custom = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'детали', 15, screen)
        self.letter_custom = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'буквы', 15, screen)
        self.detail_custom = MenuButton(250, 300, 100, 25, 'data/textures/ui1.png', 'фон', 15, screen)
    

class Game:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper3 (hd).png')
        self.attempts = 5
        self.font = pygame.font.Font(None, 30)
        self.attempt_label = pygame.font.render(f'попыток: {self.attempts}')
        self.attempt_label.blit(100,  50)
        self.wallpaper = pygame.image.load('data/textures/ui1.png')
     
    def reset(self):
        self.attempts = 5


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    
    coin = pygame.image.load('data/textures/ui1.png')
    money = 0
    menu_window = Menu(screen, active=True)
    shop_window = Menu(screen)
    game_window = Menu(screen)
    
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
