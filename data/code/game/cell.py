import pygame, random
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

        self.corrected_width = width - 20
        self.corrected_height = height - 20

        self.font = pygame.font.Font(font, self.font_size)
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill((0, 0, 0))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui.png').subsurface((3, 254, 8, 8))

        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))

        self.surf.blit(self.image, (10, 10))

    def round_corners(self, radius, *corners):
        rounded_surface = pygame.Surface(self.surf.get_size(), pygame.SRCALPHA)

        width, height = self.surf.get_size()

        # Определяем радиусы для каждого угла
        border_top_left = radius if "topleft" in corners else 0
        border_top_right = radius if "topright" in corners else 0
        border_bottom_left = radius if "bottomleft" in corners else 0
        border_bottom_right = radius if "bottomright" in corners else 0

        pygame.draw.rect(
            rounded_surface,
            (255, 255, 255, 255),
            (0, 0, width, height),
            border_top_left_radius=border_top_left,
            border_top_right_radius=border_top_right,
            border_bottom_left_radius=border_bottom_left,
            border_bottom_right_radius=border_bottom_right
        )
        self.surf.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def set_letter(self, letter, type, text_offset=(0, 0)):
        self.letter = letter
        self.type = type

        right = [(469, 250, 75, 63), (545, 250, 75, 63), (621, 250, 75, 63)]
        wrong_position = [(0, 250, 90, 63), (91, 250, 91, 63), (183, 250, 89, 63)]
        wrong = [(273, 250, 64, 63), (338, 250, 65, 63), (404, 250, 64, 63)]

        # Очистка поверхности
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))

        # Выбор изображения в зависимости от типа
        if self.type == -1:
            pass
        elif self.type == 1:
            self.image = load_image('data/textures/ui.png').subsurface(random.choice(right))  # Правильная буква
        elif self.type == 2:
            self.image = load_image('data/textures/ui.png').subsurface(random.choice(wrong_position))  # Неправильная позиция
        else:
            self.image = load_image('data/textures/ui.png').subsurface(random.choice(wrong))  # Неправильная буква

        # Масштабируем изображение и накладываем на поверхность
        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))
        self.surf.blit(self.image, (10, 10))

        # Отрисовка текста
        if self.letter:
            self.text = self.font.render(self.letter, True, self.text_color)
            text_x = self.width // 2 - self.text.get_width() // 2 + text_offset[0]
            text_y = self.height // 2 - self.text.get_height() // 2 + text_offset[1]
            self.surf.blit(self.text, (text_x, text_y))

    def get_rect_coord(self):
        return self.surf, self.rect.topleft