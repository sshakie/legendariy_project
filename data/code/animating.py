import pygame


class AnimatedSprite(pygame.sprite.Sprite):  # Класс для анимированных спрайтов
    def __init__(self, image, columns, rows, x, y, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.current = 0
        self.cut_sheet(image, columns, rows)
        self.image = self.frames[self.current]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, image, columns, rows):  # Функция для нарезки изображения
        self.rect = pygame.Rect(0, 0, image.get_width() // columns, image.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(image.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):  # Функция обновления кадров
        self.current = (self.current + 1) % len(self.frames)
        self.image = self.frames[self.current]
