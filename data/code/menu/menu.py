import pygame
from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite


class Menu:
    def __init__(self, screen, money, active=False):
        self.active = active
        self.screen = screen
        self.text_font = None
        self.font = pygame.font.Font(self.text_font, 30)
        self.clock = pygame.time.Clock()

        self.wallpaper_bought = False
        self.details_bought = False
        self.buttons_bought = False
        self.font_bought = False
        self.money = money
        self.fps = 56

        # Интерфейс (основное)
        self.all_sprites = pygame.sprite.Group()  # для анимированного фона
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/gray/animated-wallpaper1.png'), 56, 1, 0,
                                        0,
                                        self.all_sprites)
        self.title = pygame.image.load('data/textures/ui.png').subsurface((0, 0, 298, 108))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((594, 0, 33, 30))

        # Интерфейс (кнопки)
        self.play_button = Button(101, 380, 404, 118, 'играть', 0, type=1)
        self.shop_button = Button(101, 506, 403, 94, 'ларек', 0, type=2)
        self.exit_button = Button(101, 623, 403, 97, 'выход', 0, type=3)

    def render(self):  # Функция для отображения интерфейса
        if self.active:
            money_label = self.font.render(str(self.money), True, (100, 0, 0))
            self.all_sprites.draw(self.screen)  # анимированный фон
            self.all_sprites.update()
            self.screen.blit(self.title, (143, 76))
            self.screen.blit(self.coin, (551, 17))
            self.screen.blit(money_label, (545 - money_label.get_width(), 24))

            self.screen.blit(*self.play_button.get_rect_coord())
            self.screen.blit(*self.shop_button.get_rect_coord())
            self.screen.blit(*self.exit_button.get_rect_coord())
            if self.buttons_bought:
                buttons_custom = load_image('data/textures/wallpapers/colored-elements/menu-buttons.png')
                self.screen.blit(buttons_custom, (0, 0))

            self.clock.tick(self.fps)

    def on_click(self, event):  # Функция нажатия кнопки
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                if button.is_clicked(event):
                    return button
            return False

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            for button in [self.play_button, self.shop_button, self.exit_button]:
                if button.selecting():
                    pygame.mixer.Sound('data/sounds/select_2.wav').play()

    def bought_element(self):
        if self.font_bought:
            self.font = pygame.font.Font(self.text_font, 30)
            'data/myy-font.ttf'

        if self.wallpaper_bought:
            self.all_sprites = pygame.sprite.Group()
            AnimatedSprite(load_image('data/textures/wallpapers/colored-elements/animated-wallpaper1-wallpaper.png'),
                           56, 1, 0, 0, self.all_sprites)
        elif self.details_bought:
            self.all_sprites = pygame.sprite.Group()
            AnimatedSprite(load_image('data/textures/wallpapers/colored-elements/animated-wallpaper1-details.png'), 56,
                           1, 0, 0, self.all_sprites)

