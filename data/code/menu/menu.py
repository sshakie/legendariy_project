import pygame
from data.code.Button import Button, load_image
from data.code.class_config import Config
from data.code.animating import AnimatedSprite


class Menu:
    def __init__(self, screen, active=False):
        self.screen = screen
        self.active = active
        self.clock = pygame.time.Clock()
        self.fps = 56

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/animated-wallpaper1.png'), 56, 1, 0, 0, self.all_sprites)
        self.title = pygame.image.load('data/textures/ui.png').subsurface((0, 0, 298, 108))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((594, 0, 33, 30))

        # Загрузка конфига
        self.config = Config()
        self.money = self.config.money
        self.text_font = None
        self.font = pygame.font.Font(self.text_font, 30)
        self.money_label = self.font.render(self.money[6:], True, (100, 0, 0))

        # Кнопки
        self.play_button = Button(101, 380, 404, 118, 'играть', 0, type=1)
        self.shop_button = Button(101, 506, 403, 94, 'ларек', 0, type=2)
        self.exit_button = Button(101, 623, 403, 97, 'выход', 0, type=3)

    def render(self): # Функция для рендера интерфейса
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.screen.blit(self.title, (143, 76))
        self.screen.blit(self.coin, (551, 17))
        self.screen.blit(self.money_label, (535, 24))
        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())
        self.clock.tick(self.fps)

    def on_click(self, event): # Функция нажатия кнопки
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                if button.is_clicked(event):
                    return button
            return False

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                button.selecting()
