import pygame
from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite


class Shop:
    def __init__(self, screen, money, active=False):
        self.screen = screen
        self.active = active
        self.money = money
        self.text_font = 'data/myy.ttf'
        self.font = pygame.font.Font(self.text_font, 30)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/animated-wallpaper2.png'), 60, 1, 0, 0,
                                        self.all_sprites)
        self.no_problems = pygame.image.load('data/textures/ui.png').subsurface((697, 0, 600, 800))
        self.coin = pygame.image.load('data/textures/ui.png').subsurface((594, 0, 33, 30))
        self.separator1 = pygame.image.load('data/textures/ui.png').subsurface((0, 115, 600, 40))
        self.separator2 = pygame.image.load('data/textures/ui.png').subsurface((0, 115, 600, 40))
        self.upgrade_text = pygame.image.load('data/textures/ui.png').subsurface((299, 0, 294, 57))
        self.customization_text = pygame.image.load('data/textures/ui.png').subsurface((299, 58, 335, 56))
        self.money_label = self.font.render(str(self.money), True, (100, 0, 0))

        # Кнопки
        self.mistake_upgrade = Button(29, 197, 134, 75, 'право на ошибку', 15, type=4)
        self.letter_upgrade = Button(189, 196, 134, 75, 'раскрыть букву', 15, type=4)
        self.game_upgrade = Button(29, 277, 134, 75, 'игра-капча', 15, type=4)
        self.button_custom = Button(111, 427, 134, 75, 'кнопки', 30, type=4)
        self.detail_custom = Button(271, 427, 134, 75, 'детали', 30, type=4)
        self.letter_custom = Button(431, 427, 134, 75, 'буквы', 30, type=4)
        self.background_custom = Button(472, 512, 86, 59, 'фон', 30, type=5)
        self.exit_button = Button(46, 657, 509, 75, 'назад', 0, type=6)

        # Звуки
        self.sfx_select = pygame.mixer.Sound('data/sounds/select.wav')
        self.sfx_select2 = pygame.mixer.Sound('data/sounds/select_2.wav')

    def render(self):  # Функция для рендера интерфейса
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.screen.blit(self.no_problems, (0, 0))
        self.screen.blit(self.coin, (551, 17))
        self.screen.blit(self.money_label, (545 - self.money_label.get_width(), 24))
        self.screen.blit(self.separator1, (0, 160))
        self.screen.blit(self.separator2, (0, 390))
        self.screen.blit(self.upgrade_text, (143, 119))
        self.screen.blit(self.customization_text, (125, 360))
        self.screen.blit(*self.mistake_upgrade.get_rect_coord())
        self.screen.blit(*self.letter_upgrade.get_rect_coord())
        self.screen.blit(*self.game_upgrade.get_rect_coord())
        self.screen.blit(*self.button_custom.get_rect_coord())
        self.screen.blit(*self.detail_custom.get_rect_coord())
        self.screen.blit(*self.letter_custom.get_rect_coord())
        self.screen.blit(*self.background_custom.get_rect_coord())
        self.screen.blit(*self.exit_button.get_rect_coord())
        self.clock.tick(self.fps)

    def on_click(self, event):  # Функция нажатия кнопки
        if self.active:
            for button in [self.mistake_upgrade, self.letter_upgrade, self.game_upgrade, self.button_custom,
                           self.detail_custom, self.letter_custom, self.exit_button]:
                if button.is_clicked(event):
                    return button
        return False

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            for button in [self.mistake_upgrade, self.letter_upgrade, self.game_upgrade,
                           self.button_custom, self.detail_custom, self.letter_custom,
                           self.background_custom, self.exit_button]:
                if button.selecting():
                    if button == self.exit_button:
                        self.sfx_select2.play()
                    else:
                        self.sfx_select.play()

    def update(self, money):  # Подгрузка данных из main для обновления
        self.money = money

        self.money_label = self.font.render(str(self.money), True, (100, 0, 0))