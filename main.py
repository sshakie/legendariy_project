import pygame
from data.code.Button import *
from data.code.game.game import Game
from data.code.menu.menu import Menu
from data.code.shop.shop import Shop

running = True
fps = 60
with open('data/config') as config:
    config = config.read()
    money = int(config.split('\n')[0].split()[-1])
    button_custom = bool(int(config.split('\n')[1].split()[-1]))
    details_custom = bool(int(config.split('\n')[2].split()[-1]))
    letter_custom = bool(int(config.split('\n')[3].split()[-1]))
    wallpaper_can_buy = bool(int(config.split('\n')[4].split()[-1]))
    wallpaper_custom = bool(int(config.split('\n')[5].split()[-1]))
    mistake_thing = int(config.split('\n')[6].split()[-1])
    letter_thing = int(config.split('\n')[6].split()[-1])

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

pygame.init()
sfx_exit = pygame.mixer.Sound('data/sounds/menu/end.wav')
sfx_transition = pygame.mixer.Sound('data/sounds/transition.wav')
sfx_success = pygame.mixer.Sound('data/sounds/shop/success.wav')
sfx_fail = pygame.mixer.Sound('data/sounds/shop/fail.wav')

menu_window = ''
shop_window = ''
game_window = ''


def main():
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, glow_color
    global game_starting, timer, transition_alpha, exiting, running, fps, k, money, glow_alpha
    global button_custom, details_custom, letter_custom, wallpaper_can_buy, wallpaper_custom, mistake_thing, letter_thing
    global menu_window, shop_window, game_window
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.SRCALPHA)
    menu_window = Menu(screen, money, active=True)
    shop_window = Shop(screen, money)
    game_window = Game(screen)

    # Звуки
    sfx_start = pygame.mixer.Sound('data/sounds/menu/start.wav')
    sfx_start.play()
    sfx_click = pygame.mixer.Sound('data/sounds/click.wav')

    clock = pygame.time.Clock()
    update_shop_buttons()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exiting = True

            if menu_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'играть':
                    game_window = Game(screen)
                    game_starting = True
                    game_window.active = True
                    menu_window.active = False
                    sfx_click.play()
                elif butt_text == 'ларек':
                    old_scene = menu_window
                    new_scene = shop_window
                    start_transition = True
                    sfx_click.play()
                elif butt_text == 'выход':
                    exiting = True
            elif shop_window.on_click(event):
                butt_text = shop_window.on_click(event).get_text()
                if butt_text == 'право на ошибку':
                    if buy(10):
                        mistake_thing += 1
                elif butt_text == 'раскрыть букву':
                    if buy(25):
                        letter_thing += 1
                elif butt_text == 'игра-капча':
                    money += 15
                elif butt_text == 'кнопки':
                    if button_custom is False:
                        if buy(30):
                            button_custom = True
                elif butt_text == 'детали':
                    if details_custom is False:
                        if buy(45):
                            details_custom = True
                elif butt_text == 'буквы':
                    if letter_custom is False:
                        if buy(50):
                            letter_custom = True
                elif butt_text == 'фон':
                    if wallpaper_can_buy and wallpaper_custom is False:
                        if buy(65):
                            wallpaper_custom = True

                elif butt_text == 'назад':
                    old_scene = shop_window
                    new_scene = menu_window
                    start_transition = True
                    sfx_click.play()

                menu_window.update(money)
                shop_window.update(money)
                update_shop_buttons()

            elif game_window.on_click(event):
                butt_text = game_window.on_click(event).get_text()
                if butt_text == 'выйти':
                    menu_window.active = True
                    game_window.active = False
                    timer, transition_alpha, k = 60, 255, 4
                    game_starting = True
                elif butt_text == 'заново':
                    game_window = Game(screen)
                sfx_click.play()

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
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, glow_color
    global game_starting, timer, transition_alpha, exiting, running, fps, k, money, glow_alpha
    global sfx_exit, sfx_transition
    if start_transition:
        if ws_width == 1:
            sfx_transition.play()
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
        if transition_alpha == 0:
            sfx_exit.play()
        transition_alpha += 5
        if transition_alpha == 250:
            with open('data/config', 'w') as config:
                config.write(f'money {money}\n'
                             f'button {int(button_custom)}\n'
                             f'details {int(details_custom)}\n'
                             f'letter {int(letter_custom)}\n'
                             f'wallpaper {int(wallpaper_custom)}\n'
                             f'can_wallpaper {int(wallpaper_can_buy)}\n'
                             f'mistake {mistake_thing}\n'
                             f'letter {letter_thing}')
            running = False


def buy(cost):
    global money, glow_color, glow_alpha, sfx_success, sfx_fail
    if money - cost >= 0:
        money -= cost
        glow_color = [0, 255, 0]
        sfx_success.play()
    else:
        glow_color = [255, 0, 0]
        sfx_fail.play()
    glow_alpha = min(glow_alpha + 50, 150)
    return glow_color == [0, 255, 0]


def update_shop_buttons():
    global button_custom, details_custom, letter_custom, wallpaper_can_buy, wallpaper_custom, mistake_thing, letter_thing
    global menu_window, shop_window, game_window
    if button_custom:
        shop_window.button_custom.set_image((270, 261, 134, 75), 405)
    if details_custom:
        shop_window.detail_custom.set_image((270, 261, 134, 75), 405)
    if letter_custom:
        shop_window.letter_custom.set_image((270, 261, 134, 75), 405)
    if wallpaper_custom:
        shop_window.background_custom.set_image((174, 337, 86, 59), 261)
    if button_custom and details_custom and letter_custom and wallpaper_can_buy is False:
        shop_window.background_custom.set_image((0, 337, 86, 59), 87)
        wallpaper_can_buy = True


if __name__ == '__main__':
    main()
