import pygame
from data.code.Button import Button

class MenuButton(Button):
    def __init__(self, x, y, width, height, image_path, text='', text_color=(0, 0, 0), font_size=30):
        super().__init__(x, y, width, height, text, text_color, font_size)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)

    def update(self):
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.image.blit(text_surface, text_rect)


