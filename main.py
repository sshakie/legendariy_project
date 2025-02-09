import pygame, random
from data.code.Button import *
from data.code.game.game import Game
from data.code.menu.menu import Menu
from data.code.shop.shop import Shop

# Подгрузка компонентов из конфига / Создание конфига
try:
    with open('data/config.txt') as config:
        config = config.read()
        money = int(config.split('\n')[0].split()[-1])
        button_custom = bool(int(config.split('\n')[1].split()[-1]))
        details_custom = bool(int(config.split('\n')[2].split()[-1]))
        font_custom = bool(int(config.split('\n')[3].split()[-1]))
        wallpaper_custom = bool(int(config.split('\n')[4].split()[-1]))
        mistake_goods = int(config.split('\n')[5].split()[-1])
        letter_goods = int(config.split('\n')[6].split()[-1])
        wins = int(config.split('\n')[7].split()[-1])
        captches = int(config.split('\n')[8].split()[-1])
except FileNotFoundError:
    with open('data/config.txt', 'w+') as config:
        money, button_custom, details_custom, font_custom, wallpaper_can_buy = 0, 0, 0, 0, 0
        wallpaper_custom, mistake_goods, letter_goods, wins, captches = 0, 0, 0, 0, 0
        config.write(f'money {money}\n'
                     f'button {int(button_custom)}\n'
                     f'details {int(details_custom)}\n'
                     f'font {int(font_custom)}\n'
                     f'wallpaper {int(wallpaper_custom)}\n'
                     f'mistake {mistake_goods}\n'
                     f'letter {letter_goods}\n'
                     f'win {wins}\n'
                     f'captcha {captches}')
wallpaper_can_buy = False

# Для перехода между сценами
old_scene, new_scene = None, None
start_transition, stop_transition = False, False
game_starting = True
exiting = False
black_screen, glow_screen = pygame.Surface((600, 800)), pygame.Surface((600, 800))
transition_alpha = 255
glow_color, glow_alpha = [0, 255, 0], 0
ws_width = 1
transition_timer = 0
k = 4  # нужно в моменте

# Остальное
menu_window, shop_window, game_window = '', '', ''
pygame.init()
running = True
fps = 60
captcha = {'в цепи': (0, 0, 148, 64), 'высшую': (149, 0, 252, 113), 'беккерелем': (402, 0, 235, 76),
           'возникновение': (638, 0, 207, 56), 'обусловливающая': (846, 0, 246, 60),
           'распада ядер': (1093, 0, 98, 56), 'система': (1192, 0, 148, 37), 'мерно': (1341, 0, 79, 48),
           'номера': (1421, 0, 151, 58), 'разгадай': (1573, 0, 245, 94), 'миролюбивый': (1396, 95, 199, 98),
           'аэропорт': (1596, 95, 204, 99), 'моленье': (1255, 95, 140, 56), 'время приключений': (1255, 152, 140, 42),
           'кот': (1095, 79, 159, 115), 'медуза': (1044, 133, 50, 61), 'собака': (924, 105, 119, 89),
           'ноты': (828, 126, 95, 68),
           'обруч': (791, 126, 36, 38), 'небо': (713, 126, 77, 47)}


