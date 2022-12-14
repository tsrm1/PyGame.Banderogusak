""" Игра Бандерогусак, анимация фона, героя, бонусов и врагов
"""
import random                           # импортируем библиотеку random
import time                             # импортируем библиотеку time  (time.sleep(3))
from os import listdir                  # импортируем метод listdir
import pygame                           # импортируем библиотеку pygame
import spritesheet                      # импортируем библиотеку spritesheet (создали отдельно, находиться в той же папке)
pygame.init()                           # инициализируем/вызываем библиотеку pygame
screen_size = WIDTH, HEIGHT = 1920, 1080  # ширина и высота окна
main_surface = pygame.display.set_mode((screen_size), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN) # создаём поверхность отрисовки
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
BLACK = (0, 0, 0)               # цвет чёрный
# WHITE = (255, 255, 255)         # цвет белый
# GRAY = (128, 128, 128)          # цвет серый
# YELLOW = (255, 255, 0)          # цвет жёлтый
# PINK = (255, 0, 255)            # цвет розовый
# VIOLET = (0, 255, 255)          # цвет фиолетовый

hero_attr = {                   # hero position. положение "героя"
    # "x": WIDTH/2,               # начальное положение "героя", координата X
    # "y": HEIGHT/2,              # начальное положение "героя", координата Y
    "image": pygame.transform.scale(pygame.image.load('image/Goose/1-1.png').convert_alpha(), (100, 30)),   # создаём поверхность "героя" и загружаем на неё изображение
    "image_numer": 0,
    "live": True,                # статус "героя". Он жив (True) или он взрывается (False)
    "size": (100, 30),          # размер изображения "героя" (ширина, высота)
    "speed": 5,                 # смещение "героя" по координате X или Y
}

IMG_PATH = 'image/Goose'
hero_images = [pygame.transform.scale(pygame.image.load(IMG_PATH + '/' + file ).convert_alpha(), hero_attr["size"]) for file in listdir(IMG_PATH)]
#hero = pygame.transform.scale(pygame.image.load('image/Goose/1-1.png').convert_alpha(), hero_attr["size"])   # создаём поверхность "героя" и загружаем на неё изображение
#hero_img_index = 0
hero_attr["image_numer"] = 0
#hero = hero_images[hero_img_index]
hero = hero_images[hero_attr["image_numer"]]

hero_rect = hero.get_rect()                                 # получаем размеры и положение поверхности "героя"
hero_rect = hero_rect.move(WIDTH/2, HEIGHT/2)  # смещаем поверхность "героя" на середину рабочего окна
# hero_rect = hero_rect.move(hero_attr["x"], hero_attr["y"])  # смещаем поверхность "героя" на середину рабочего окна

back_ground = pygame.transform.scale(pygame.image.load('image/background.png').convert(), screen_size)    # создаём поверхность "бекгроунд" и загружаем на неё изображение
back_ground_speed = 2
back_ground_dx1 = 0         # исходное смещение 1-го фонового изображения 
back_ground_dx2 = WIDTH     # исходное смещение 2-го фонового изображения 


bildings_heights =  HEIGHT - HEIGHT // 3    # высота неба над уровнем зданий

# def create_enemy():
#     enemy = pygame.transform.scale(pygame.image.load('image/enemy.png').convert_alpha(), enemy_size)    # создаём поверхность "врага" и загружаем на неё изображение
#     enemy_rect = pygame.Rect(WIDTH, random.randint(0, bildings_heights), *enemy.get_size())
#     enemy_speed = random.randint(4, 10)                  # создаём произвольную скорость "врага"
#     return [enemy, enemy_rect, enemy_speed]             # возвращяем данные очередного "врага"

