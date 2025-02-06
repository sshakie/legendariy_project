import pygame, random
from data.code.Button import load_image


class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, font, font_size):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = None
        self.font = pygame.font.Font(font, font_size)

        self.corrected_width = width - 20
        self.corrected_height = height - 20
        self.letter = ''
        self.text = None

        self.screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen.fill((0, 0, 0))
        self.rect = self.screen.get_rect(topleft=(x, y))
        pygame.draw.rect(self.screen, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui.png').subsurface((3, 254, 8, 8))
        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))
        self.screen.blit(self.image, (10, 10))

    def round_corners(self, radius, *corners):  # Функция, которая скругляет определённые края
        # Определяем радиусы для каждого угла
        border_top_left = radius if "topleft" in corners else 0
        border_top_right = radius if "topright" in corners else 0
        border_bottom_left = radius if "bottomleft" in corners else 0
        border_bottom_right = radius if "bottomright" in corners else 0

        rounded_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(rounded_surface, (255, 255, 255), (0, 0, self.width, self.height),
                         border_top_left_radius=border_top_left,
                         border_top_right_radius=border_top_right,
                         border_bottom_left_radius=border_bottom_left,
                         border_bottom_right_radius=border_bottom_right)
        self.screen.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def set_letter(self, letter, type, text_offset=(0, 0)):
        self.letter = letter
        self.type = type

        right = [(469, 250, 75, 63), (545, 250, 75, 63), (621, 250, 75, 63)]
        wrong_position = [(0, 250, 90, 63), (91, 250, 91, 63), (183, 250, 89, 63)]
        wrong = [(273, 250, 64, 63), (338, 250, 65, 63), (404, 250, 64, 63)]

        self.screen.fill((0, 0, 0))

        if self.type == -1:
            pass
        elif self.type == 1:  # Правильная буква
            self.image = load_image('data/textures/ui.png').subsurface(random.choice(right))
        elif self.type == 2:  # Неправильная позиция
            self.image = load_image('data/textures/ui.png').subsurface(
                random.choice(wrong_position))
        elif self.type == -2:  # Буква не открыта
            self.image = load_image('data/textures/ui.png').subsurface((3, 254, 8, 8))
        else:  # Нет буквы
            self.image = load_image('data/textures/ui.png').subsurface(random.choice(wrong))

        self.image = pygame.transform.scale(self.image, (self.corrected_width, self.corrected_height))
        self.screen.blit(self.image, (10, 10))
        if self.letter:
            self.text = self.font.render(self.letter, True, (0, 0, 0))
            text_x = self.width // 2 - self.text.get_width() // 2 + text_offset[0]
            text_y = self.height // 2 - self.text.get_height() // 2 + text_offset[1]
            self.screen.blit(self.text, (text_x, text_y))

    def get_rect_coord(self):  # Функция, возвращающая координаты хитбокса
        return self.screen, self.rect.topleft
