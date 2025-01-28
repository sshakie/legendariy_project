import pygame

def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class KeyboardButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text='', text_color=(0, 0, 0), font_size=30, border_radius=10):
        super().__init__()
        self.line_text = text
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))

        pygame.draw.rect(self.surf, color, (0, 0, width, height), border_radius=self.border_radius)
        self.font = pygame.font.Font(None, self.font_size)
        text_color = self.text_color

        if all(channel < 180 for channel in color):
            text_color = (255, 255, 255)

        self.text = self.font.render(self.line_text, True, text_color)
        text_x = (width - self.text.get_width()) // 2
        text_y = (height - self.text.get_height()) // 2
        self.surf.blit(self.text, (text_x, text_y))

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        return False

    def get_rect_coord(self):
        return self.surf, self.rect.topleft

    def get_text(self):
        return self.line_text


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, text, font_size, text_color=(0, 0, 0), crop: tuple[int, int, int, int]=None, selected_coords=(0, 0)):
        super().__init__()
        self.line_text = text
        self.text_color = text_color
        self.font_size = font_size
        self.selected_coords = selected_coords
        self.width = width
        self.height = height

        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x, y))
        pygame.draw.rect(self.surf, (255, 255, 255, 0), self.rect)

        self.base_image = load_image(image_path).subsurface(crop)

        if crop:
            self.image = self.base_image
            if self.selected_coords != (0, 0):
                self.selected_image = load_image(image_path).subsurface((self.selected_coords[0], self.selected_coords[1], crop[2], crop[3]))

        # Масштабируем изображение до размеров кнопки
        self.image = pygame.transform.scale(self.image, (width, height))
        if self.selected_coords != (0, 0):
            self.selected_image = pygame.transform.scale(self.selected_image, (width, height))

            # Настраиваем шрифт и текст
        self.font = pygame.font.Font(None, font_size)
        self.text = self.font.render(self.line_text, True, self.text_color)
        self.text_x = width // 2 - self.text.get_width() // 2
        self.text_y = (height // 2 - self.text.get_height() // 2) - 10

        # Рисуем изображение и текст на кнопке
        self.surf.blit(self.image, (0, 0))
        self.surf.blit(self.text, (self.text_x, self.text_y))

    def check_cursor_position(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.check_cursor_position()
        return False

    def get_rect_coord(self):
        return self.surf, self.rect.topleft

    def get_text(self):
        return self.line_text

    def selecting(self):
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        if self.check_cursor_position():
            self.image = self.selected_image
        else:
            self.image = self.base_image
        # Рисуем изображение и текст на кнопке
        self.surf.blit(self.image, (0, 0))
        self.surf.blit(self.text, (self.text_x, self.text_y))