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

class Balon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("balon.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        self.velocidad = [0.45, -0.3]

    def actualizar(self, time, fichas1, fichas2):#, pala_jug):
        self.rect.centerx += self.velocidad[0] * time
        self.rect.centery += self.velocidad[1] * time
        if self.rect.left <= 39 or self.rect.right >= 761:
            self.velocidad[0] = -self.velocidad[0]
            self.rect.centerx += self.velocidad[0] * time
        if self.rect.top <= 114 or self.rect.bottom >= 442:
            self.velocidad[1] = -self.velocidad[1]
            self.rect.centery += self.velocidad[1] * time

        for ficha in (fichas1.fichas + fichas2.fichas):
            if pygame.sprite.collide_rect(self, ficha):
                if ficha.dir == "der":
                    self.velocidad[0] = abs(self.velocidad[0])
                if ficha.dir == "izq":
                    self.velocidad[0] = -1*abs(self.velocidad[0])
                self.rect.centerx += self.velocidad[0] * time
                ficha.bol = 1
                if ficha in fichas1.fichas:
                    for fich in ficha.com:
                        fichas1.fichas[fich].bol = 1
                elif ficha in fichas2.fichas:
                    for fich in ficha.com:
                        fichas2.fichas[fich].bol = 1

class Ficha(pygame.sprite.Sprite):
    def __init__(self, img, pos, lim, dirt, com=[]):
        pygame.sprite.Sprite.__init__(self)
        self.image = [load_image(img[0]),
                      load_image(img[1]),
                      load_image(img[2])]
        self.rect = self.image[0].get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.limSup = lim[0]
        self.limInf = lim[1]
        self.dir = dirt
        self.bol = 0
        self.com = com # Compañeros de linea

    def __str__(self):
        return str(self.rect)

class Fichas(object):
    def __init__(self, img, jug=1):
        # jug es el tipo de jugador
        # 1 -> Jugador principal
        # 2 -> Maquina
        # 3 -> Jugador 2
        self.speed = 0.5
        if jug == 1:
            self.jug = 1
            # Crear arreglo de los rects
            self.fichas = [Ficha(img, (50, 259), (197, 326), "der"),
                          Ficha(img, (146, 173), (114, 240), "der", [2]),
                          Ficha(img, (146, 347), (288, 414), "der", [1]),
                          Ficha(img, (338, 135), (114, 158), "der", [4, 5, 6]),
                          Ficha(img, (338, 222), (201, 245), "der", [3, 5, 6]),
                          Ficha(img, (338, 306), (285, 329), "der", [3, 4, 6]),
                          Ficha(img, (338, 391), (370, 414), "der", [3, 4, 5]),
                          Ficha(img, (530, 163), (114, 211), "der", [7, 8]),
                          Ficha(img, (530, 262), (213, 310), "der", [6, 8]),
                          Ficha(img, (530, 366), (317, 414), "der", [6, 7])
                         ]
        else:
            self.jug = jug
            # Crear arreglo de los rects
            self.fichas = [Ficha(img, (727, 258), (197, 326), "izq"),
                           Ficha(img, (631, 133), (114, 240), "izq", [2]),
                           Ficha(img, (631, 345), (288, 414), "izq", [1]),
                           Ficha(img, (432, 133), (114, 158), "izq", [4, 5, 6]),
                           Ficha(img, (432, 218), (201, 245), "izq", [3, 5, 6]),
                           Ficha(img, (432, 303), (285, 329), "izq", [3, 4, 6]),
                           Ficha(img, (432, 389), (370, 414), "izq", [3, 4, 5]),
                           Ficha(img, (241, 161), (114, 211), "izq", [7, 8]),
                           Ficha(img, (241, 264), (213, 310), "izq", [6, 8]),
                           Ficha(img, (241, 364), (317, 414), "izq", [6, 7])
                         ]

    def mover(self, time, keys, bola=None):
        if self.jug == 1:
            if keys[K_w]:
                for ficha in self.fichas:
                    top = ficha.limSup
                    if ficha.rect.top > top:
                        if ficha.rect.y - self.speed * time <= 114:
                            ficha.rect.y = 114
                        else:
                            ficha.rect.y -= self.speed * time
            if keys[K_s]:
                for ficha in self.fichas:
                    top = ficha.limInf
                    if ficha.rect.top < top:
                        if ficha.rect.y + self.speed * time >= 414:
                            ficha.rect.y = 414
                        else:
                            ficha.rect.y += self.speed * time
        elif self.jug == 2:
            # Verifica que la bola este en un sector de la cancha
            cond1 = bola.rect.x >=111 and bola.rect.x <= 251    # Delanteros
            cond2 = bola.rect.x >= 402 and bola.rect.x <= 442   # Volantes
            cond3 = bola.rect.x >= 601 and bola.rect.x <= 641   # Defensas
            cond3 = bola.rect.x >= 687                          # Portero
            if cond1 or cond2 or cond2 or cond3:
                # Comprobar direccion
                if bola.velocidad[1] > 0: # Hacia arriba
                    for ficha in self.fichas:
                        top = ficha.limSup
                        if ficha.rect.top > top:
                            if ficha.rect.y - self.speed * time <= 114:
                                ficha.rect.y = 114
                            else:
                                ficha.rect.y -= self.speed * time
                elif bola.velocidad[1] <= 0: # Hacia abajo
                    for ficha in self.fichas:
                        top = ficha.limInf
                        if ficha.rect.top < top:
                            if ficha.rect.y + self.speed * time >= 414:
                                ficha.rect.y = 414
                            else:
                                ficha.rect.y += self.speed * time

        elif self.jug == 3:
            if keys[K_UP]:
                for ficha in self.fichas:
                    top = ficha.limSup
                    if ficha.rect.top > top:
                        if ficha.rect.y - self.speed * time <= 114:
                            ficha.rect.y = 114
                        else:
                            ficha.rect.y -= self.speed * time
            if keys[K_DOWN]:
                for ficha in self.fichas:
                    top = ficha.limInf
                    if ficha.rect.top < top:
                        if ficha.rect.y + self.speed * time >= 414:
                            ficha.rect.y = 414
                        else:
                            ficha.rect.y += self.speed * time

    def pintar(self, screen, clock):
        for ficha in self.fichas:
            screen.blit(ficha.image[ficha.bol], ficha.rect)
            if ficha.bol == 1:
                ficha.bol = 2
            elif ficha.bol == 2:
                ficha.bol = 0

class Marcador(object):
    def __init__(self):
        pass

def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image


class Tablero(object):
    def __init__(self):
        self.screen = pygame.display.set_mode([ANCHO,ALTO])
        self.W = ANCHO
        self.H = ALTO
        self.marcador = [0, 0]

    # Metodo para pintar tablero
    def pintar(self):
        # PARTE SUPERIOR DEL TABLERO
        pygame.draw.rect(self.screen, (125, 73, 33), (0, 0, self.W, self.H))

        # BORDES EXTERNOS DE LA MESA
        c = pygame.draw.rect(self.screen, (89, 87, 87), (0, 74, self.W, 29))
        pygame.draw.rect(self.screen, (89, 87, 87), (0,103, 21, 350))
        pygame.draw.rect(self.screen, (89, 87, 87), (0,453, self.W, 30))
        pygame.draw.rect(self.screen, (89, 87, 87), (779,103, 21, 350))

        # BORDES INTERNOS DE LA MESA
        pygame.draw.rect(self.screen, (48, 47, 47), (21,103, 758, 11))
        pygame.draw.rect(self.screen, (48, 47, 47), (21, 442, 758, 11))
        pygame.draw.rect(self.screen, (48, 47, 47), (21, 103, 18, 350))
        pygame.draw.rect(self.screen, (48, 47, 47), (761, 103, 18, 350))

        # COLOR DEL CESPED
        pygame.draw.rect(self.screen, (32, 120, 20), (21, 198, 18, 154))
        pygame.draw.rect(self.screen, (32, 120, 20), (761, 198, 18, 154))
        pygame.draw.rect(self.screen, (42, 156, 26), (39, 114, 722, 328))

        # RAYAS BLANCAS DEL CAMPO
        pygame.draw.rect(self.screen, (255, 255, 255), (39, 114, 722, 328), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (39, 114, 361, 328), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (39, 198, 52, 154), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (709, 198, 52, 154), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (39, 178, 89, 194), 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (672, 178, 89, 194), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (400, 275), 87, 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (400, 275), 7)

if __name__ == '__main__':
    pygame.init()
    tablero = Tablero()
    # Mouse invisible
    pygame.mouse.set_visible(False)
    terminar = False
    bola = Balon()
    imgA = ["img/jugador/11.png",
            "img/jugador/12.png",
            "img/jugador/13.png"]
    imgB = ["img/jugador/21.png",
            "img/jugador/22.png",
            "img/jugador/23.png"]
    fichasA = Fichas(imgA)
    fichasB = Fichas(imgB, 2)
    clock = pygame.time.Clock()

    while not terminar:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        bola.actualizar(time, fichasA, fichasB)#, pala_jug)
        fichasA.mover(time, keys, bola)
        if fichasB.jug == 2:
            fichasB.mover(time, keys, bola)
        elif fichasB.jug == 3:
            fichasB.mover(time, keys)

        tablero.pintar()
        tablero.screen.blit(bola.image, bola.rect)
        fichasA.pintar(tablero.screen, clock)
        fichasB.pintar(tablero.screen, clock)
        clock.tick(50)
        pygame.display.flip()