def main():
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, glow_color
    global game_starting, transition_timer, transition_alpha, exiting, running, fps, k, money, glow_alpha
    global button_custom, details_custom, font_custom, wallpaper_can_buy, wallpaper_custom, mistake_goods, letter_goods
    global menu_window, shop_window, game_window, wins, attempts_for_game, time_for_game, captches

    pygame.display.set_caption('Wordy')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size, pygame.SRCALPHA)

    menu_window = Menu(screen, money, active=True)
    shop_window = Shop(screen, money, mistake_goods, letter_goods)
    update_shop_buttons()
    update_coloring()
    old_mistake_goods = mistake_goods
    old_letter_goods = letter_goods

    # Звуки
    timer_event, timer_event2 = pygame.USEREVENT + 1, pygame.USEREVENT + 2  # Создал, чтобы не накладывались ост на звуки
    pygame.time.set_timer(timer_event, 2000, loops=1)
    timer_event_actived = True

    pygame.mixer.Sound('data/sounds/menu/start.wav').play()
    sfx_click = pygame.mixer.Sound('data/sounds/click.wav')

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exiting = True
            if event.type == timer_event:  # Сделал, чтобы не накладывались ост на звуки
                if menu_window.active:
                    pygame.mixer.music.load('data/sounds/menu/ost.wav')
                    pygame.mixer.music.play(loops=-1)
                elif shop_window.active:
                    pygame.mixer.music.load('data/sounds/shop/ost.wav')
                    pygame.time.delay(500)
                    pygame.mixer.music.play(loops=-1, fade_ms=500)
                timer_event_actived = False
            if event.type == timer_event2 and game_window.active:  # Сделал, чтобы успел fadeout menu_ost
                pygame.mixer.music.load('data/sounds/game/ost (by zer).wav')
                pygame.mixer.music.play(loops=-1)
            if event.type == pygame.KEYDOWN:  # Кейбинды выхода
                if shop_window.playing:
                    if shop_window.key_pressing(event):
                        money += 35
                        captches += 1
                elif event.key == pygame.K_ESCAPE:
                    if shop_window.active:
                        old_scene, new_scene = shop_window, menu_window
                        start_transition = True
                        sfx_click.play()
                        pygame.mixer.music.load('data/sounds/menu/ost.wav')
                        pygame.mixer.music.play(loops=-1)
                    elif isinstance(game_window, Game):
                        game_window.display_sure = True
                        sfx_click.play()

            if menu_window.on_click(event):  # Если нажата кнопка в меню
                butt_text = menu_window.on_click(event).get_text()
                if butt_text == 'играть' and not exiting:
                    # Настройка усложнения игры:
                    # до 4 побед = 5 поп., 220 сек | от 5 до 8 побед = 4 поп., 185 сек | от 8 до 11 побед = 3 поп. 150 сек | больше = 3 поп. 110 сек
                    time_for_game = 220
                    attempts_for_game = 5
                    if 5 <= wins <= 8:
                        attempts_for_game = 4
                        time_for_game = 185
                    elif 8 <= wins <= 11:
                        attempts_for_game = 3
                        time_for_game = 150
                    elif wins > 11:
                        attempts_for_game = 3
                        time_for_game = 110

                    game_window = Game(screen, time_for_game, attempts_for_game,
                                       mistake_goods=mistake_goods, letter_goods=letter_goods,
                                       wallpaper_bought=wallpaper_custom, font_bought=font_custom, active=True)
                    menu_window.active = False

                    if mistake_goods > 0:
                        old_mistake_goods = mistake_goods
                        mistake_goods -= 1
                    if letter_goods > 0:
                        old_letter_goods = letter_goods
                        letter_goods -= 1

                    game_starting = True  # Запускает переход
                    with open('data/config.txt', 'w') as config:
                        config.write(f'money {money}\n'
                                     f'button {int(button_custom)}\n'
                                     f'details {int(details_custom)}\n'
                                     f'font {int(font_custom)}\n'
                                     f'wallpaper {int(wallpaper_custom)}\n'
                                     f'mistake {mistake_goods}\n'
                                     f'letter {letter_goods}\n'
                                     f'win {wins}\n'
                                     f'captcha {captches}')

                    sfx_click.play()
                    pygame.mixer.music.fadeout(1000)
                    pygame.time.set_timer(timer_event2, 1001, loops=1)
                elif butt_text == 'ларек' and not exiting:
                    old_scene, new_scene = menu_window, shop_window
                    start_transition = True

                    sfx_click.play()
                    if not timer_event_actived:
                        pygame.mixer.music.load('data/sounds/shop/ost.wav')
                        pygame.mixer.music.play(loops=-1)
                elif butt_text == 'выход':
                    exiting = True

            elif shop_window.on_click(event):  # Если нажата кнопка в ларьке
                butt_text = shop_window.on_click(event).get_text()
                if butt_text == 'право на ошибку' and shop_window.playing is False:
                    if buy(45):
                        mistake_goods += 1
                        shop_window.mistake_count = shop_window.font.render(str(mistake_goods), True, (100, 0, 0))
                elif butt_text == 'раскрыть букву' and shop_window.playing is False:
                    if buy(35):
                        letter_goods += 1
                        shop_window.letter_count = shop_window.font.render(str(letter_goods), True, (100, 0, 0))
                elif butt_text == 'игра-капча' and shop_window.playing is False and captches < 10:
                    if buy(25):
                        pair = random.choice(list(captcha.items()))
                        image = load_image('data/textures/captcha.png').subsurface(pair[-1])
                        shop_window.captcha_image = pygame.transform.scale(image, (203, 112))
                        shop_window.captcha_word = pair[0]
                        shop_window.writing = ''
                        shop_window.playing = True
                elif butt_text == 'кнопки' and shop_window.playing is False:
                    if button_custom is False:
                        if buy(75):
                            button_custom = True
                            update_shop_buttons()
                            update_coloring()
                elif butt_text == 'детали' and shop_window.playing is False:
                    if details_custom is False:
                        if buy(100):
                            details_custom = True
                            update_shop_buttons()
                            update_coloring()
                elif butt_text == 'шрифт' and shop_window.playing is False:
                    if font_custom is False:
                        if buy(50):
                            font_custom = True
                            update_shop_buttons()
                            update_coloring()
                elif butt_text == 'фон' and shop_window.playing is False:
                    if wallpaper_can_buy and wallpaper_custom is False:
                        if buy(250):
                            wallpaper_custom = True
                            update_shop_buttons()
                            update_coloring()

                elif butt_text == 'назад' and not shop_window.playing and not start_transition and not stop_transition:
                    old_scene, new_scene = shop_window, menu_window
                    start_transition = True

                    sfx_click.play()
                    if not timer_event_actived:
                        pygame.mixer.music.load('data/sounds/menu/ost.wav')
                        pygame.mixer.music.play(loops=-1, fade_ms=1000)

            if isinstance(game_window, Game):
                if game_window.on_click(event):  # Если нажата кнопка в игре
                    butt_text = game_window.on_click(event).get_text()
                    if butt_text == 'выйти' and game_window.display_sure is False:
                        game_window.display_sure = True
                        sfx_click.play()
                    if butt_text == 'выйти2' or butt_text == 'выйти3':  # выйти2/выйти3 = кнопка из проигрыша/выигрыша
                        if butt_text == 'выйти3':
                            wins += 1
                            money += game_window.prize

                        game_window = ''
                        menu_window.active = True
                        transition_timer, transition_alpha, k = 60, 255, 4  # здесь k=4, чтобы фпс не падал, когда мне это нужно
                        game_starting = True  # Запускает переход

                        sfx_click.play()
                        pygame.mixer.music.load('data/sounds/menu/ost.wav')
                        pygame.mixer.music.play(loops=-1)
                    elif butt_text == 'заново' or butt_text == 'заново2':
                        # Настройка усложнения игры:
                        # до 4 побед = 5 поп., 220 сек | от 5 до 8 побед = 4 поп., 185 сек | от 8 до 11 побед = 3 поп. 150 сек | больше = 3 поп. 110 сек
                        time_for_game = 220
                        attempts_for_game = 5
                        if 5 <= wins <= 8:
                            attempts_for_game = 4
                            time_for_game = 185
                        elif 8 <= wins <= 11:
                            attempts_for_game = 3
                            time_for_game = 150
                        elif wins > 11:
                            attempts_for_game = 3
                            time_for_game = 110

                        game_window = Game(screen, time_for_game, attempts_for_game, mistake_goods=mistake_goods,
                                           letter_goods=letter_goods, wallpaper_bought=wallpaper_custom,
                                           font_bought=font_custom, active=True)
                        sfx_click.play()
                        pygame.mixer.music.load('data/sounds/game/ost (by zer).wav')
                        pygame.mixer.music.play(loops=-1)

            if event.type == pygame.MOUSEBUTTONDOWN and isinstance(game_window, Game):
                accepting = game_window.accept_exiting(event)
                if accepting == 'yes':
                    game_window = ''
                    menu_window.active = True
                    transition_timer, transition_alpha, k = 60, 255, 4  # здесь k=4, чтобы фпс не падал, когда мне это нужно
                    game_starting = True  # Запускает переход

                    sfx_click.play()
                    pygame.mixer.music.fadeout(2000)
                    pygame.time.set_timer(timer_event, 1000, loops=1)
                elif accepting == 'no':
                    game_window.display_sure = False
                    sfx_click.play()

        if isinstance(game_window, Game):
            if game_window.win_lose_flg is not None:
                pygame.mixer.music.fadeout(250)

        # Обновление счетчиков
        menu_window.money = money
        shop_window.money = money
        shop_window.mistake_goods = mistake_goods
        shop_window.letter_goods = letter_goods

        # Логика переключения окон
        if menu_window.active:
            menu_window.selecting_button()
            menu_window.render()
        elif shop_window.active:
            if shop_window.playing is False:
                shop_window.selecting_button()
            shop_window.render()
        elif game_window.active:
            game_window.selecting_button()
            game_window.render()

        # Для переходов
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 800), ws_width)
        transition()
        black_screen.fill((0, 0, 0))
        black_screen.set_alpha(transition_alpha)
        glow_screen.fill(tuple(glow_color))
        glow_screen.set_alpha(glow_alpha)
        glow_alpha = max(0, glow_alpha - 2)

        screen.blit(black_screen, (0, 0))
        screen.blit(glow_screen, (0, 0))
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


