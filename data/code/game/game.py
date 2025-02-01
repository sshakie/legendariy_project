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
        self.count_string = 0
        self.input_word = str()

        # Интерфейс
        self.all_sprites = pygame.sprite.Group()
        self.wallpaper = AnimatedSprite(load_image('data/textures/wallpapers/animated-wallpaper3.png'), 60, 1, 0, 0,
                                        self.all_sprites)
        self.line = pygame.image.load('data/textures/ui.png').subsurface((0, 156, 601, 93))
        self.exit_button = Button(8, 6, 134, 39, 'выйти', 0, type=7)

        # Текст
        self.text_font = None
        self.font = pygame.font.Font(self.text_font, 30)
        self.attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (0, 0, 0))
        self.font = pygame.font.Font(None, 50)

        # Настройка
        self.guessing = [{x: Cell(x, y, 5, 15, (50, 50, 50)) for x in range(self.len_word)} for y in
                         range(self.attempts)]  # TODO Сделать динамически изменяемый размер шрифт и цвет
        self.keyboard = []  # TODO Сделать клавиатуру
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

        for i in range(len(self.guessing)):
            for q in self.guessing[i].keys():
                self.screen.blit(*self.guessing[i][q].get_rect_coord())
        for i in self.keyboard:
            self.screen.blit(*i.get_rect_coord())

    def selecting_button(self):  # Функция для выделения кнопки
        if self.active:
            self.exit_button.selecting()

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
                    data = self.logic.check_input_word(self.input_word)
                    if not data:  # Слова нет в словаре
                        return  # TODO хз че делать
                    else:
                        for i, v in sorted(data.items(), key=lambda m: m[0]):
                            if v is None:
                                pass  # TODO Если буквы нет в искомом слове
                            elif v == 'неверное положение':
                                pass  # TODO Если у буквы не верное положение
                            elif isinstance(v, list):
                                pass  # TODO Если у буквы нормальное положение
                else:
                    if len(self.input_word) < self.len_word:
                        self.input_word += btn_text
