import pygame


class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.set_view(left, top, cell_size)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Lines(Board):
    def __init__(self, width, height, clock):
        super().__init__(width, height)
        self.board = [[0] * width for _ in range(height)]
        self.clock = clock
        self.red = False

    def has_path(self, x1, y1, x2, y2):
        if self.board[y2][x2] != 0:
            return []

        visited = [[False] * self.width for _ in range(self.height)]
        queue = [(x1, y1, [])]
        visited[y1][x1] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            cx, cy, path = queue.pop(0)

            if (cx, cy) == (x2, y2):
                return path + [(cx, cy)]

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx]:
                    if self.board[ny][nx] == 0:
                        visited[ny][nx] = True
                        queue.append((nx, ny, path + [(cx, cy)]))

        return []

    def animate_movement(self, path, screen):
        for x, y in path:
            self.board[y][x] = 1
            screen.fill((0, 0, 0))
            self.render(screen)
            pygame.display.flip()
            self.clock.tick(60)
            self.board[y][x] = 0

    def on_click(self, cell):
        x, y = cell
        current = self.board[y][x]

        if current == 0:
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] == 2:
                        path = self.has_path(j, i, x, y)
                        if path:
                            path.pop(0)
                            self.animate_movement(path, pygame.display.get_surface())
                            self.board[i][j] = 0
                            self.board[y][x] = 1
                            self.red = False
                            return
                        else:
                            return
            self.board[y][x] = 1

        elif current == 1 and not self.red:
            self.board[y][x] = 2
            self.red = True

        elif current == 2:
            self.board[y][x] = 1
            self.red = False

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                # Отрисовка сетки
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

                if self.board[y][x] == 1:
                    pygame.draw.circle(screen, (0, 0, 255),
                                       (x * self.cell_size + self.left + self.cell_size // 2,
                                        y * self.cell_size + self.top + self.cell_size // 2),
                                       self.cell_size / 2 - 1)
                elif self.board[y][x] == 2:  # Красный шарик
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (x * self.cell_size + self.left + self.cell_size // 2,
                                        y * self.cell_size + self.top + self.cell_size // 2),
                                       self.cell_size / 2 - 1)


def main():
    pygame.init()
    size = 500, 500

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    board = Lines(10, 10, clock)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                cell = board.get_cell(mouse_pos)
                if cell:
                    board.get_click(mouse_pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
