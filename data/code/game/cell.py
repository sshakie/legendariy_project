import pygame
from data.code.Button import load_image


class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, font, font_size, text_color):
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

        self.font = pygame.font.Font(font, self.font_size)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill((0, 0, 0))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui.png').subsurface((9, 321, 12, 12))

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
            self.image = load_image('data/textures/ui.png').subsurface((469, 250, 75, 63))  # Правильная буква
        elif self.type == 2:
            self.image = load_image('data/textures/ui.png').subsurface((0, 250, 90, 63))  # Неправильная позиция
        else:
            self.image = load_image('data/textures/ui.png').subsurface((273, 250, 64, 63))  # Неправильная буква

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
