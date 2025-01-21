import pygame.sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, text_color, font_size):
        super().__init__()
        self.text = text
        self.text_color = text_color
        self.font_size = font_size

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.font = pygame.font.Font(None, font_size)

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        else:
            return False