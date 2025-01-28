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

    config = open('data/config').read()
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
                if butt_text == 'Играть':
                    game_window.active = True
                    menu_window.active = False
                elif butt_text == 'Ларёк':
                    shop_window.active = True
                    menu_window.active = False
                else:
                    running = False
                    # Нажата кнопка выхода
            elif shop_window.on_click(event):
                butt_text = shop_window.on_click(event).get_text()
                if butt_text == '-1 ошибка':
                    pass
                elif butt_text == '+1 буква':
                    pass
                elif butt_text == 'Игра':
                    pass
                elif butt_text == 'Кнопки':
                    pass
                elif butt_text == 'Детали':
                    pass
                elif butt_text == 'Буквы':
                    pass
                elif butt_text == 'Фон':
                    pass
                elif butt_text == '<- назад':
                    menu_window.active = True
                    shop_window.active = False

            # elif game_window.on_click(event):
            #     butt_text = game_window.on_click(event).get_text()
            #     if butt_text == 'выход':
            #         menu_window.active = True
            #         game_window.active = False

        # Логика переключения окон
        if menu_window.active:
            menu_window.render()
        elif shop_window.active:
            shop_window.render()
        elif game_window.active:
            game_window.render()

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
