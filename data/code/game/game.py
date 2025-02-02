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

        self.exit_button_2 = Button(8, 6, 134, 39, 'выйти', 0, type=7)

        self.win_lose_flg = None

        # Текст
        self.text_font = 'data/myy.ttf'
        self.font = pygame.font.Font(self.text_font, 50)
        self.attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))

        # Настройка
        self.guessing = [
            {x: Cell(75 + x * 92, 100 + y * 70, 95, 63, self.text_font, 50, text_color=(50, 50, 50)) for x in range(self.len_word)} for
            y in range(self.attempts)]  # TODO Сделать динамически изменяемый размер шрифт и цвет
        # TODO Сделать динамически изменяемый размер шрифт и цвет
        self.keyboard = []  # TODO Сделать клавиатуру
        self.logic = Logic(f'data/dictionary/words-length-{self.len_word}.txt')

        # Звуки
        self.sfx_select2 = pygame.mixer.Sound('data/sounds/select_2.wav')

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

        for i in range(len(self.guessing)):
            for q in self.guessing[i].keys():
                self.screen.blit(*self.guessing[i][q].get_rect_coord())
        for i in self.keyboard:
            self.screen.blit(*i.get_rect_coord())

        if self.win_lose_flg is None:
            return
        elif self.win_lose_flg is True: # Выигрыш
            self.screen.blit(self.win_display, (0, 0))
        elif self.win_lose_flg is False:
            self.screen.blit(self.lose_display, (0, 0))

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            if self.exit_button.selecting():
                self.sfx_select2.play()

    def check_clicked(self, event):  # Функция проверки нажатия на кнопку эмулированной клавиатуры
        for i in self.keyboard:
            if i.is_clicked(event):
                return i
        return False

    def on_click(self, event):  # Функция нажатия кнопки
        if self.active and self.exit_button.is_clicked(event):
            return self.exit_button

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

    def return_press(self):
        data = self.logic.check_input_word(self.input_word)
        if not data or len(self.input_word) < int(self.len_word):  # Слова нет в словаре
            return  # TODO хз че делать
        else:
            for i, v in sorted(data.items(), key=lambda m: m[0]):
                if v is None:
                    self.guessing[self.count_string][self.input_word.index(i)].set_letter(i, 0)
                elif v == 'неверное положение':
                    self.guessing[self.count_string][self.input_word.index(i)].set_letter(i, 2)
                elif isinstance(v, list):
                    for q in v:
                        self.guessing[self.count_string][q].set_letter(i, 1)
        self.count_string += 1
        self.attempts -= 1
        self.attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))
        self.check_win()
        self.input_word = ''

    def check_win(self): # TODO Придумать адекватное название метода
        if self.count_string < self.attempts:
            if self.input_word == self.logic.get_right_word().lower():
                self.win_lose_flg = True
        else:
            self.win_lose_flg = False
            # Проигрыш