def buy(cost):  # Функция покупки товара
    global money, glow_color, glow_alpha
    if money - cost >= 0:
        money -= cost
        glow_color = [0, 255, 0]
        pygame.mixer.Sound('data/sounds/shop/success.wav').play()
    else:
        glow_color = [255, 0, 0]
        pygame.mixer.Sound('data/sounds/shop/fail.wav').play()
    glow_alpha = min(glow_alpha + 50, 150)
    return glow_color == [0, 255, 0]


def update_shop_buttons():  # Функция, обновляющая текстуры кнопки магазина для их закрытия/открытия
    global button_custom, details_custom, font_custom, wallpaper_can_buy, wallpaper_custom, mistake_goods, letter_goods
    global menu_window, shop_window, game_window
    if button_custom:
        shop_window.button_custom.set_image((270, 261, 134, 75), 405)
    if details_custom:
        shop_window.detail_custom.set_image((270, 261, 134, 75), 405)
    if font_custom:
        shop_window.font_custom.set_image((270, 261, 134, 75), 405)
    if wallpaper_custom:
        shop_window.background_custom.set_image((174, 337, 86, 59), 261)
    elif button_custom and details_custom and font_custom:
        shop_window.background_custom.set_image((0, 337, 86, 59), 87)
        wallpaper_can_buy = True


