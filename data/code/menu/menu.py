import pygame
from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite


class Menu:
    def __init__(self, screen, money, active=False):
        self.screen = screen
        self.active = active
        self.money = money
        self.text_font = 'data/myy.ttf'
        self.font = pygame.font.Font(self.text_font, 30)
        self.clock = pygame.time.Clock()
        self.fps = 56

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/animated-wallpaper1.png'), 56, 1, 0, 0,
                                        self.all_sprites)
        self.title = pygame.image.load('data/textures/ui.png').subsurface((0, 0, 298, 108))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((594, 0, 33, 30))
        self.money_label = self.font.render(str(self.money), True, (100, 0, 0))

        # Кнопки
        self.play_button = Button(101, 380, 404, 118, 'играть', 0, type=1)
        self.shop_button = Button(101, 506, 403, 94, 'ларек', 0, type=2)
        self.exit_button = Button(101, 623, 403, 97, 'выход', 0, type=3)

        # Звуки
        self.sfx_select2 = pygame.mixer.Sound('data/sounds/select_2.wav')

    def render(self):  # Функция для рендера интерфейса
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.screen.blit(self.title, (143, 76))
        self.screen.blit(self.coin, (551, 17))
        self.screen.blit(self.money_label, (545 - self.money_label.get_width(), 24))
        self.screen.blit(*self.play_button.get_rect_coord())
        self.screen.blit(*self.shop_button.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())
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
                    self.sfx_select2.play()

    def update(self, money):  # Подгрузка данных из main для обновления
        self.money = money

        self.money_label = self.font.render(str(self.money), True, (100, 0, 0))