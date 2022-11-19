""" Игра Бандерогусак, анимация фона, героя, бонусов и врагов
"""
import random                           # импортируем библиотеку random
import pygame                           # импортируем библиотеку pygame
pygame.init()                           # инициализируем/вызываем библиотеку pygame
screen_size = WIDTH, HEIGHT = 800, 600  # ширина и высота окна
main_surface = pygame.display.set_mode((screen_size), pygame.DOUBLEBUF | pygame.HWSURFACE) # создаём поверхность отрисовки
# set_mode(Width, Height) - формируем/вызываем окно (щирина, высота) в pixel
# pygame.DOUBLEBUF - двойная буферизация
# pygame.HWSURFACE - аппаратное ускорение отрисовки
# pygame.FULLSCREEN - полноэкранный режим
# pygame.OPENGL - обработка отображений с помощью библиотеки OpenGL
# pygame.RESIZABLE - окно с  изменяемыми размерами
# pygame.NOFRAME - окно без рамки и заголовка
# pygame.SCALED - разрешение, зависящее от размеров рабочего стола
pygame.display.set_caption("Banderogusak on PyGame")                        # устанавливаем название окна
pygame.display.set_icon(pygame.image.load("image/goose2.jpg"))              # устанавливаем иконку окна
clock = pygame.time.Clock()             # создаём экземпляр класса Clock
FPS = 60                                # устанавливаем частоту обработки цикла, FPS раз в секунду

RED = (255, 0, 0),              # цвет красный
GREEN = (0, 255, 0),            # цвет зелённый
BLUE = (0, 0, 255)              # цвет синий
BLACK = (0, 0, 0)               # цвет чёрный
WHITE = (255, 255, 255)         # цвет белый
GRAY = (128, 128, 128)          # цвет серый
YELLOW = (255, 255, 0)          # цвет жёлтый
PINK = (255, 0, 255)            # цвет розовый
VIOLET = (0, 255, 255)          # цвет фиолетовый

hero_attr = {                   # hero position. положение "героя"
    "x": WIDTH/2,               # начальное положение "героя", координата X
    "y": HEIGHT/2,              # начальное положение "героя", координата Y
    "speed": 5,                 # смещение "героя" по координате X или Y
    "color": WHITE              # RGB цвет "героя"
}
hero = pygame.Surface((20, 20))                             # создаём поверхность "героя"
hero.fill(hero_attr["color"])                               # закрашиваем поверхность "героя" в текущий цвет
hero_rect = hero.get_rect()                                 # получаем размеры и положение поверхности "героя"
hero_rect = hero_rect.move(hero_attr["x"], hero_attr["y"])  # смещаем поверхность "героя" на середину рабочего окна


enemy_color_list = [RED, GREEN, BLUE, GRAY, PINK, VIOLET]   # перечень возможных цветов "врага"
enemy_width_min = 10
enemy_width_max = 30

def create_enemy():
    enemy_width = random.randint(enemy_width_min, enemy_width_max)  # создаём произвольный размер "врага"
    enemy = pygame.Surface((enemy_width, enemy_width))              # создаём произвольную поверхность "врага"
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy.get_size())
    enemy_speed = random.randint(2, 5)                  # создаём произвольную скорость "врага"
    enemy_color = random.randint(0, 5)                  # создаём произвольный цвет "врага"
    enemy.fill(enemy_color_list[enemy_color])           # закрашиваем поверхность в цвет "врага"
    print(f'There are {len(enemies)} enemies. Created a new enemy with size {enemy_width}px and color {enemy_color_list[enemy_color]}')
    return [enemy, enemy_rect, enemy_speed]             # возвращяем данные очередного "врага"

def create_bonus():
    bonus_width = 20                                    # создаём размер поверхности "бонуса"
    bonus = pygame.Surface((bonus_width, bonus_width))  # создаём поверхность "бонуса"
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)                  # создаём произвольную скорость "бонуса"
    bonus_color = YELLOW                                # создаём цвет "бонуса"
    bonus.fill(bonus_color)                             # закрашиваем поверхность в цвет "бонуса"
    print(f'There are {len(bonuses)} bonuses. Created a new bonus')
    return [bonus, bonus_rect, bonus_speed]             # возвращяем данные очередного "бонуса"

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)               # установка таймера вызова функции сосздания нового "врага", 1500 мс

CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 2000)               # установка таймера вызова функции сосздания нового "бонуса", 2000 мс

enemies = []
bonuses = []
score = 0
font_score = pygame.font.SysFont('Verdana', 20)         # устанавливаем щрифт и размер текста (px)
# SysFont(name, size, bold=False, italic=False)

# start game loop
game_over = False                               # флаг "конец игры"
while not game_over:                            # start game loop
    for event in pygame.event.get():            # переменная event принимает значение сообщений из очереди событий pygame.event.
        if event.type == pygame.QUIT:           # проверяем ТИП события event, равно ли QUIT (нажата ли иконка закрытия рабочего окна)
            game_over = True                    # выход из основного цикла
        if event.type == CREATE_ENEMY:          # если появилось событие создать "врага"
            enemies.append(create_enemy())      # в список "врагов" добавляем нового "врага"
        if event.type == CREATE_BONUS:          # если появилось событие создать "бонус"
            bonuses.append(create_bonus())      # в список "врагов" добавляем новый "бонус"
    # управление "героем"
    keys = pygame.key.get_pressed()             # в переменную key записываем состояние всех клавиш на клавиатуре
    # все нажатые кнопки имеют статус TRUE (1), остальные FALSE (0)
    if keys[pygame.K_LEFT] and hero_rect.left > 0:  # если кнопка K_LEFT нажата и поверхность "героя" не в самом начале
        hero_rect = hero_rect.move(-hero_attr["speed"], 0)  # свдвигаем поверхность "героя" влево
    if keys[pygame.K_RIGHT] and hero_rect.right < WIDTH:  # если кнопка K_RIGHT нажата и поверхность "героя" не в самом конце
        hero_rect = hero_rect.move(hero_attr["speed"], 0)  # свдвигаем поверхность "героя" вправо
    if keys[pygame.K_UP] and hero_rect.top > 0:  # если кнопка K_UP нажата и поверхность "героя" не в самом верху
        hero_rect = hero_rect.move(0, -hero_attr["speed"])  # свдвигаем поверхность "героя" вверх
    if keys[pygame.K_DOWN] and hero_rect.bottom < HEIGHT:  # если кнопка K_DOWN нажата и поверхность "героя" не в самом низу
        hero_rect = hero_rect.move(0, hero_attr["speed"])  # свдвигаем поверхность "героя" вниз

    main_surface.fill(BLACK)                    # clear screen
    main_surface.blit(hero, hero_rect)          # накладываем поверность "героя" на основную поверхность "фон"

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        if enemy[1].left < 0:                   # если поверхность "врага" ушла за левый край рабочего окна
            enemies.pop(enemies.index(enemy))   # удаляем "врага" из списка "врагов"
            print(f'There are {len(enemies)} enemies. Delete one old enemy.')
        else:                                       # иначе
            main_surface.blit(enemy[0], enemy[1])   # накладываем поверхность "врага" на основную поверхность "фон"

        if hero_rect.colliderect(enemy[1]):         # если плоскость "героя" пересеклась с плоскостью "врага"
            game_over = True                        # устанавливаем флаг "конец игры", выход из основного цикла
            print(f'Игра окнчена. Ваш "герой" погиб. Вы набрали {score} очков.')

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        if bonus[1].bottom > HEIGHT:                   # если поверхность "бонус" ушла за нижний край рабочего окна
            bonuses.pop(bonuses.index(bonus))           # удаляем "бонус" из списка "бонусов"
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus.')
        else:                                       # иначе
            main_surface.blit(bonus[0], bonus[1])   # накладываем поверхность "врага" на основную поверхность "фон"

        if hero_rect.colliderect(bonus[1]):         # если плоскость "героя" пересеклась с плоскостью "бонус"
            bonuses.pop(bonuses.index(bonus))       # удаляем "врага" из списка "бонусов"
            score += 1
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus. Score = {score}')

    pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
    clock.tick(FPS)                     # вызывааем метод tick() класса Clock(), устанавливаем задержку для цикла, FPS
                                        # FPS раз в секунду с учётом времени на выполнение операций в самом цикле
pygame.quit()  # выход из модуля pygame
quit()
