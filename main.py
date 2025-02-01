import pygame
from data.code.Button import *
from data.code.game.game import Game
from data.code.menu.menu import Menu
from data.code.shop.shop import Shop

# Для перехода между сценами
ws_width = 1
old_scene = None
new_scene = None
start_transition = False
stop_transition = False
black_screen = pygame.Surface((600, 800))
game_starting = False
timer = 120
alpha = 0
exiting = False
running = True
fps = 60


def main():
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, game_starting, timer, alpha, exiting, running, fps
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME, pygame.SRCALPHA)
    menu_window = Menu(screen, active=True)
    shop_window = Shop(screen)
    game_window = Game(screen)

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if menu_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'играть':
                    game_starting = True
                    game_window.active = True
                    menu_window.active = False
                elif butt_text == 'ларек':
                    old_scene = menu_window
                    new_scene = shop_window
                    start_transition = True
                elif butt_text == 'выход':
                    exiting = True
            elif shop_window.on_click(event):
                butt_text = shop_window.on_click(event).get_text()
                if butt_text == '-1 ошибка':
                    pass
                elif butt_text == '+1 буква':
                    pass
                elif butt_text == 'игра':
                    pass
                elif butt_text == 'кнопки':
                    pass
                elif butt_text == 'детали':
                    pass
                elif butt_text == 'буквы':
                    pass
                elif butt_text == 'фон':
                    pass
                elif butt_text == 'назад':
                    menu_window.active = True
                    shop_window.active = False

            elif game_window.on_click(event):
                butt_text = game_window.on_click(event).get_text()
                if butt_text == 'выйти':
                    menu_window.active = True
                    game_window.active = False

        # Логика переключения окон
        if menu_window.active:
            menu_window.selecting_button()
            menu_window.render()
        elif shop_window.active:
            shop_window.selecting_button()
            shop_window.render()
        elif game_window.active:
            game_window.selecting_button()
            game_window.render()

        transition()

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 800), ws_width)
        black_screen.fill((0, 0, 0))
        black_screen.set_alpha(alpha)
        screen.blit(black_screen, (0, 0))

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


def transition():  # Переход между сценами
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, game_starting, timer, alpha, exiting, running, fps
    if start_transition:
        ws_width += 50
        if ws_width == 301:
            old_scene.active = False
            new_scene.active = True
            start_transition = False
            stop_transition = True
    if stop_transition:
        ws_width -= 50
        if ws_width == 1:
            stop_transition = False
    if game_starting:
        if timer > 0:
            alpha = 255
            timer -= 1
        else:
            fps = 15
            alpha -= 10
            if alpha == 5:
                fps, alpha, timer = 60, 0, 120
                game_starting = False
    if exiting:
        alpha += 10
        if alpha == 250:
            running = False


if __name__ == '__main__':
    main()
