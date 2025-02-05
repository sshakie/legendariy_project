import os

import pygame, random
from pygame import MOUSEBUTTONDOWN

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
    letter_thing = int(config.split('\n')[7].split()[-1])
    wins = int(config.split('\n')[8].split()[-1])
    captches = int(config.split('\n')[9].split()[-1])

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
time_for_game = 180
attempts_for_game = 5
captcha = {'в цепи': (0, 0, 148, 64), 'высшую': (149, 0, 252, 113), 'беккерелем': (402, 0, 235, 76),
           'возникновение': (638, 0, 207, 56), 'обусловливающая': (846, 0, 246, 60),
           'распада ядер': (1093, 0, 98, 56), 'система': (1192, 0, 148, 37), 'мерно': (1341, 0, 79, 48),
           'номера': (1421, 0, 151, 58),
           'человеконенавистничество': (1573, 0, 245, 94), 'миролюбивый': (1396, 95, 199, 98),
           'аэропорт': (1596, 95, 204, 99)}

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
    global menu_window, shop_window, game_window, wins, attempts_for_game, time_for_game, captches
    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.SRCALPHA)
    menu_window = Menu(screen, money, active=True)
    shop_window = Shop(screen, money, mistake_thing, letter_thing)
    playing = False

    # Звуки
    sfx_start = pygame.mixer.Sound('data/sounds/menu/start.wav')
    sfx_start.play()
    sfx_click = pygame.mixer.Sound('data/sounds/click.wav')

    image = ''
    captcha_word = ''
    writing = ''

    clock = pygame.time.Clock()
    update_shop_buttons()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exiting = True
            if menu_window.on_click(event):
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'играть':
                    if 2 <= wins <= 3:
                        attempts_for_game = 4
                        time_for_game = 120
                    elif 4 <= wins <= 5:
                        attempts_for_game = 3
                        time_for_game = 90
                    elif wins > 6:
                        attempts_for_game = 2
                        time_for_game = 60
                    game_window = Game(screen, mistake_thing, letter_thing, attempts=attempts_for_game,
                                       timer=time_for_game, active=True)
                    game_starting = True
                    menu_window.active = False
                    with open('data/config', 'w') as config:
                        config.write(f'money {money}\n'
                                     f'button {int(button_custom)}\n'
                                     f'details {int(details_custom)}\n'
                                     f'letter {int(letter_custom)}\n'
                                     f'wallpaper {int(wallpaper_custom)}\n'
                                     f'can_wallpaper {int(wallpaper_can_buy)}\n'
                                     f'mistake {mistake_thing}\n'
                                     f'letter {letter_thing}\n'
                                     f'win {wins}\n'
                                     f'captcha {captches}')
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
                if butt_text == 'право на ошибку' and playing is False:
                    if buy(45):
                        mistake_thing += 1
                        shop_window.mistake_count = shop_window.font.render(str(mistake_thing), True, (100, 0, 0))
                elif butt_text == 'раскрыть букву' and playing is False:
                    if buy(35):
                        letter_thing += 1
                        shop_window.letter_count = shop_window.font.render(str(letter_thing), True, (100, 0, 0))
                elif butt_text == 'игра-капча' and playing is False and captches < 10:
                    if buy(25):
                        playing = True
                        pair = random.choice(list(captcha.items()))
                        image = load_image('data/textures/captcha.png').subsurface(pair[-1])
                        image = pygame.transform.scale(image, (203, 112))
                        captcha_word = pair[0]
                        writing = ''
                elif butt_text == 'кнопки' and playing is False:
                    if button_custom is False:
                        if buy(75):
                            button_custom = True
                elif butt_text == 'детали' and playing is False:
                    if details_custom is False:
                        if buy(100):
                            details_custom = True
                elif butt_text == 'буквы' and playing is False:
                    if letter_custom is False:
                        if buy(50):
                            letter_custom = True
                elif butt_text == 'фон' and playing is False:
                    if wallpaper_can_buy and wallpaper_custom is False:
                        if buy(250):
                            wallpaper_custom = True

                elif butt_text == 'назад' and playing is False:
                    old_scene = shop_window
                    new_scene = menu_window
                    start_transition = True
                    sfx_click.play()

            if isinstance(game_window, Game):
                if game_window.on_click(event):
                    butt_text = game_window.on_click(event).get_text()
                    if butt_text == 'выйти' and game_window.display_sure is False:
                        game_window.display_sure = True
                        sfx_click.play()
                    elif butt_text == 'выйти2' or butt_text == 'выйти3':
                        if butt_text == 'выйти3':
                            wins += 1
                        menu_window.active = True
                        game_window.active = False
                        timer, transition_alpha, k = 60, 255, 4
                        game_starting = True
                        money += game_window.prize
                        sfx_click.play()
                    elif butt_text == 'заново' or butt_text == 'заново2':
                        if butt_text == 'заново2':
                            wins += 1
                        if 2 <= wins <= 3:
                            attempts_for_game = 4
                            time_for_game = 120
                        elif 4 <= wins <= 5:
                            attempts_for_game = 3
                            time_for_game = 90
                        elif wins > 6:
                            attempts_for_game = 2
                            time_for_game = 60

                        game_window = Game(screen, mistake_thing, letter_thing, attempts=attempts_for_game,
                                           timer=time_for_game, active=True)
                        money += game_window.prize
                        sfx_click.play()

            if event.type == MOUSEBUTTONDOWN:
                if isinstance(game_window, Game):
                    accepting = game_window.accept_exiting(event)
                else:
                    accepting = None
                if accepting == 'yes':
                    game_window.active = False
                    menu_window.active = True
                    timer, transition_alpha, k = 60, 255, 4
                    game_starting = True
                    sfx_click.play()
                elif accepting == 'no':
                    game_window.display_sure = False
                    sfx_click.play()


            if event.type == pygame.KEYDOWN and playing:
                if event.key == pygame.K_BACKSPACE:
                    writing = writing[:-1]
                    pygame.mixer.Sound('data/sounds/game/backspace.wav').play()
                elif event.key == pygame.K_RETURN:
                    if writing == captcha_word:
                        money += 35
                        pygame.mixer.Sound('data/sounds/shop/win.wav').play()
                        captches += 1
                    else:
                        pygame.mixer.Sound('data/sounds/shop/lose.wav').play()
                    playing = False
                elif event.unicode in 'абвгдежзийклмнопрстуфхцчшщъыьэюя ':
                    writing += event.unicode
                    pygame.mixer.Sound('data/sounds/game/press.wav').play()

        menu_window.update(money)
        shop_window.update(money)
        update_shop_buttons()

        # Логика переключения окон
        if menu_window.active:
            menu_window.selecting_button()
            menu_window.render()
        elif shop_window.active:
            if playing is False:
                shop_window.selecting_button()
            shop_window.render()
        elif game_window.active:
            game_window.selecting_button()
            game_window.render()

        if playing:
            screen.blit(load_image('data/textures/captcha-screen.png'), (0, 0))
            screen.blit(image, (358, 208))
            font = pygame.font.Font('data/myy.ttf', 20)
            screen.blit((font.render(writing, True, (255, 255, 255))), (364, 326))

        transition()
        glow_alpha = max(0, glow_alpha - 2)

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
                             f'letter {letter_thing}\n'
                             f'win {wins}\n'
                             f'captcha {captches}')
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
