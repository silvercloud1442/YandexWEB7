import os
import sys
import pygame
import requests

response = None

map_api_server = "http://static-maps.yandex.ru/1.x/"

map_param = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "ll": ','.join(['44.688571', '43.027601']),
    "spn": ','.join(['0.001', '0.001']),
    "l": "map"
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

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
