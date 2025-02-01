import pygame
from data.code.Button import *
from data.code.game.game import Game
from data.code.menu.menu import Menu
from data.code.shop.shop import Shop

running = True
fps = 60
with open('data/config') as config:
    money = int(config.read().split('\n')[0].split()[-1])
# Для перехода между сценами
old_scene = None
new_scene = None
start_transition = False
stop_transition = False
game_starting = True
exiting = False
black_screen = pygame.Surface((600, 800))
glow_screen = pygame.Surface((600, 800))
transition_alpha = 255
glow_alpha = 0
glow_color = [0, 255, 0]
ws_width = 1
timer = 0
k = 4


def main():
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, game_starting, timer, transition_alpha, exiting, running, fps, k, money, glow_alpha, glow_color
    pygame.init()
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.NOFRAME, pygame.SRCALPHA)
    menu_window = Menu(screen, money, active=True)
    shop_window = Shop(screen, money)
    game_window = Game(screen)

    ui = pygame.mixer.Sound('data/sounds/ui sound.wav')
    ui.play()

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('data/config', 'w') as config:
                    config.write(f'money {money}')
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
                if butt_text == 'право на ошибку':
                    if buy(15000000):
                        print(1)
                elif butt_text == 'раскрыть букву':
                    if buy(10000000):
                        print(2)
                elif butt_text == 'игра-капча':
                    money += 15
                elif butt_text == 'кнопки':
                    if buy(20000000):
                        print(3)
                elif butt_text == 'детали':
                    if buy(17000000):
                        print(4)
                elif butt_text == 'буквы':
                    if buy(35000000):
                        print(5)
                elif butt_text == 'фон':
                    if buy(6000000):
                        print(6)
                elif butt_text == 'назад':
                    old_scene = shop_window
                    new_scene = menu_window
                    start_transition = True

                menu_window.update(money)
                shop_window.update(money)

            elif game_window.on_click(event):
                butt_text = game_window.on_click(event).get_text()
                if butt_text == 'выйти':
                    menu_window.active = True
                    game_window.active = False
                    timer, transition_alpha, k = 60, 255, 4
                    game_starting = True

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
        glow_alpha = max(0, glow_alpha - 1)

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 800), ws_width)
        black_screen.fill((0, 0, 0))
        black_screen.set_alpha(transition_alpha)
        glow_screen.fill(tuple(glow_color))
        glow_screen.set_alpha(glow_alpha)
        screen.blit(black_screen, (0, 0))
        screen.blit(glow_screen, (0, 0))

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


def transition():  # Переход между сценами
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, game_starting, timer, transition_alpha, exiting, running, fps, k, money, glow_alpha, glow_color
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
            transition_alpha = 255
            timer -= 1
        else:
            fps = 15 * k
            transition_alpha -= 10
            if transition_alpha == 5:
                fps, transition_alpha, timer = 60, 0, 120
                game_starting = False
                k = 1
    if exiting:
        transition_alpha += 10
        if transition_alpha == 250:
            with open('data/config', 'w') as config:
                config.write(f'money {money}')
            running = False


def buy(cost):
    global money, glow_color, glow_alpha
    if money - cost >= 0:
        money -= cost
        glow_color = [0, 255, 0]
    else:
        glow_color = [255, 0, 0]
    glow_alpha = min(glow_alpha + 50, 150)
    return glow_color == [0, 255, 0]


if __name__ == '__main__':
    main()
