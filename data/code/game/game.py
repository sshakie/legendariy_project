import pygame

from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite
from data.code.game.cell import Cell
from data.code.game.logic import Logic


class Game:
    def __init__(self, screen, attempts=5, len_word=5, active=False):
        self.screen = screen
        self.active = active
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.attempts = attempts
        self.len_word = len_word
        self.count_string = 0  # Порядковый номер попытки
        self.input_word = str()

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/animated-wallpaper3.png'), 60, 1, 0, 0,
                                        self.all_sprites)
        self.line = pygame.image.load('data/textures/ui.png').subsurface((0, 156, 601, 93))
        self.exit_button = Button(8, 6, 134, 39, 'выйти', 0, type=7)

        # Интерфейс выигрыша

        self.win_display = load_image('data/textures/wallpapers/win-screen.png')
        self.lose_display = load_image('data/textures/wallpapers/gameover-screen.png')

        self.reset_button = None
        self.exit_button_2 = None

        self.win_lose_flg = None

        # Текст
        self.text_font = 'data/myy.ttf'
        self.font = pygame.font.Font(self.text_font, 50)
        self.attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))

        # Настройка
        #if self.len_word == 5:
        x_0 = 75 # Начальная позиция по х
        y_0 = 100 # Начальная позиция по у
        width = 100 # Ширина
        height = 63 # Высота
        wight_between_cell = 92 # Расстояние от левого края одного квадрата, до левого края другого
        height_between_cell = 70 # Расстояние от верхнего края одного квадрата, до верхнего края другого

        if self.len_word == 6: # TODO Расставить правильно значения
            x_0 = 75  # Начальная позиция по х
            y_0 = 100  # Начальная позиция по у
            width = 95  # Ширина
            height = 63  # Высота
            wight_between_cell = 92  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 70  # Расстояние от верхнего края одного квадрата, до верхнего края другого
        elif self.len_word == 7: # TODO Расставить правильно значения
            x_0 = 75  # Начальная позиция по х
            y_0 = 100  # Начальная позиция по у
            width = 95  # Ширина
            height = 63  # Высота
            wight_between_cell = 92  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 70  # Расстояние от верхнего края одного квадрата, до верхнего края другого
        elif self.len_word == 8: # TODO Расставить правильно значения
            x_0 = 75  # Начальная позиция по х
            y_0 = 100  # Начальная позиция по у
            width = 95  # Ширина
            height = 63  # Высота
            wight_between_cell = 92  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 70  # Расстояние от верхнего края одного квадрата, до верхнего края другого
        self.guessing = [
            {x: Cell(x_0 + x * wight_between_cell, y_0 + y * height_between_cell, width, height, self.text_font, 50, text_color=(0, 0, 0)) for x in range(self.len_word)}
            for y in range(self.attempts)]


        self.transparency_red_rect = 0

        self.border_radius = 5
        self.red_rect = pygame.Rect(self.guessing[0][0].x, self.guessing[0][0].y,
                                    (self.guessing[0][0].width * self.len_word - 3 * (self.len_word - 1)),
                                    self.guessing[0][0].height)

        self.keyboard = []
        self.logic = Logic(f'data/dictionary/words-length-{self.len_word}.txt')

        # Создание клавиатуры на экране
        for i, letter in enumerate('йцукенгшщзхъ'):
            x_0, y_0, l = 33, 645, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, letter, 30, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)
        for i, letter in enumerate('фывапролджэ'):
            x_0, y_0, l = 55, 695, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, letter, 30, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)
        for i, letter in enumerate('ячсмитьбю'):
            x_0, y_0, l = 100, 745, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, letter, 30, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)

    def render(self):  # Функция для рендера интерфейса
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        self.screen.blit(self.attempt_label, (289, 52))
        self.screen.blit(*self.exit_button.get_rect_coord())
        self.screen.blit(self.line, (0, 543))

        self.clock.tick(self.fps)

        for y in range(self.attempts):
            self.guessing[y][0].round_corners(5, 'topleft', 'bottomleft')
            self.guessing[y][self.len_word - 1].round_corners(5, 'topright', 'bottomright')

        for i in range(len(self.guessing)):
            for q in self.guessing[i].keys():
                self.screen.blit(*self.guessing[i][q].get_rect_coord())
        for i in self.keyboard:
            self.screen.blit(*i.get_rect_coord())

        if self.win_lose_flg is not None:
            if self.win_lose_flg:  # Выигрыш
                self.screen.blit(self.win_display, (0, 0))
            elif self.win_lose_flg is False:
                self.screen.blit(self.lose_display, (0, 0))
            self.screen.blit(*self.reset_button.get_rect_coord())
            self.screen.blit(*self.exit_button_2.get_rect_coord())
        else:
            red_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            red_surface.fill((0, 0, 0, 0))
            pygame.draw.rect(red_surface, (self.transparency_red_rect, 0, 0), self.red_rect,
                             border_radius=self.border_radius, width=5)
            self.screen.blit(red_surface, (0, 0))
            self.transparency_red_rect -= 3

            if self.transparency_red_rect < 0:
                self.transparency_red_rect = 0

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            self.exit_button.selecting()
            if self.win_lose_flg is not None:
                self.reset_button.selecting()
                self.exit_button_2.selecting()

    def check_clicked(self, event):  # Функция проверки нажатия на кнопку эмулированной клавиатуры
        for i in self.keyboard:
            if i.is_clicked(event):
                return i
        return False

    def on_click(self, event):  # Функция нажатия кнопки
        if self.active:
            if self.exit_button.is_clicked(event):
                return self.exit_button
            if self.win_lose_flg is not None:
                if self.reset_button.is_clicked(event):
                    return self.reset_button
                if self.exit_button_2.is_clicked(event):
                    return self.exit_button_2

        button = self.check_clicked(event)
        if button:
            if isinstance(button, Button):
                btn_text = button.get_text()
                if btn_text == 'backspace':
                    self.input_word = self.input_word[:-1]
                elif btn_text == 'enter':
                    self.return_press()
                else:
                    if len(self.input_word) < self.len_word:
                        self.input_word += btn_text

        # Обработка нажатий с клавиатуры
        if self.count_string < self.attempts:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_word = self.input_word[:-1]
                    self.guessing[self.count_string][len(self.input_word)].set_letter('', -1)
                    print(self.input_word)
                elif event.key == pygame.K_RETURN:
                    self.return_press()
                elif event.unicode in 'абвгдежзийклмнопрстуфхцчшщъыьэюя':
                    self.input_word += event.unicode

            if len(self.input_word) > self.len_word:
                self.input_word = self.input_word[0:self.len_word]

            self.input_word = self.input_word.lower()
            for i, letter in enumerate(self.input_word):
                self.guessing[self.count_string][i].set_letter(letter, -1)

    def get_key(self, letter):
        for key in self.keyboard:
            if key.get_text() == letter:
                return key

    def return_press(self):
        if len(self.input_word) == self.len_word:
            data = self.logic.check_input_word(self.input_word)
            print(data)
            if not data:  # Слова нет в словаре
                self.transparency_red_rect = 200
                return
            else:
                for i, v in enumerate(data):
                    if v is False:
                        self.guessing[self.count_string][i].set_letter(self.input_word[i], 0)  #
                        self.get_key(self.input_word[i]).set_image((44, 709, 43, 43))
                    elif v == 'неверное положение':
                        self.guessing[self.count_string][i].set_letter(self.input_word[i], 2)  #
                        self.get_key(self.input_word[i]).set_image((220, 709, 43, 43))
                    elif v is True:
                        self.guessing[self.count_string][i].set_letter(self.input_word[i], 1)  # (132, 709, 43, 43)
                        self.get_key(self.input_word[i]).set_image((132, 709, 43, 43))
            self.count_string += 1
            self.check_win()

            self.input_word = ''
            self.red_rect.y += self.red_rect.height + 7 # TODO Исправить перенос рамки в соответствии с

    def check_win(self):  # TODO Придумать адекватное название метода
        if self.count_string < self.attempts:
            if self.input_word == self.logic.get_right_word().lower():
                self.win_lose_flg = True
                self.reset_button = Button(154, 354, 309, 91, 'заново', 0, type=10)
                self.exit_button_2 = Button(154, 466, 308, 91, 'выйти', 0, type=11)
        else:
            self.win_lose_flg = False
            self.reset_button = Button(154, 354, 309, 91, 'заново', 0, type=8)
            self.exit_button_2 = Button(154, 466, 308, 91, 'выйти', 0, type=9)
