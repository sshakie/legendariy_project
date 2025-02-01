import pygame
from data.code.Button import *
from data.code.game.game import Game
from data.code.menu.menu import Menu
from data.code.shop.shop import Shop


def main():
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME)
    menu_window = Menu(screen, active=True)
    shop_window = Shop(screen)
    game_window = Game(screen)

    running = True
    fps = 60
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if menu_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'играть':
                    game_window.active = True
                    menu_window.active = False
                elif butt_text == 'ларек':
                    shop_window.active = True
                    menu_window.active = False
                elif butt_text == 'выход':
                    running = False
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

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
