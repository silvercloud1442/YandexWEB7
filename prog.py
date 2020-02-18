#Добавил смену слоёв и смещение карты

import os
import sys
import pygame
import requests

font_name = pygame.font.match_font('arial')
sl = 'sh'
map_file = ''
spn = 0.001
ll = [44.688571, 43.027601]
L = 'map'


def map(spn, ll, L):
    global map_file

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_param = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "ll": ','.join([str(ll[0]), str(ll[1])]),
        "spn": ','.join([str(spn), str(spn)]),
        "l": L
    }

    response = requests.get(map_api_server, params=map_param)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def Downplay():
    global spn
    spn += 0.002
    map(spn, ll, L)


def Increase():
    global spn
    spn -= 0.002
    if spn < 0.001:
        spn = 0.001
    map(spn, ll, L)


# Смена слоя на: схема
def LayerMap():
    global sl, L
    sl = 'sh'
    L = 'map'
    map(spn, ll, L)


# Смена слоя на: спутник
def LayerSatellite():
    global sl, L
    sl = 'sp'
    L = 'sat'
    map(spn, ll, L)


# Смена слоя на: гибрид
def LayerHybrid():
    global sl, L
    sl = 'gb'
    L = 'sat,skl'
    map(spn, ll, L)


# Смешение центра карты вверх
def MapUp():
    global ll, spn
    ll[1] += spn / 2
    map(spn, ll, L)


# Смешение центра карты вниз
def MapDown():
    global ll, spn
    ll[1] -= spn / 2
    map(spn, ll, L)


# Смешение центра карты влево
def MapLeft():
    global ll, spn
    ll[0] -= spn / 2
    map(spn, ll, L)


# Смешение центра карты вправо
def MapRigt():
    global ll, spn
    ll[0] += spn / 2
    map(spn, ll, L)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


map(spn, ll, L)
pygame.init()
screen = pygame.display.set_mode((700, 700))
run = True
while run:
    butDownplay = pygame.Rect((100, 40, 200, 50))
    butIncrease = pygame.Rect((400, 40, 200, 50))
    butMap = pygame.Rect((310, 35, 80, 20))
    butSatellite = pygame.Rect((310, 60, 80, 20))
    butHybrid = pygame.Rect((310, 85, 80, 20))
    pygame.draw.rect(screen, (0, 0, 255), (100, 40, 200, 50))
    pygame.draw.rect(screen, (0, 0, 255), (400, 40, 200, 50))
    if sl == 'sh':
        pygame.draw.rect(screen, (0, 255, 0), (310, 35, 80, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (310, 35, 80, 20))
    if sl == 'sp':
        pygame.draw.rect(screen, (0, 255, 0), (310, 60, 80, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (310, 60, 80, 20))
    if sl == 'gb':
        pygame.draw.rect(screen, (0, 255, 0), (310, 85, 80, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (310, 85, 80, 20))
    draw_text(screen, "-", 18, 200, 55)
    draw_text(screen, "+", 18, 500, 55)
    draw_text(screen, "СХЕМА", 18, 350, 35)
    draw_text(screen, "СПУТНИК", 18, 350, 60)
    draw_text(screen, "ГИБРИД", 18, 350, 85)
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
        if event.type == 5:
            if butDownplay.collidepoint(x, y):
                Downplay()
            if butIncrease.collidepoint(x, y):
                Increase()
            if butMap.collidepoint(x, y):
                LayerMap()
            if butSatellite.collidepoint(x, y):
                LayerSatellite()
            if butHybrid.collidepoint(x, y):
                LayerHybrid()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                Downplay()
            if event.key == pygame.K_PAGEDOWN:
                Increase()
            if event.key == pygame.K_UP:
                MapUp()
            if event.key == pygame.K_DOWN:
                MapDown()
            if event.key == pygame.K_RIGHT:
                MapRigt()
            if event.key == pygame.K_LEFT:
                MapLeft()

    screen.blit(pygame.image.load(map_file), (50, 150))
    pygame.display.flip()

os.remove(map_file)
