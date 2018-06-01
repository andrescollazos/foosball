# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
import sys
import random

ANCHO = 800
ALTO = 600
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE1 = (8, 71, 10)
VERDE2 = (14, 132, 18)
VERDE = [VERDE1, VERDE2]

# PINTAR EL TABLERO DE JUEGO
def tablero(screen, num_lineas):
    W = ANCHO
    H = ALTO

    # PARTE SUPERIOR DEL TABLERO
    pygame.draw.rect(screen, (125, 73, 33), (0, 0, W, H))

    # BORDES EXTERNOS DE LA MESA
    pygame.draw.rect(screen, (89, 87, 87), (0, 74, W, 29))
    pygame.draw.rect(screen, (89, 87, 87), (0,103, 21, 350))
    pygame.draw.rect(screen, (89, 87, 87), (0,453, W, 30))
    pygame.draw.rect(screen, (89, 87, 87), (779,103, 21, 350))

    # BORDES INTERNOS DE LA MESA
    pygame.draw.rect(screen, (48, 47, 47), (21,103, 758, 11))
    pygame.draw.rect(screen, (48, 47, 47), (21, 442, 758, 11))
    pygame.draw.rect(screen, (48, 47, 47), (21, 103, 18, 350))
    pygame.draw.rect(screen, (48, 47, 47), (761, 103, 18, 350))

    # COLOR DEL CESPED
    pygame.draw.rect(screen, (32, 120, 20), (21, 198, 18, 154))
    pygame.draw.rect(screen, (32, 120, 20), (761, 198, 18, 154))
    pygame.draw.rect(screen, (42, 156, 26), (39, 114, 722, 328))

    # RAYAS BLANCAS DEL CAMPO
    pygame.draw.rect(screen, (255, 255, 255), (39, 114, 722, 328), 2)
    pygame.draw.rect(screen, (255, 255, 255), (39, 114, 361, 328), 2)
    pygame.draw.rect(screen, (255, 255, 255), (39, 198, 52, 154), 2)
    pygame.draw.rect(screen, (255, 255, 255), (709, 198, 52, 154), 2)
    pygame.draw.rect(screen, (255, 255, 255), (39, 178, 89, 194), 2)
    pygame.draw.rect(screen, (255, 255, 255), (672, 178, 89, 194), 2)
    pygame.draw.circle(screen, (255, 255, 255), (400, 275), 97, 2)
    pygame.draw.circle(screen, (255, 255, 255), (400, 275), 7)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([ANCHO,ALTO])
    # Mouse invisible
    pygame.mouse.set_visible(False)
    terminar = False
    reloj = pygame.time.Clock()

    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        tablero(screen, 12)
        pygame.display.flip()
