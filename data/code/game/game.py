import pygame, random
from data.code.Button import Button, load_image
from data.code.animating import AnimatedSprite
from data.code.game.cell import Cell
from data.code.game.logic import Logic


class Game:
    def __init__(self, screen, timer, attempts, len_word=5, mistake_goods=0, letter_goods=0,
                 wallpaper_bought=False, font_bought=False, active=False):
        self.screen = screen
        self.active = active
        self.attempts = attempts
        self.len_word = len_word
        self.text_font = None
        if font_bought:
            self.text_font = 'data/myy-font.ttf'
        self.font = pygame.font.Font(self.text_font, 50)
        self.endscreen_font = pygame.font.Font(self.text_font, 40)
        self.clock = pygame.time.Clock()
        self.time_started_game = pygame.time.get_ticks()

        self.logic = Logic(f'data/dictionary/words-length-{self.len_word}.txt')
        self.right_letters = {i: '' for i in range(self.len_word)}
        self.attempt_numbering = 0  # Порядковый номер попытки
        self.input_word = str()
        self.keyboard = []
        self.k = 1.0
        self.prize = 0
        self.fps = 60

        self.reset_button = None
        self.exit_button_2 = None  # Кнопка выхода на экране выигрыша/проигрыша
        self.display_sure = False
        self.win_lose_flg = None
        self.ended = False  # Нужно чтобы звук не дублировался на экране выигрыша/проигрыша

        self.transparency_red_rect = 0
        self.transparency_green_rect = 0

        self.mistake_goods = bool(mistake_goods)
        self.letter_goods = letter_goods
        self.timer = timer + 5

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()  # для анимированного фона
        if wallpaper_bought:
            AnimatedSprite(load_image('data/textures/wallpapers/colored-elements/animated-wallpaper3-wallpaper.png'),
                           60, 1, 0, 0, self.all_sprites)
        else:
            AnimatedSprite(load_image('data/textures/wallpapers/gray/animated-wallpaper3.png'), 60, 1, 0,
                                        0,
                                        self.all_sprites)

        self.line = pygame.image.load('data/textures/ui.png').subsurface((0, 156, 601, 93))
        self.coin = load_image('data/textures/ui.png').subsurface((628, 0, 18, 21))
        self.exit_button = Button(8, 6, 134, 39, 'выйти', 0, type=7)

        self.win_display = load_image('data/textures/screens/win-screen.png')
        self.lose_display = load_image('data/textures/screens/gameover-screen.png')

        # Настройка расположения клеток для разных длин слов (стандарт - 5 букв)
        x_0 = 50  # Нач. позиция х
        y_0 = 100  # Нач. позиция у
        width, height = 110, 83
        width_between_cell = 100  # Расстояние от левого края одного квадрата, до левого края другого
        height_between_cell = 98  # Расстояние от верхнего края одного квадрата, до верхнего края другого
        self.red_rect = pygame.Rect(x_0, y_0, 509, height)
        if self.len_word == 6:
            x_0 = 45  # Нач. позиция х
            y_0 = 100  # Нач. позиция у
            width, height = 96, 83
            width_between_cell = 86  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 98  # Расстояние от верхнего края одного квадрата, до верхнего края другого
            self.red_rect = pygame.Rect(x_0, y_0, 526, height)
        elif self.len_word == 7:
            x_0 = 41  # Нач. позиция х
            y_0 = 100  # Нач. позиция у
            width, height = 84, 83
            width_between_cell = 74  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 98  # Расстояние от верхнего края одного квадрата, до верхнего края другого
            self.red_rect = pygame.Rect(x_0, y_0, 528, height)
        elif self.len_word == 8:
            x_0 = 40  # Нач. позиция х
            y_0 = 100  # Нач. позиция у
            width, height = 76, 83
            width_between_cell = 66  # Расстояние от левого края одного квадрата, до левого края другого
            height_between_cell = 98  # Расстояние от верхнего края одного квадрата, до верхнего края другого
            self.red_rect = pygame.Rect(x_0, y_0, 538, height)

        # Создание клеток
        self.guessing = [
            {x: Cell(x_0 + x * width_between_cell, y_0 + y * height_between_cell, width, height, self.text_font, 50,
                     ) for x in range(self.len_word)}
            for y in range(self.attempts)]

        # Создание клавиатуры
        for i, let in enumerate('йцукенгшщзхъ'):
            x_0, y_0, l = 33, 645, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, let, 30, font=self.text_font, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)
        for i, let in enumerate('фывапролджэ<'):
            x_0, y_0, l = 33, 695, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, let, 30, font=self.text_font, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)
        for i, let in enumerate('ячсмитьбю'):
            x_0, y_0, l = 100, 745, 45
            kb = Button(x_0 + l * i, y_0, 40, 40, let, 30, font=self.text_font, crop=(0, 709, 44, 44))
            self.keyboard.append(kb)
        self.enter = Button(505, 745, 85, 40, 'enter', 0, font=self.text_font, crop=(308, 709, 85, 43))
        self.keyboard.append(self.enter)

        if int(self.letter_goods):  # Если куплено открытие расположение рандомной клетки, то открываем
            let = random.choice(list(enumerate(self.logic.word)))
            self.guessing[self.attempt_numbering][let[0]].set_letter(let[1], 1)
            self.get_key(let[1]).set_image(random.choice([(132, 709, 43, 43), (176, 709, 43, 43)]))
            self.right_letters[let[0]] = let[1]

    def render(self):  # Функция для отображения интерфейса
        if self.active:
            self.all_sprites.draw(self.screen)  # для анимированного фона
            self.all_sprites.update()
            attempts_label = self.font.render(f'Попыток: {self.attempts - self.attempt_numbering}', True, (0, 0, 0))
            self.screen.blit(attempts_label,
                             (590 - attempts_label.get_width(), 52))
            self.screen.blit(self.line, (0, 543))
            self.screen.blit(*self.exit_button.get_rect_coord())

            # Таймер
            if self.win_lose_flg is None:
                self.noww = max(0, self.timer - ((pygame.time.get_ticks() - self.time_started_game) // 1000))
            self.screen.blit((self.font.render(str(self.noww), True, (0, 0, 0))), (10, 52))

            # Клетки
            for i in range(len(self.guessing)):
                self.guessing[i][0].round_corners(8, 'topleft', 'bottomleft')
                self.guessing[i][self.len_word - 1].round_corners(8, 'topright', 'bottomright')
                for q in self.guessing[i].keys():
                    self.screen.blit(*self.guessing[i][q].get_rect_coord())

            for i in self.keyboard:
                self.screen.blit(*i.get_rect_coord())

            if self.display_sure:  # Окно подтверждения выхода
                self.screen.blit(load_image('data/textures/screens/do-you-sure.png'), (0, 0))

            # Условия для отображения окна выигрыша/проигрыша
            if self.noww == 0:
                self.attempts = self.attempt_numbering
                self.check_win()
            if self.win_lose_flg is not None:
                if self.win_lose_flg:  # Выигрыш
                    prize = round(10 * self.k)
                    self.screen.blit(self.win_display, (0, 0))
                    self.screen.blit((self.endscreen_font.render(str(prize), True, (255, 106, 0))), (380, 320))
                    self.screen.blit(self.coin, (415, 321))
                else:  # Проигрыш
                    self.screen.blit(self.lose_display, (0, 0))
                    self.screen.blit((self.endscreen_font.render(self.logic.word, True, (255, 106, 0))),
                                     (323, 305))
                self.screen.blit(*self.reset_button.get_rect_coord())
                self.screen.blit(*self.exit_button_2.get_rect_coord())
            else:  # Выделение клеток красным, если слово некорректно
                red_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                red_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(red_surface, (self.transparency_red_rect, self.transparency_green_rect, 0),
                                 self.red_rect,
                                 border_radius=5, width=10)
                self.screen.blit(red_surface, (0, 0))
                self.transparency_red_rect = max(0, self.transparency_red_rect - 3)
                self.transparency_green_rect = max(0, self.transparency_green_rect - 3)

            self.clock.tick(self.fps)

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            if not self.display_sure:
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
        if self.active and not self.display_sure:
            if self.exit_button.is_clicked(event):
                return self.exit_button
            if self.win_lose_flg is not None:
                if self.reset_button.is_clicked(event):
                    return self.reset_button
                if self.exit_button_2.is_clicked(event):
                    return self.exit_button_2
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = self.check_clicked(event)
                if button:
                    if isinstance(button, Button):
                        btn_text = button.get_text()
                        if btn_text == '<':
                            self.input_word = self.input_word[:-1]
                            self.guessing[self.attempt_numbering][len(self.input_word)].set_letter('', -1)
                            pygame.mixer.Sound('data/sounds/game/backspace.wav').play()
                        elif btn_text == 'enter':
                            self.return_press()
                            pygame.mixer.Sound('data/sounds/game/enter.wav').play()
                        else:
                            if len(self.input_word) < self.len_word:
                                self.input_word += btn_text
                            pygame.mixer.Sound('data/sounds/game/press.wav').play()
                        if int(self.letter_goods):
                            for i, c in self.guessing[min(self.attempt_numbering, self.attempts - 1)].items():
                                if c.letter == '':
                                    if self.right_letters[i]:
                                        c.set_letter(self.right_letters[i], 1)
                                    else:
                                        c.set_letter('', -2)
                        for i, letter in enumerate(self.input_word):
                            self.guessing[self.attempt_numbering][i].set_letter(letter, -2)


            # Обработка нажатий с клавиатуры
            elif event.type == pygame.KEYDOWN:
                if self.attempt_numbering < self.attempts:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_word = self.input_word[:-1]
                        self.guessing[self.attempt_numbering][len(self.input_word)].set_letter('', -1)
                        pygame.mixer.Sound('data/sounds/game/backspace.wav').play()
                    elif event.key == pygame.K_RETURN:
                        self.return_press()
                        pygame.mixer.Sound('data/sounds/game/enter.wav').play()
                    elif event.unicode in 'абвгдежзийклмнопрстуфхцчшщъыьэюя':
                        if event.unicode.isalpha():
                            self.input_word += event.unicode
                            pygame.mixer.Sound('data/sounds/game/press.wav').play()

                    if len(self.input_word) > self.len_word:
                        self.input_word = self.input_word[0:self.len_word]

                    if int(self.letter_goods):
                        for i, c in self.guessing[min(self.attempt_numbering, self.attempts - 1)].items():
                            if c.letter == '':
                                if self.right_letters[i]:
                                    c.set_letter(self.right_letters[i], 1)
                                else:
                                    c.set_letter('', -2)
                    for i, letter in enumerate(self.input_word):
                        self.guessing[self.attempt_numbering][i].set_letter(letter, -2)

    def accept_exiting(self, event):  # Функция для подтверждения/отмены выхода
        if self.display_sure and (
                event.pos[0] in list(range(192, 192 + 98)) and event.pos[1] in list(range(397, 397 + 37))):
            return 'yes'
        elif self.display_sure and (
                event.pos[0] in list(range(310, 310 + 98)) and event.pos[1] in list(range(397, 397 + 37))):
            return 'no'
        return None

    def get_key(self, letter):  # Функция для получения нажатой клавиши
        for key in self.keyboard:
            if key.get_text() == letter:
                return key

    def return_press(self):
        right = [(132, 709, 43, 43), (176, 709, 43, 43)]
        wrong_position = [(220, 709, 43, 43), (264, 709, 43, 43)]
        wrong = [(44, 709, 43, 43), (88, 709, 43, 43)]
        if len(self.input_word) == self.len_word:
            data = self.logic.check_input_word(self.input_word)
            if not data:  # Слова нет в словаре
                self.transparency_red_rect = 200
                return
            else:
                w = 0
                w_p = 0
                r = 0
                if self.mistake_goods:
                    for i, v in enumerate(data):
                        if v is False:
                            self.get_key(self.input_word[i]).set_image(random.choice(wrong))
                            self.right_letters[i] = v
                            w += 1
                        elif v == 'неверное положение':
                            self.get_key(self.input_word[i]).set_image(random.choice(wrong_position))
                            w_p += 1
                        elif v is True:
                            self.get_key(self.input_word[i]).set_image(random.choice(right))
                            r += 1
                        self.guessing[self.attempt_numbering][i].set_letter('', -2)  #
                else:
                    for i, v in enumerate(data):
                        if v is False:
                            self.guessing[self.attempt_numbering][i].set_letter(self.input_word[i], 0)  #
                            self.get_key(self.input_word[i]).set_image(random.choice(wrong))
                            self.right_letters[i] = v
                            w += 1
                        elif v == 'неверное положение':
                            self.guessing[self.attempt_numbering][i].set_letter(self.input_word[i], 2)  #
                            self.get_key(self.input_word[i]).set_image(random.choice(wrong_position))
                            w_p += 1
                        elif v is True:
                            self.guessing[self.attempt_numbering][i].set_letter(self.input_word[i],
                                                                                1)  # (132, 709, 43, 43)
                            self.get_key(self.input_word[i]).set_image(random.choice(right))
                            r += 1
                if r != 0:
                    pygame.mixer.Sound('data/sounds/game/right-letter.wav').play()
                elif w_p != 0:
                    pygame.mixer.Sound('data/sounds/game/wrong_pos.wav').play()
                elif w != 0:
                    pygame.mixer.Sound('data/sounds/game/all-wrong.wav').play()
            if self.mistake_goods:
                self.mistake_goods = False

                self.check_win()
                self.input_word = ''
                self.transparency_green_rect = 200
            else:
                self.attempt_numbering += 1
                self.check_win()
                self.input_word = ''
                self.red_rect.y += 98
            self.letter_goods = 0
        else:
            self.transparency_red_rect = 200

    def check_win(self):  # Функция для проверки выигрыша
        if self.input_word == self.logic.word:
            self.win_lose_flg = True
            self.reset_button = Button(154, 354, 309, 91, 'заново2', 0, font=self.text_font, type=10)
            self.exit_button_2 = Button(154, 466, 308, 91, 'выйти3', 0, font=self.text_font, type=11)
            if self.ended is False:
                pygame.mixer.Sound('data/sounds/game/win.wav').play()
            self.ended = True

            # Добавление награды, учитывая множители
            with open('data/config.txt') as config:
                config = config.read()
                a = [bool(int(config.split('\n')[1].split()[-1])), bool(int(config.split('\n')[2].split()[-1])),
                     bool(int(config.split('\n')[3].split()[-1])), bool(int(config.split('\n')[4].split()[-1]))]
                self.k *= (1 + (0.4 * a.count(True)))
            if self.attempt_numbering <= 2:
                self.k *= 1.4
            self.prize = round(15 * self.k)
        elif self.attempt_numbering == self.attempts:
            self.win_lose_flg = False
            self.reset_button = Button(154, 354, 309, 91, 'заново', 0, font=self.text_font, type=8)
            self.exit_button_2 = Button(154, 466, 308, 91, 'выйти2', 0, font=self.text_font, type=9)
            if self.ended is False:
                pygame.mixer.Sound('data/sounds/game/lose.wav').play()
            self.ended = True
