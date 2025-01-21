import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text='', text_color=(0, 0, 0), font_size=30, border_radius=10):
        super().__init__()
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.font = pygame.font.Font(None, font_size)

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(), border_radius=self.border_radius)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.surf.get_rect().center)
            self.surf.blit(text_surface, text_rect)

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        else:
            return False