def create_enemy():
    enemy_size = (70, 25)      # размер изображения "врага" (ширина, высота) 
    img = pygame.image.load('image/enemy.png').convert_alpha()
    enemy1 = {
        "image": pygame.transform.scale(img, enemy_size),    # создаём поверхность "врага" и загружаем на неё изображение
        "rect": pygame.Rect(WIDTH, random.randint(0, bildings_heights), *img.get_size()),
        "speed": random.randint(4, 10),                  # создаём произвольную скорость "врага"
        "img_numer": 0,
    }
    print(f'There are {len(enemies)+1} enemies. Created a new enemy.')    
    return enemy1             # возвращяем данные очередного "врага"

def create_explode(version, center):
    if version: 
        explode_size = (192, 192)                               # создаём размер поверхности "взрыва"
        explode = {
            #"image": pygame.transform.scale(img, enemy_size),    # создаём поверхность "врага" и загружаем на неё изображение
            "rect": pygame.Rect(center, explode_size),
            "speed": 3,                                          # создаём произвольную скорость смещения "взрыва"
            "img_numer": 0,
            "img_numer_max": 20,
        }
    # else:
    #     explode_size = (192, 192)                               # создаём размер поверхности "взрыва"
    #     explode = {
    #         #"image": pygame.transform.scale(img, enemy_size),    # создаём поверхность "врага" и загружаем на неё изображение
    #         "rect": pygame.Rect(center, explode_size),
    #         #"speed": random.randint(4, 10),                  # создаём произвольную скорость "взрыва"
    #         "img_numer": 0,
    #         "img_numer_max": 20,
    #     }
    print(f'There are {len(explosions)+1} explosions. Created a new explode.', explode)  
    return explode            # возвращяем данные очередного "взрыва"

explosions = []

def create_bonus():
    bonus_size = (50, 83)                               # создаём размер поверхности "бонуса"
    bonus = {
        "image": pygame.transform.scale(pygame.image.load('image/bonus.png').convert_alpha(), bonus_size),    # создаём поверхность "бонуса" и загружаем на неё изображение
        "rect": pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size),
        "speed": random.randint(2, 5),                  # создаём произвольную скорость "бонуса"
        "img_numer": 0,      
    }
    print(f'There are {len(bonuses)+1} bonuses. Created a new bonus.')
    return bonus             # возвращяем данные очередного "бонуса"
    

def change_image_explosions():
    for explode in explosions:
        if explode["img_numer"] < explode["img_numer_max"]:
            explode["img_numer"] +=1
            print(f'Explode {explode} moved to {explode["img_numer"]}')
        else:
            explosions.pop(explosions.index(explode))       # удаляем "взрыв" из списка "взрывов"
            print(f'There are {len(explosions)} explosions. Delete one old explode.')
    print("change_image_explosions ", len(explosions))

sprite_sheet_image_explotion_hero = pygame.image.load('image/sprite-explosion-48p-255x255.png').convert_alpha()
sprite_sheet_hero_explotion = spritesheet.SpriteSheet(sprite_sheet_image_explotion_hero)
hero_explotion_frames = sprite_sheet_hero_explotion.strip_from_sheet(8, 6, 256, 256, 1)   # (col_row, col_span, width, height, scale, colour=(0, 0, 0))
hero_explotion_frame_numer = 0

sprite_sheet_image_explotion_bonus = pygame.image.load('image/sprite-explosion-20p-192x192.png').convert_alpha()
sprite_sheet_bonus_explotion = spritesheet.SpriteSheet(sprite_sheet_image_explotion_bonus)
bonus_explotion_frames = sprite_sheet_bonus_explotion.strip_from_sheet(5, 4, 192, 192, 1)   # (col_row, col_span, width, height, scale, colour=(0, 0, 0))

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)               # установка таймера вызова функции сосздания нового "врага", 1500 мс

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)               # установка таймера вызова функции сосздания нового "бонуса", 2000 мс

CHANGE_IMG_HERO = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG_HERO, 125)               # установка таймера вызова функции смены изображения "героя", 125 мс

CHANGE_IMG_EXPLODE = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGE_IMG_EXPLODE, 100)               # установка таймера вызова функции смены изображения "взрыва", 125 мс



