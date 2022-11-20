""" Игра Бандерогусак, анимация фона, героя, бонусов и врагов
"""
import random                           # импортируем библиотеку random
import time                             # импортируем библиотеку time  (time.sleep(3))
from os import listdir                  # импортируем метод listdir
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
# GREEN = (0, 255, 0),            # цвет зелённый
# BLUE = (0, 0, 255)              # цвет синий
# BLACK = (0, 0, 0)               # цвет чёрный
# WHITE = (255, 255, 255)         # цвет белый
# GRAY = (128, 128, 128)          # цвет серый
# YELLOW = (255, 255, 0)          # цвет жёлтый
# PINK = (255, 0, 255)            # цвет розовый
# VIOLET = (0, 255, 255)          # цвет фиолетовый

hero_attr = {                   # hero position. положение "героя"
    "x": WIDTH/2,               # начальное положение "героя", координата X
    "y": HEIGHT/2,              # начальное положение "героя", координата Y
    "size": (100, 30),          # размер изображения "героя" (ширина, высота)
    "speed": 5,                 # смещение "героя" по координате X или Y
}
IMG_PATH = 'image/Goose'
hero_images = [pygame.transform.scale(pygame.image.load(IMG_PATH + '/' + file ).convert_alpha(), hero_attr["size"]) for file in listdir(IMG_PATH)]
#hero = pygame.transform.scale(pygame.image.load('image/Goose/1-1.png').convert_alpha(), hero_attr["size"])   # создаём поверхность "героя" и загружаем на неё изображение
hero_img_index = 0
hero = hero_images[hero_img_index]
hero_rect = hero.get_rect()                                 # получаем размеры и положение поверхности "героя"
hero_rect = hero_rect.move(hero_attr["x"], hero_attr["y"])  # смещаем поверхность "героя" на середину рабочего окна

back_ground = pygame.transform.scale(pygame.image.load('image/background.png').convert(), screen_size)    # создаём поверхность "бекгроунд" и загружаем на неё изображение
back_ground_speed = 2
back_ground_dx1 = 0         # исходное смещение 1-го фонового изображения 
back_ground_dx2 = WIDTH     # исходное смещение 2-го фонового изображения 

enemy_size = (70, 25)      # размер изображения "врага" (ширина, высота) 
bildings_heights =  HEIGHT - HEIGHT // 3    # высота неба над уровнем зданий

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('image/enemy.png').convert_alpha(), enemy_size)    # создаём поверхность "врага" и загружаем на неё изображение
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, bildings_heights), *enemy.get_size())
    enemy_speed = random.randint(2, 5)                  # создаём произвольную скорость "врага"
    return [enemy, enemy_rect, enemy_speed]             # возвращяем данные очередного "врага"

def create_bonus():
    bonus_size = (50, 83)                               # создаём размер поверхности "бонуса"
    bonus = pygame.transform.scale(pygame.image.load('image/bonus.png').convert_alpha(), bonus_size)    # создаём поверхность "бонуса" и загружаем на неё изображение
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)                  # создаём произвольную скорость "бонуса"
    print(f'There are {len(bonuses)} bonuses. Created a new bonus')
    return [bonus, bonus_rect, bonus_speed]             # возвращяем данные очередного "бонуса"

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)               # установка таймера вызова функции сосздания нового "врага", 1500 мс

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)               # установка таймера вызова функции сосздания нового "бонуса", 2000 мс

CHANGE_IMG_HERO = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG_HERO, 125)               # установка таймера вызова функции смены изображения "героя", 125 мс

