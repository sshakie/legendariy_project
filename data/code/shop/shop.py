import pygame
from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite


class Shop:
    def __init__(self, screen, money, mistake_goods, letter_goods, active=False):
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
        self.mistake_goods = mistake_goods
        self.letter_goods = letter_goods
        self.fps = 60

        # Для игры-капчи
        self.playing = False
        self.captcha_image = ''
        self.captcha_word = ''
        self.writing = ''

        # Интерфейс (основное)
        self.all_sprites = pygame.sprite.Group()  # для анимированного фона
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/gray/animated-wallpaper2.png'), 60, 1, 0,
                                        0,
                                        self.all_sprites)
        self.sublayer = pygame.image.load('data/textures/ui.png').subsurface((697, 0, 600, 800))
        self.separator = pygame.image.load('data/textures/ui.png').subsurface((0, 115, 600, 40))
        self.upgrade_text = pygame.image.load('data/textures/ui.png').subsurface((299, 0, 294, 57))
        self.customization_text = pygame.image.load('data/textures/ui.png').subsurface((299, 58, 335, 56))

        self.coin = pygame.image.load('data/textures/ui.png').subsurface((594, 0, 33, 30))
        self.prices = pygame.image.load('data/textures/screens/prices.png')

        # Интерфейс (кнопки)
        self.exit_button = Button(46, 657, 509, 75, 'назад', 0, type=6)

        self.mistake_upgrade = Button(29, 197, 134, 75, ['право на ', 'ошибку'], 22, font=self.text_font, type=4)
        self.letter_upgrade = Button(189, 196, 134, 75, ['раскрыть ', 'букву'], 22, font=self.text_font, type=4)
        self.game_upgrade = Button(29, 277, 134, 75, ['игра-', 'капча'], 26, font=self.text_font, type=4, offset=(-10, 0))
        self.font_custom = Button(111, 427, 134, 75, 'шрифт', 30, font=self.text_font, type=4)
        self.button_custom = Button(271, 427, 134, 75, 'кнопки', 30, font=self.text_font, type=4)
        self.detail_custom = Button(431, 427, 134, 75, 'детали', 27, font=self.text_font, type=4)
        self.background_custom = Button(472, 512, 86, 59, 'фон', 30, font=self.text_font, type=5, offset=(0, -10))

    def render(self):  # Функция для отображения интерфейса
        if self.active:
            money_label = self.font.render(str(self.money), True, (100, 0, 0))
            mistake_label = self.font.render(str(self.mistake_goods), True, (100, 0, 0))
            letter_label = self.font.render(str(self.letter_goods), True, (100, 0, 0))

            self.all_sprites.draw(self.screen)  # анимированный фон
            self.all_sprites.update()
            self.screen.blit(self.sublayer, (0, 0))

            self.screen.blit(self.upgrade_text, (143, 119))
            self.screen.blit(self.separator, (0, 160))
            self.screen.blit(self.customization_text, (125, 360))
            self.screen.blit(self.separator, (0, 390))

            self.screen.blit(*self.exit_button.get_rect_coord())
            self.screen.blit(*self.mistake_upgrade.get_rect_coord())
            self.screen.blit(*self.letter_upgrade.get_rect_coord())
            self.screen.blit(*self.game_upgrade.get_rect_coord())
            self.screen.blit(*self.button_custom.get_rect_coord())
            self.screen.blit(*self.detail_custom.get_rect_coord())
            self.screen.blit(*self.font_custom.get_rect_coord())
            self.screen.blit(*self.background_custom.get_rect_coord())
            if self.buttons_bought:
                buttons_custom = load_image('data/textures/wallpapers/colored-elements/shop-buttons.png')
                self.screen.blit(buttons_custom, (0, 0))

            self.screen.blit(self.coin, (551, 17))
            self.screen.blit(self.prices, (0, 0))
            self.screen.blit(money_label, (545 - money_label.get_width(), 24))
            self.screen.blit(mistake_label, (44, 245))
            self.screen.blit(letter_label, (204, 245))

            # Отображение игры-капчи
            if self.playing:
                self.screen.blit(load_image('data/textures/screens/captcha-screen.png'), (0, 0))
                self.screen.blit(self.captcha_image, (358, 208))
                font = pygame.font.Font('data/myy-font.ttf', 20)
                self.screen.blit((font.render(self.writing, True, (255, 255, 255))), (364, 326))

            self.clock.tick(self.fps)

    def on_click(self, event):  # Функция нажатия кнопки
        if self.active:
            for button in [self.mistake_upgrade, self.letter_upgrade, self.game_upgrade, self.button_custom,
                           self.detail_custom, self.font_custom, self.background_custom, self.exit_button]:
                if button.is_clicked(event):
                    return button
        return False

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            for button in [self.mistake_upgrade, self.letter_upgrade, self.game_upgrade,
                           self.button_custom, self.detail_custom, self.font_custom,
                           self.background_custom, self.exit_button]:
                if button.selecting():
                    if button == self.exit_button:
                        pygame.mixer.Sound('data/sounds/select_2.wav').play()
                    else:
                        pygame.mixer.Sound('data/sounds/select.wav').play()

    def key_pressing(self, event):
        if event.type == pygame.KEYDOWN and self.playing:
            if event.key == pygame.K_BACKSPACE:
                self.writing = self.writing[:-1]
                pygame.mixer.Sound('data/sounds/game/backspace.wav').play()
            elif event.key == pygame.K_RETURN:
                self.playing = False
                if self.writing == self.captcha_word:
                    pygame.mixer.Sound('data/sounds/shop/win.wav').play()
                    return True
                pygame.mixer.Sound('data/sounds/shop/lose.wav').play()
                return False
            elif event.unicode in 'абвгдежзийклмнопрстуфхцчшщъыьэюя ':
                self.writing += event.unicode
                pygame.mixer.Sound('data/sounds/game/press.wav').play()
            return None

    def bought_element(self):
        if self.wallpaper_bought:
            AnimatedSprite(load_image('data/textures/wallpapers/colored-elements/animated-wallpaper2-wallpaper.png'),
                           60, 1, 0, 0, self.all_sprites)
        if self.details_bought:
            AnimatedSprite(load_image('data/textures/wallpapers/colored-elements/animated-wallpaper2-details.png'), 60,
                           1, 0, 0, self.all_sprites)
        if self.font_bought:
            self.font = pygame.font.Font(self.text_font, 30)
            self.mistake_upgrade = Button(29, 197, 134, 75, ['право на ', 'ошибку'], 22, font=self.text_font, type=4)
            self.letter_upgrade = Button(189, 196, 134, 75, ['раскрыть ', 'букву'], 22, font=self.text_font, type=4)
            self.game_upgrade = Button(29, 277, 134, 75, ['игра-', 'капча'], 26, font=self.text_font, type=4,
                                       offset=(-10, 0))
            self.font_custom = Button(111, 427, 134, 75, 'шрифт', 30, font=self.text_font, type=4)
            self.button_custom = Button(271, 427, 134, 75, 'кнопки', 30, font=self.text_font, type=4)
            self.detail_custom = Button(431, 427, 134, 75, 'детали', 27, font=self.text_font, type=4)
            self.background_custom = Button(472, 512, 86, 59, 'фон', 30, font=self.text_font, type=5, offset=(0, -10))