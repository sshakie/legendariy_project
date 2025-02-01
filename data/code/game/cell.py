import pygame
from data.code.Button import load_image


class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int, font_size, text_color):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.type = None
        self.letter = None
        self.text = None
        self.text_color = text_color
        self.text_font = None
        self.font = pygame.font.Font(self.text_font, font_size)

        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.image = load_image('data/textures/ui.png').subsurface((236, 724, 22, 22))  # TODO картинка когда клетка закрыта
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.surf.blit(self.image, (0, 0))

    def set_letter(self, letter, type):
        self.letter = letter
        self.type = type

        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(self.size, self.size))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        if self.type == 1:
            self.image = load_image('data/textures/ui.png').subsurface((0, 715, 75, 63))  # TODO Путь до иконки с правильным ответом
        elif self.type == 2:
            self.image = load_image('data/textures/ui.png').subsurface( (0, 651, 90, 63))  # TODO Путь до иконки "не на своем месте"
        else:
            self.image = load_image('data/textures/ui.png').subsurface((273, 651, 64, 63))  # TODO путь до иконки "не верно"

            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.surf.blit(self.image, (0, 0))

            # Настраиваем шрифт и текст
            self.text = self.font.render(self.letter, True, self.text_color)
            text_x = self.size // 2 - self.text.get_width() // 2
            text_y = self.size // 2 - self.text.get_height() // 2
            # Рисуем текст
            self.surf.blit(self.text, (text_x, text_y))

    def get_rect_coord(self):
        return self.surf, self.rect.topleft
