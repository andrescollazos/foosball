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
GRIS = (162, 162, 162)
VERDE1 = (8, 71, 10)
VERDE2 = (14, 132, 18)
VERDE = [VERDE1, VERDE2]
pygame.init()

EQUIPOS = {
            "clubes": ["nacional", "dim", "santafe", "america", "millonarios", "cali", "junior", "tolima",
                       "cali", "bucaramanga", "huila", "caldas", "pasto", "boyaca", "aguilas", "patriotas",
                       "envigado", "cortulua", "jaguares", "random"],
            "selecciones": ["colombia", "brasil", "argentina", "uruguay", "paraguay", "venezuela", "chile", "ecuador", "bolivia", "peru"]
          }

# Devuelve el tipo de equipo
def tipo_equipo(equipo):
    if equipo in EQUIPOS["clubes"]:
        return "/clubes/"
    if equipo in EQUIPOS["selecciones"]:
        return "/selecciones/"

class Balon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("img/balon.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        self.velocidad = [0.45, -0.3]

    def actualizar(self, time, fichas1, fichas2, marcador):
        self.rect.centerx += self.velocidad[0] * time
        self.rect.centery += self.velocidad[1] * time

        # Verificar si anota gol
        # Equipo 1
        if self.rect.x >= 21 and self.rect.x <= 39 and self.rect.y >= 198 and self.rect.y <= 352:
            marcador.resultado[1] = marcador.resultado[1] + 1
            marcador.gol = [True, 1]
            print("Gol")
            return -1
            #print("GOOOL")
        else:
            if self.rect.x >= (761 - 22) and self.rect.x <= (776 - 20) and self.rect.y >= 198 and self.rect.y <= 352:
                marcador.resultado[0] = marcador.resultado[0] + 1
                marcador.gol = [True, 0]
                print("Gol")
                return -1
                #print("GOOOL")

        if self.rect.left <= 38 or self.rect.right >= 761:
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
    def __init__(self, equipo, img, jug=1):
        self.equipo = equipo
        # jug es el tipo de jugador
        # 1 -> Jugador principal
        # 2 -> Maquina
        # 3 -> Jugador 2
        self.speed = 0.5
        self.acts = []
        if jug == 1:
            self.jug = 1
            # Crear arreglo de los rects
            self.fichas = [
                          Ficha(img, (50, 259), (197, 326), "der"),
                          Ficha(img, (146, 173), (114, 240), "der", [2]),
                          Ficha(img, (146, 347), (288, 414), "der", [1]),
                          Ficha(img, (338, 135), (114, 158), "der", [4, 5, 6]),
                          Ficha(img, (338, 222), (201, 245), "der", [3, 5, 6]),
                          Ficha(img, (338, 306), (285, 329), "der", [3, 4, 6]),
                          Ficha(img, (338, 391), (370, 414), "der", [3, 4, 5]),
                          Ficha(img, (530, 163), (114, 211), "der", [8, 9]),
                          Ficha(img, (530, 262), (213, 310), "der", [7, 9]),
                          Ficha(img, (530, 366), (317, 414), "der", [7, 8])
                         ]
            self.barras = [ [
                             [54, 18, 10, 67, 0],
                             [54, 114, 10, 145, 1],
                             [54, 287, 10, 155, 2],
                             [54, 482, 10, 62, 3]
                            ],
                            [
                             [150, 18, 10, 67, 0],
                             [150, 114, 10, 59, 1],
                             [150, 201, 10, 146, 4],
                             [150, 375, 10, 67, 2],
                             [150, 482, 10, 59, 3]
                            ],
                            [
                             [342, 62, 10, 23, 0],
                             [342, 114, 10, 21, 1],
                             [342, 163, 10, 59, 4],
                             [342, 250, 10, 56, 4],
                             [342, 334, 10, 57, 4],
                             [342, 419, 10, 23, 2],
                             [342, 482, 10, 21, 3]
                            ],
                            [
                             [534, 37, 10, 48, 0],
                             [534, 114, 10, 49, 1],
                             [534, 191, 10, 71, 4],
                             [534, 290, 10, 71, 4],
                             [534, 394, 10, 48, 2],
                             [534, 482, 10, 49, 3]
                            ]
            ]
        else:
            self.jug = jug
            # Crear arreglo de los rects
            self.fichas = [Ficha(img, (727, 258), (197, 326), "izq"),
                           Ficha(img, (631, 173), (114, 240), "izq", [2]),
                           Ficha(img, (631, 347), (288, 414), "izq", [1]),
                           Ficha(img, (432, 135), (114, 158), "izq", [4, 5, 6]),
                           Ficha(img, (432, 222), (201, 245), "izq", [3, 5, 6]),
                           Ficha(img, (432, 306), (285, 329), "izq", [3, 4, 6]),
                           Ficha(img, (432, 391), (370, 414), "izq", [3, 4, 5]),
                           Ficha(img, (241, 163), (114, 211), "izq", [8, 9]),
                           Ficha(img, (241, 262), (213, 310), "izq", [7, 9]),
                           Ficha(img, (241, 366), (317, 414), "izq", [8, 7])
                         ]
            self.barras = [ [
                             [731, 18, 10, 67, 0],
                             [731, 114, 10, 145, 1],
                             [731, 287, 10, 155, 2],
                             [731, 482, 10, 62, 3]
                            ],
                            [
                             [635, 18, 10, 67, 0],
                             [635, 114, 10, 59, 1],
                             [635, 201, 10, 146, 4],
                             [635, 375, 10, 67, 2],
                             [635, 482, 10, 59, 3]
                            ],
                            [
                             [436, 62, 10, 23, 0],
                             [436, 114, 10, 21, 1],
                             [436, 163, 10, 59, 4],
                             [436, 250, 10, 56, 4],
                             [436, 334, 10, 57, 4],
                             [436, 419, 10, 23, 2],
                             [436, 482, 10, 21, 3]
                            ],
                            [
                             [245, 37, 10, 48, 0],
                             [245, 114, 10, 49, 1],
                             [245, 191, 10, 71, 4],
                             [245, 290, 10, 71, 4],
                             [245, 394, 10, 48, 2],
                             [245, 482, 10, 49, 3]
                            ]
            ]

    def convert(self, num):
        if num >= 0 and num < 1:
            return 0
        elif num >= 1 and num < 3:
            return 1
        elif num >= 3 and num < 7:
            return 2
        elif num >= 7 and num < 10:
            return 3

    def mover_barras(self, pos, ficha):
        # Cargar informacion de fichas compañeras
        fichs = [ficha]
        for fich in ficha.com:
            fichs.append(self.fichas[fich])
        try:
            linea = self.barras[pos]
        except:
            linea = []
        for i, barra in enumerate(linea):
            if barra[0] - 4 == ficha.rect.x:
                if barra[4] == 0:
                    barra[3] = fichs[len(fichs)-1].limInf - fichs[len(fichs)-1].rect.y
                    barra[1] = 85 - barra[3]
                elif barra[4] == 1:
                    barra[3] = fichs[0].rect.y - 114
                elif barra[4] == 2:
                    barra[3] = 442 - (fichs[len(fichs)-1].rect.y + 28)
                    barra[1] = fichs[len(fichs)-1].rect.y + 28
                elif barra[4] == 3:
                    barra[3] = fichs[0].rect.y - fichs[0].limSup
                elif barra[4] == 4:
                    barra[1] = linea[i-1][1] + linea[i-1][3] + 28

    def mover(self, time, keys, bola=None):
        if self.jug == 1:
            if keys[K_w]:
                xa = 0
                for i, ficha in enumerate(self.fichas):
                    top = ficha.limSup
                    if ficha.rect.top > top:
                        if ficha.rect.y - self.speed * time <= 114:
                            ficha.rect.y = 114
                        else:
                            ficha.rect.y -= self.speed * time
                        if not (ficha.rect.x in self.acts):
                            self.acts.append(ficha.rect.x)
                            self.mover_barras(self.convert(i), ficha)
                self.acts = []

            if keys[K_s]:
                xa = 0
                for i, ficha in enumerate(self.fichas):
                    top = ficha.limInf
                    if ficha.rect.top < top:
                        if ficha.rect.y + self.speed * time >= 414:
                            ficha.rect.y = 414
                        else:
                            ficha.rect.y += self.speed * time
                        if not(ficha.rect.x in self.acts):
                            self.acts.append(ficha.rect.x)
                            self.mover_barras(self.convert(i), ficha)
                self.acts = []

        elif self.jug == 2:
            # Verifica que la bola este en un sector de la cancha
            cond1 = bola.rect.x >=111 and bola.rect.x <= 251    # Delanteros
            cond2 = bola.rect.x >= 402 and bola.rect.x <= 442   # Volantes
            cond3 = bola.rect.x >= 601 and bola.rect.x <= 641   # Defensas
            cond3 = bola.rect.x >= 687                          # Portero
            if cond1 or cond2 or cond2 or cond3:
                # Comprobar direccion
                if bola.velocidad[1] > 0: # Hacia arriba
                    for i, ficha in enumerate(self.fichas):
                        top = ficha.limSup
                        if ficha.rect.top > top:
                            if ficha.rect.y - self.speed * time <= 114:
                                ficha.rect.y = 114
                            else:
                                ficha.rect.y -= self.speed * time
                            if not(ficha.rect.x in self.acts):
                                self.acts.append(ficha.rect.x)
                                self.mover_barras(self.convert(i), ficha)
                    self.acts = []
                elif bola.velocidad[1] <= 0: # Hacia abajo
                    for i, ficha in enumerate(self.fichas):
                        top = ficha.limInf
                        if ficha.rect.top < top:
                            if ficha.rect.y + self.speed * time >= 414:
                                ficha.rect.y = 414
                            else:
                                ficha.rect.y += self.speed * time
                            if not(ficha.rect.x in self.acts):
                                self.acts.append(ficha.rect.x)
                                self.mover_barras(self.convert(i), ficha)
                    self.acts = []
        elif self.jug == 3:
            if keys[K_UP]:
                for i, ficha in enumerate(self.fichas):
                    top = ficha.limSup
                    if ficha.rect.top > top:
                        if ficha.rect.y - self.speed * time <= 114:
                            ficha.rect.y = 114
                        else:
                            ficha.rect.y -= self.speed * time
                        if not(ficha.rect.x in self.acts):
                            self.acts.append(ficha.rect.x)
                            self.mover_barras(self.convert(i), ficha)
                self.acts = []
            if keys[K_DOWN]:
                for i, ficha in enumerate(self.fichas):
                    top = ficha.limInf
                    if ficha.rect.top < top:
                        if ficha.rect.y + self.speed * time >= 414:
                            ficha.rect.y = 414
                        else:
                            ficha.rect.y += self.speed * time
                        if not(ficha.rect.x in self.acts):
                            self.acts.append(ficha.rect.x)
                            self.mover_barras(self.convert(i), ficha)
                self.acts = []

    def pintar(self, screen, clock):
        for ficha in self.fichas:
            screen.blit(ficha.image[ficha.bol], ficha.rect)
            if ficha.bol == 1:
                ficha.bol = 2
            elif ficha.bol == 2:
                ficha.bol = 0

        for linea in self.barras:
            rect = 0
            for barra in linea:
                rect = Rect(barra[0], barra[1], barra[2], barra[3])
                pygame.draw.rect(screen, GRIS, rect)

class Marcador(object):
    def __init__(self, jugadores, img):
        self.marcador_sprite = load_image(img, True)
        self.marcador_rect = self.marcador_sprite.get_rect()
        self.marcador_rect.centerx = ANCHO/2
        self.marcador_rect.y = 6
        self.jugadores = jugadores
        self.resultado = [0, 0]
        self.gol = [False, False]

    def pintar(self, screen):
        fuente = pygame.font.Font(None, 50)
        # Renderizar fuentes con el resultado parcial
        jugador1 = fuente.render(str(self.resultado[0]), 0, NEGRO)
        jugador2 = fuente.render(str(self.resultado[1]), 0, NEGRO)
        # Mostrar sprite del marcador
        screen.blit(self.marcador_sprite, self.marcador_rect)
        # Escribir el marcador parcial
        screen.blit(jugador1, (360, 31))
        screen.blit(jugador2, (425, 31))
        # Visualizar los logos de los equipos en la parte inferior:
        # Cargar escudo del equipo
        equipoA, equipoB = self.jugadores[0], self.jugadores[1]

        imageA = pygame.image.load("img/equipos" + tipo_equipo(equipoA) + equipoA + ".png")
        imageA = pygame.transform.scale(imageA, (50, 50))
        rectA = imageA.get_rect()
        rectA.x, rectA.y = 0, 530
        # Cargar escudo del contrario:
        imageB = pygame.image.load("img/equipos" + tipo_equipo(equipoB) + equipoB + ".png")
        imageB = pygame.transform.scale(imageB, (50,50))
        rectB = imageB.get_rect()
        rectB.right, rectB.y = 800, 530

        screen.blit(imageA, rectA)
        screen.blit(imageB, rectB)

    def __str__(self):
        return "[" + str(self.resultado[0]) + " , " + str(self.resultado[1]) + "]"

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
        pygame.draw.rect(self.screen, (89, 87, 87), (0, 74, self.W, 29))
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

def celebracion(screen, clock, marcador,tipo="gol"):
    if tipo == "gol":
        # Analizar la informacion, extraer el equipo que hace el gol
        equipo = marcador.jugadores[marcador.gol[1]] # Cargar nombre
        # El que recibe el gol esta en la otra posicion
        if marcador.gol[1]:
            res_e = 0
        else:
            res_e = 1
        contrario = marcador.jugadores[res_e] # Cargar nombre

        # Cargar imagen de celebracion de gol del equipo
        imagen_eq = pygame.image.load("img/celebraciones/goles/" + equipo  + ".jpg")
        imagen_eq = pygame.transform.scale(imagen_eq, (800, 600))
        rect = imagen_eq.get_rect()
        rect.x, rect.y = 0, 0

        # Cargar imagen generica: ¡goooooool!
        image_gol = pygame.image.load("img/celebraciones/gol.png")
        rect_gol = image_gol.get_rect()
        rect_gol.x, rect_gol.y = 0, 0

        # Cargar escudo del equipo
        image_esc = pygame.image.load("img/equipos" + tipo_equipo(equipo) + equipo + ".png")
        image_esc = pygame.transform.scale(image_esc, (200, 200))
        rect_esc = image_esc.get_rect()
        rect_esc.x, rect_esc.y = 20, 10
        # Cargar escudo del contrario:
        image_cont = pygame.image.load("img/equipos" + tipo_equipo(contrario) + contrario + ".png")
        image_cont = pygame.transform.scale(image_cont, (100,100))
        rect_cont = image_cont.get_rect()
        rect_cont.x, rect_cont.y = 700, 350


        # Generar resultado en pantalla
        fuente_e1 = pygame.font.Font(None, 300)
        fuente_e2 = pygame.font.Font(None, 60)
        goles_eq1 = fuente_e1.render(str(marcador.resultado[marcador.gol[1]]), 0, BLANCO)
        goles_eq2 = fuente_e2.render(str(marcador.resultado[res_e]), 0, BLANCO)


        screen.blit(imagen_eq, rect)
        screen.blit(image_gol, rect_gol)
        screen.blit(image_esc, rect_esc)
        screen.blit(image_cont, rect_cont)
        screen.blit(goles_eq1, (225, 10))
        screen.blit(goles_eq2, (665, 390))
        pygame.display.flip()
        clock.tick(0.15)

    elif tipo == "victoria":
        pass

def main():
    tablero = Tablero()
    # Mouse invisible
    pygame.mouse.set_visible(False)
    terminar = False
    bola = Balon()
    equipoA = "nacional"
    equipoB = "brasil"
    imgA = ["img/jugador" + tipo_equipo(equipoA) + equipoA +"/11.png",
            "img/jugador" + tipo_equipo(equipoA) + equipoA +"/12.png",
            "img/jugador" + tipo_equipo(equipoA) + equipoA +"/13.png"]
    imgB = ["img/jugador" + tipo_equipo(equipoB) + equipoB +"/21.png",
            "img/jugador" + tipo_equipo(equipoB) + equipoB +"/22.png",
            "img/jugador" + tipo_equipo(equipoB) + equipoB +"/23.png"]
    fichasA = Fichas(equipoA, imgA)
    fichasB = Fichas(equipoB, imgB, 2)
    marcador = Marcador([equipoA, equipoB], "img/marcador.png")

    clock = pygame.time.Clock()

    while not terminar:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        bola.actualizar(time, fichasA, fichasB, marcador)#, pala_jug)
        if marcador.gol[0] and len(marcador.gol) > 0:
            celebracion(tablero.screen, clock, marcador)

        fichasA.mover(time, keys, bola)
        if fichasB.jug == 2:
            fichasB.mover(time, keys, bola)
        elif fichasB.jug == 3:
            fichasB.mover(time, keys)

        tablero.pintar()
        tablero.screen.blit(bola.image, bola.rect)
        marcador.pintar(tablero.screen)
        fichasA.pintar(tablero.screen, clock)
        fichasB.pintar(tablero.screen, clock)
        clock.tick(50)
        pygame.display.flip()

def select_equipo(torneo):
    if torneo == "america":
        tipo_eq = "selecciones"
        equipos = EQUIPOS[tipo_eq]
        tam = (140, 140)
        posiciones = [
            [(10, 155), (170, 155), (330, 155), (490, 155), (650, 155)],
            [(10, 405), (170, 405), (330, 405), (490, 405), (650, 405)],
        ]

    elif torneo == "aguila":
        tipo_eq = "clubes"
        equipos = EQUIPOS[tipo_eq]
        tam = (100, 100)
        # Posiciones para los equipos
        posiciones = [
                    [(30, 112), (190, 112), (350, 112), (510, 112), (670, 112)],
                    [(30, 237), (190, 237), (350, 237), (510, 237), (670, 237)],
                    [(30, 362), (190, 362), (350, 362), (510, 362), (670, 362)],
                    [(30, 487), (190, 487), (350, 487), (510, 487), (670, 487)],
                ]
    juntas = []
    for posicion in posiciones:
        juntas += posicion
    # Cargar todos los escudos de los equipos
    rects = []
    for i, eq in enumerate(equipos):
        image = pygame.image.load("img/equipos/" + tipo_eq + "/" + eq + ".png")
        image = pygame.transform.scale(image, tam)
        rect_i = image.get_rect()
        rect_i.x, rect_i.y = juntas[i][0], juntas[i][1]
        rects.append([image, rect_i])

    screen = pygame.display.set_mode([ANCHO,ALTO])

    terminar = False
    clock = pygame.time.Clock()
    pos =[0, 0]
    marco = pygame.Rect(posiciones[pos[0]][pos[0]], tam)
    pygame.draw.rect(screen, (155, 0, 0), marco, 2)

    # FONDO DE PANTALLA
    fondo = pygame.image.load("img/modos/fondo2.jpg")
    rect_fondo = fondo.get_rect()
    rect_fondo.x, rect_fondo.y = 0, 0

    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            if pos[1] < 4:
                pos[1] += 1
        if keys[K_LEFT]:
            if pos[1] > 0:
                pos[1] -= 1
        if keys[K_UP]:
            if pos[0] > 0:
                pos[0] -= 1
        if keys[K_DOWN]:
            if pos[0] < len(posiciones)-1:
                pos[0] += 1
        if keys[K_ESCAPE]:
            terminar = True
            select_mode()
            return -1
        if keys[K_RETURN]:
            pass

        screen.blit(fondo, rect_fondo)
        for i, rect in enumerate(rects):
            screen.blit(rect[0], rect[1])
        marco = pygame.Rect(posiciones[pos[0]][pos[1]], tam)
        pygame.draw.rect(screen, (155, 0, 0), marco, 4)
        pygame.display.flip()
        clock.tick(20)
def copa(torneo):
    select_equipo(torneo)

def select_mode():
    screen = pygame.display.set_mode([ANCHO,ALTO])
    terminar = False
    clock = pygame.time.Clock()

    marco = pygame.Rect((40, 140), (328, 391))
    pygame.draw.rect(screen, (155, 0, 0), marco, 2)

    while not terminar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            if marco.x == 40:
                marco.x = 400
        if keys[K_LEFT]:
            if marco.x == 400:
                marco.x = 40
        if keys[K_ESCAPE]:
            terminar = True
        if keys[K_RETURN]:
            if marco.x == 40:
                copa("america")
                terminar = True
                return -1
            elif marco.x == 400:
                copa("aguila")
                terminar = True
                return -1

        # FONDO DE PANTALLA
        fondo = pygame.image.load("img/modos/fondo.jpg")
        rect_fondo = fondo.get_rect()
        rect_fondo.x, rect_fondo.y = 0, 0

        # CARGAR COPA AMERICA 2019
        america = pygame.image.load("img/torneos/america.png")
        rect_ame = america.get_rect()
        rect_ame.x, rect_ame.y = 40, 140

        # CARGAR LIGA AGUILA
        aguila = pygame.image.load("img/torneos/aguila.png")
        rect_ag = aguila.get_rect()
        rect_ag.x, rect_ag.y = 400, 140

        screen.blit(fondo, rect_fondo)
        screen.blit(america, rect_ame)
        screen.blit(aguila, rect_ag)
        pygame.draw.rect(screen, (155, 0, 0), marco, 4)
        pygame.display.flip()

select_mode()
