import pygame

from data.code.Button import load_image


class Game:
    def __init__(self, screen, attempts=5, len_word=5, active=False):
        self.screen = screen
        self.active = active
        self.wallpaper = pygame.image.load('data/textures/wallpaper3 (hd).png')
        self.attempts = attempts
        self.font = pygame.font.Font(None, 30)
        self.len_word = len_word
        self.guessing = [{x: Cell(x, y, size, font_size, text_color) for x in range(self.len_word)} for y in range(self.attempts)]
        self.count_string = 0

        # Клавиатура
        self.keyboard = []

    def render(self):
        self.screen.blit(self.wallpaper, (0, 0))
        attempt_label = self.font.render(f'Попыток: {self.attempts}', True, (255, 255, 255))
        self.screen.blit(attempt_label, (100, 50))
        for i in self.guessing:
            for q in self.guessing[i].keys():
                self.screen.blit(*i[q].get_rect_coord())


    def reset(self):
        self.attempts = 5

    def on_click(self):
        pass


class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int, font_size, text_color):
        super().__init__()
        self.x = x
        self.y = y
        self.type = None
        self.letter = None
        self.font_size = font_size
        self.text_color = text_color

        self.size = size

        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui1.png').subsurface(Кроп)) # TODO картинка когда клетка закрыта

        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.surf.blit(self.image, (0, 0))


    def set_letter(self, letter, type):
        self.letter = letter
        self.type = type

        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(self.size, self.size))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        if self.type == 1:
            self.image = load_image('data/textures/ui1.png').subsurface(Кроп)) # TODO Путь до иконки с правильным ответом
        elif self.type == 2:
            self.image = load_image('data/textures/ui1.png').subsurface(Кроп)) # TODO Путь до иконки "не на своем месте"
        else:
            self.image = load_image('data/textures/ui1.png').subsurface(Кроп)) # TODO путь до иконки "не верно"

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.surf.blit(self.image, (0, 0))

        # Настраиваем шрифт и текст
        self.font = pygame.font.Font(self.letter, None, self.font_size)
        self.text = self.font.render(self.letter, True, self.text_color)
        text_x = self.size // 2 - self.text.get_width() // 2
        text_y = self.size // 2 - self.text.get_height() // 2

        # Рисуем текст
        self.surf.blit(self.text, (text_x, text_y))

    def get_rect_coord(self):
        return self.surf, self.rect.topleft