enemies = []
bonuses = []
score = 0           # количество пойманных "бонусов"
score_fall = 0      # количество пропущенных "бонусов"
score_damage = 0    # количество сбитых "бонусов"
font_score = pygame.font.SysFont('Verdana', 20)         # устанавливаем шрифт и размер текста (px) для отображения "бонуса"
font_game_over = pygame.font.SysFont('Verdana', 40)         # устанавливаем шрифт и размер текста (px) для отображения "Game Over"
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

        if event.type == CHANGE_IMG_HERO:          # если появилось событие создать "бонус"
            hero_img_index += 1 
            if hero_img_index == len(hero_images):
                hero_img_index = 0
            hero = hero_images[hero_img_index]

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

    back_ground_dx1 -= back_ground_speed
    back_ground_dx2 -= back_ground_speed
    if back_ground_dx1 < -back_ground.get_width():
        back_ground_dx1 = back_ground.get_width()
    if back_ground_dx2 < -back_ground.get_width():
        back_ground_dx2 = back_ground.get_width()

    main_surface.blit(back_ground, (back_ground_dx1, 0))        # накладываем поверность "бэкгроунд" №1 на основную поверхность "фон"
    main_surface.blit(back_ground, (back_ground_dx2, 0))        # накладываем поверность "бэкгроунд" №2 на основную поверхность "фон"    
    main_surface.blit(hero, hero_rect)                          # накладываем поверность "героя" на основную поверхность "фон"

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        if enemy[1].left < 0:                   # если поверхность "врага" ушла за левый край рабочего окна
            enemies.pop(enemies.index(enemy))   # удаляем "врага" из списка "врагов"
            print(f'There are {len(enemies)} enemies. Delete one old enemy.')
        else:                                       # иначе
            main_surface.blit(enemy[0], enemy[1])   # накладываем поверхность "врага" на основную поверхность "фон"

        for bonus in bonuses:
            if (enemy[1]).colliderect(bonus[1]):         # если плоскость "героя" пересеклась с плоскостью "бонус"
                bonuses.pop(bonuses.index(bonus))       # удаляем "бонус" из списка "бонусов"
                score_damage += 1
                # print(f'There are {len(bonuses)} bonuses. Delete one old bonus. Score = {score}')
        
        if hero_rect.colliderect(enemy[1]):         # если плоскость "героя" пересеклась с плоскостью "врага"
            game_over = True                        # устанавливаем флаг "конец игры", выход из основного цикла
            print(f'Игра окнчена. Ваш "герой" погиб. Вы набрали {score} очков.')

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        if bonus[1].bottom > bildings_heights:          # если поверхность "бонус" ушла за нижний край рабочего окна
            bonuses.pop(bonuses.index(bonus))           # удаляем "бонус" из списка "бонусов"
            score_fall +=1
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus.')
        else:                                       # иначе
            main_surface.blit(bonus[0], bonus[1])   # накладываем поверхность "врага" на основную поверхность "фон"

        if hero_rect.colliderect(bonus[1]):         # если плоскость "героя" пересеклась с плоскостью "бонус"
            bonuses.pop(bonuses.index(bonus))       # удаляем "бонус" из списка "бонусов"
            score += 1
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus. Score = {score}')



    main_surface.blit(font_score.render('Бонуси: '+str(score), True, RED), (50, 0))  # накладываем поверность "текст" на основную поверхность "фон"
    main_surface.blit(font_score.render('Збито: '+str(score_damage), True, RED), (275, 0))  # накладываем поверность "текст" на основную поверхность "фон"
    main_surface.blit(font_score.render('Пропущено: '+str(score_fall), True, RED), (500, 0))  # накладываем поверность "текст" на основную поверхность "фон"

    pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
    clock.tick(FPS)                     # вызывааем метод tick() класса Clock(), устанавливаем задержку для цикла, FPS
                                        # FPS раз в секунду с учётом времени на выполнение операций в самом цикле

main_surface.blit(font_game_over.render('Гусю капець. Ігрі кінець.', True, RED), (WIDTH/2-250, HEIGHT/2-20))  # накладываем поверность "текст" на основную поверхность "фон"
pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
time.sleep(3)
pygame.quit()  # выход из модуля pygame
quit()