enemies = []
bonuses = []
score = 0           # количество пойманных "бонусов"
score_fall = 0      # количество пропущенных "бонусов"
score_damage = 0    # количество сбитых "бонусов"
font_score = pygame.font.SysFont('Verdana', 20)         # устанавливаем шрифт и размер текста (px) для отображения "бонуса"
font_game_over = pygame.font.SysFont('Verdana', 40)         # устанавливаем шрифт и размер текста (px) для отображения "Game Over"
# SysFont(name, size, bold=False, italic=False)

# start game loop
hero_attr["live"] = True                        # флаг "герой жив", "герой умирает"
game_over = False                               # флаг "конец игры", игра закончилась
while not game_over:                            # start game loop
    for event in pygame.event.get():            # переменная event принимает значение сообщений из очереди событий pygame.event.
        if event.type == pygame.QUIT:           # проверяем ТИП события event, равно ли QUIT (нажата ли иконка закрытия рабочего окна)
            game_over = True                    # выход из основного цикла

        if event.type == CREATE_ENEMY:          # если появилось событие создать "врага"
            enemies.append(create_enemy())      # в список "врагов" добавляем нового "врага"

        if event.type == CREATE_BONUS:          # если появилось событие создать "бонус"
            bonuses.append(create_bonus())      # в список "врагов" добавляем новый "бонус"

        if event.type == CHANGE_IMG_EXPLODE:          # если появилось событие создать "бонус"
            change_image_explosions()      # в список "врагов" добавляем новый "бонус"

        if event.type == CHANGE_IMG_HERO:           # если появилось событие изменить изображение "героя"
            hero_attr["image_numer"] += 1                     # увеличиваем счётчик номера изображения "героя"
            if hero_attr["image_numer"] == len(hero_images):  # если достигли последнего изображения в списке изображений "героя",
                hero_attr["image_numer"] = 0                  # устанавливаем текущим самое первое изображение в списке изображений "героя"
            hero = hero_images[hero_attr["image_numer"]]      # присваиваем "герою" текущее изображение

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

    back_ground_dx1 -= back_ground_speed                        # ументшаем координату X 1-го фонового  изображения на величну back_ground_speed
    back_ground_dx2 -= back_ground_speed                        # ументшаем координату X 2-го фонового  изображения на величну back_ground_speed
    if back_ground_dx1 < -back_ground.get_width():              # обнуляем смещение 1-го фонового изображения на ширину фонового изображения
        back_ground_dx1 = back_ground.get_width()
    if back_ground_dx2 < -back_ground.get_width():              # обнуляем смещение 2-го фонового изображения на ширину фонового изображения
        back_ground_dx2 = back_ground.get_width()

    main_surface.blit(back_ground, (back_ground_dx1, 0))        # накладываем поверность "бэкгроунд" №1 на основную поверхность "фон"
    main_surface.blit(back_ground, (back_ground_dx2, 0))        # накладываем поверность "бэкгроунд" №2 на основную поверхность "фон"    
    
    if hero_attr["live"]:
        main_surface.blit(hero, hero_rect)                          # накладываем поверность "героя" на основную поверхность "фон"
    else:
        main_surface.blit(hero_explotion_frames[hero_explotion_frame_numer], hero_rect)
        hero_explotion_frame_numer +=1
        if hero_explotion_frame_numer >=48: game_over = True

    for enemy in enemies:
        enemy["rect"] = enemy["rect"].move(-enemy["speed"], 0)  # свдивгаем поверхность текущего "врага" влево на величину enemy_speed
        if enemy["rect"].left < 0:                   # если поверхность "врага" ушла за левый край рабочего окна
            enemies.pop(enemies.index(enemy))   # удаляем "врага" из списка "врагов"
            print(f'There are {len(enemies)} enemies. Delete one old enemy.')
        else:                                       # иначе
            main_surface.blit(enemy["image"], enemy["rect"])   # накладываем поверхность "врага" на основную поверхность "фон"

        for bonus in bonuses:
            if (enemy["rect"]).colliderect(bonus["rect"]):        # если плоскость "героя" пересеклась с плоскостью "бонус"
                explosions.append(create_explode(1, bonus["rect"].center))
                print("запрос на создание взрыва в точке ", bonus["rect"].center)
                bonuses.pop(bonuses.index(bonus))       # удаляем "бонус" из списка "бонусов"
                enemies.pop(enemies.index(enemy))       # удаляем "врага" из списка "врогов"
                score_damage += 1                       # увеличиваем счётчик сбитых "бонусов"
                # print(f'There are {len(bonuses)} bonuses. Delete one old bonus. Score = {score}')
        
        if hero_rect.colliderect(enemy["rect"]):         # если плоскость "героя" пересеклась с плоскостью "врага"
            #fire_rect = fire_rect.move(hero_rect.get_rect(x), hero_rect.get_rect(y))
            hero_attr["live"] = False                        # устанавливаем флаг "конец игры", выход из основного цикла
            enemies.pop(enemies.index(enemy))       # удаляем "врага" из списка "врагов"
            print(f'Игра окнчена. Ваш "герой" погиб. Вы набрали {score} очков.')

    for bonus in bonuses:
        bonus["rect"] = bonus["rect"].move(0, bonus["speed"])           # сдвигаем поверхность "бонус" вниз на bonus_speed px
        if bonus["rect"].bottom > bildings_heights:          # если поверхность "бонус" ушла за нижний край рабочего окна
            bonuses.pop(bonuses.index(bonus))           # удаляем "бонус" из списка "бонусов"
            score_fall +=1                              # увеличиваем счётчик пропущенных "бонусов"
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus.')
        else:                                       # иначе
            main_surface.blit(bonus["image"], bonus["rect"])   # накладываем поверхность "врага" на основную поверхность "фон"

        if hero_rect.colliderect(bonus["rect"]) and hero_attr["live"]:         # если плоскость "героя" пересеклась с плоскостью "бонус"
            bonuses.pop(bonuses.index(bonus))       # удаляем "бонус" из списка "бонусов"
            score += 1                              # увеличиваем счётчик пойманных "бонусов"
            print(f'There are {len(bonuses)} bonuses. Delete one old bonus. Score = {score}')
        
    for explode in explosions:
        explode["rect"] = explode["rect"].move( -explode["speed"], 0)           # сдвигаем поверхность "взрыва" влево на explode_speed px
        if explode["img_numer"] < explode["img_numer_max"]:
            explode["image"] = bonus_explotion_frames[explode["img_numer"]]
            main_surface.blit(explode["image"], explode["rect"])   # накладываем поверхность "взрыва" на основную поверхность "фон"          
        else: pass
            

    main_surface.blit(font_score.render('Бонуси: '+str(score), True, RED), (50, 0))  # накладываем поверность "текст" на основную поверхность "фон"
    main_surface.blit(font_score.render('Збито: '+str(score_damage), True, RED), (275, 0))  # накладываем поверность "текст" на основную поверхность "фон"
    main_surface.blit(font_score.render('Пропущено: '+str(score_fall), True, RED), (500, 0))  # накладываем поверность "текст" на основную поверхность "фон"

    pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
    clock.tick(FPS)                     # вызывааем метод tick() класса Clock(), устанавливаем задержку для цикла, FPS
                                        # FPS раз в секунду с учётом времени на выполнение операций в самом цикле

main_surface.blit(font_game_over.render('Гусаку капець. Грі кінець.', True, RED), (WIDTH/2-250, HEIGHT/2-20))  # накладываем поверность "текст" на основную поверхность "фон"
pygame.display.update()             # вывод прямоугольной области (списка областей) из буфера
time.sleep(3)                       # устанавливаем задержку на 3 секунды
pygame.quit()                       # выход из модуля pygame
quit()                              # выход из программы