def transition():  # Функция переходов между сценами
    global ws_width, old_scene, new_scene, start_transition, stop_transition, black_screen, glow_color
    global game_starting, transition_timer, transition_alpha, exiting, running, fps, k, money, glow_alpha
    if start_transition:  # Запуск перехода между ларьком и меню (закрытие экрана)
        if ws_width == 1:
            pygame.mixer.Sound('data/sounds/transition.wav').play()
        ws_width += 50
        if ws_width == 301:
            old_scene.active = False
            new_scene.active = True
            start_transition = False
            stop_transition = True
    if stop_transition:  # Реверсия (открытие экрана)
        ws_width -= 50
        if ws_width == 1:
            stop_transition = False
    if game_starting:  # Переход между меню и игрой
        if transition_timer > 0:  # (закрытие экрана)
            if transition_alpha != 255:
                transition_alpha = 255
            transition_timer -= 1
        else:  # (открытие экрана)
            fps = 15 * k
            transition_alpha -= 10
            if transition_alpha == 5:
                fps, transition_alpha, transition_timer = 60, 0, 120
                game_starting = False
                k = 1
    if exiting:  # Анимация выхода из игры
        if transition_alpha == 0:
            pygame.mixer.Sound('data/sounds/menu/end.wav').play()
            pygame.mixer.music.fadeout(1000)
        transition_alpha += 5
        if transition_alpha == 250:  # закрытие игры
            with open('data/config.txt', 'w') as config:
                config.write(f'money {money}\n'
                             f'button {int(button_custom)}\n'
                             f'details {int(details_custom)}\n'
                             f'font {int(font_custom)}\n'
                             f'wallpaper {int(wallpaper_custom)}\n'
                             f'mistake {mistake_goods}\n'
                             f'letter {letter_goods}\n'
                             f'win {wins}\n'
                             f'captcha {captches}')
            running = False


def update_coloring():
    global menu_window, game_window, shop_window
    menu_window.wallpaper_bought = wallpaper_custom
    shop_window.wallpaper_bought = wallpaper_custom
    menu_window.details_bought = details_custom
    shop_window.details_bought = details_custom
    menu_window.buttons_bought = button_custom
    shop_window.buttons_bought = button_custom
    menu_window.font_bought = font_custom
    shop_window.font_bought = font_custom
    if font_custom:
        menu_window.text_font = 'data/myy-font.ttf'
        shop_window.text_font = 'data/myy-font.ttf'

    menu_window.bought_element()
    shop_window.bought_element()
    update_shop_buttons()


if __name__ == '__main__':
    main()
