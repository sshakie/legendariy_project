import pygame

from data.code.Button import Button


class KeyboardButton(Button):
    def __init__(self, x, y, width, height, color, text='', text_color=(0, 0, 0), font_size=30, border_radius=10):
        super().__init__(x, y, width, height, text, text_color, font_size)
        self.color = color
        self.border_radius = border_radius

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(), border_radius=self.border_radius)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.surf.get_rect().center)
            self.surf.blit(text_surface, text_rect)
