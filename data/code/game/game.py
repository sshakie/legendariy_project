import pygame

from data.code.Button import load_image, KeyboardButton, Button
from data.code.game.logic import Logic


class Game:
    def __init__(self, screen, attempts=5, len_word=5, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper3.png')
        self.attempts = attempts
        self.font = pygame.font.Font(None, 30)
        self.len_word = len_word
        self.guessing = [{x: Cell(75 + x * 92, 100 + y * 70, 95, 63, 50, (50, 50, 50)) for x in range(self.len_word)} for y in range(self.attempts)] # TODO Сделать динамически изменяемый размер шрифт и цвет
        self.count_string = 0  # Порядковый номер попытки
        self.input_word = str()

        self.exit_button = Button(8, 6, 134, 39, 'data/textures/ui.png', 'выйти', 0, crop=(228, 759, 134, 39))
        self.line = pygame.image.load('data/textures/ui.png').subsurface((0, 557, 601, 93))
        self.attempts = 5
        self.font = pygame.font.Font(None, 50)

        # Клавиатура
        self.keyboard = []  # TODO Сделать клавиатуру

        for i, letter in enumerate('йцукенгшщзхъ'):
            x_0 = 33
            y_0 = 645
            r = 45 # Расстояние между кнопками
            kb = Button(x_0 + r * i, y_0, 40, 40, "data/textures/ui.png", letter, 30, crop=(228, 715, 43, 43)) # Картинка по умолчанию
            self.keyboard.append(kb)


        for i, letter in enumerate('фывапролджэ'):
            x_0 = 55
            y_0 = 695
            r = 45 # Расстояние между кнопками
            kb = Button(x_0 + r * i, y_0, 40, 40, "data/textures/ui.png", letter, 30, crop=(228, 715, 43, 43)) # Картинка по умолчанию
            self.keyboard.append(kb)

        for i, letter in enumerate('ячсмитьбю'):
            x_0 = 100
            y_0 = 745
            r = 45 # Расстояние между кнопками
            kb = Button(x_0 + r * i, y_0, 40, 40, "data/textures/ui.png", letter, 30, crop=(228, 715, 43, 43)) # Картинка по умолчанию
            self.keyboard.append(kb)


        if len_word == 5:
            self.logic = Logic('data/dictionary/words-length-5.txt')
        elif len_word == 6:
            self.logic = Logic('data/dictionary/words-length-6.txt')
        elif len_word == 7:
            self.logic = Logic('data/dictionary/words-length-7.txt')
        elif len_word == 8:
            self.logic = Logic('data/dictionary/words-length-8.txt')

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))
        self.screen.blit(attempt_label, (289, 52))
        self.screen.blit(*self.exit_button.get_rect_coord())
        self.screen.blit(self.line, (0, 543))
        for i in range(len(self.guessing)):
            for q in self.guessing[i].keys():
                self.screen.blit(*self.guessing[i][q].get_rect_coord())

        for i in self.keyboard:
            self.screen.blit(*i.get_rect_coord())

    def reset(self):
        self.attempts = 5 # TODO Так быть не должно

    def check_clicked(self, event):
        for i in self.keyboard:
            if i.is_clicked(event):
                return i
        return False

    def on_click(self, event):
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

        for i, letter in enumerate(self.input_word):
            self.guessing[self.count_string][i].set_letter(letter, -1)

    def return_press(self):
        data = self.logic.check_input_word(self.input_word)
        if not data:  # Слова нет в словаре
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
        self.input_word = ''

class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, font_size, text_color):
        super().__init__()
        self.x = x
        self.y = y
        self.type = None
        self.letter = None
        self.font_size = font_size
        self.text_color = text_color

        self.text = None

        self.width = width
        self.height = height

        self.corrected_width = width - 10
        self.corrected_height = height - 10

        self.font = pygame.font.Font(None, self.font_size)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill((0, 0, 0))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui.png').subsurface((236, 724, 22, 22))  # TODO картинка когда клетка закрыта

        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))

        self.surf.blit(self.image, (5, 5))

    def set_letter(self, letter, type, text_offset=(0, 0)):
        self.letter = letter
        self.type = type

        # Очистка поверхности
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))

        # Выбор изображения в зависимости от типа
        if self.type == -1:
            pass
        elif self.type == 1:
            self.image = load_image('data/textures/ui.png').subsurface((0, 715, 75, 63))  # Правильная буква
        elif self.type == 2:
            self.image = load_image('data/textures/ui.png').subsurface((0, 651, 90, 63))  # Неправильная позиция
        else:
            self.image = load_image('data/textures/ui.png').subsurface((273, 651, 64, 63))  # Неправильная буква

        # Масштабируем изображение и накладываем на поверхность
        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))
        self.surf.blit(self.image, (5, 5))

        # Отрисовка текста
        if self.letter:
            self.text = self.font.render(self.letter, True, self.text_color)
            text_x = self.width // 2 - self.text.get_width() // 2 + text_offset[0]
            text_y = self.height // 2 - self.text.get_height() // 2 + text_offset[1]
            self.surf.blit(self.text, (text_x, text_y))

    def get_rect_coord(self):
        return self.surf, self.rect.topleft
