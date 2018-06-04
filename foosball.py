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
        self.velocidad = [0.5, -0.5]

    def actualizar(self, time, fich):#, pala_jug):
        self.rect.centerx += self.velocidad[0] * time
        self.rect.centery += self.velocidad[1] * time
        if self.rect.left <= 39 or self.rect.right >= 761:
            self.velocidad[0] = -self.velocidad[0]
            self.rect.centerx += self.velocidad[0] * time
        if self.rect.top <= 114 or self.rect.bottom >= 442:
            self.velocidad[1] = -self.velocidad[1]
            self.rect.centery += self.velocidad[1] * time

        if pygame.sprite.collide_rect(self, fich):
            self.velocidad[0] = -self.velocidad[0]
            self.rect.centerx += self.velocidad[0] * time

class Fichas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ficha.jpg", True)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 259
        self.speed = 0.5

    def mover(self, time, keys):
        if self.rect.top > 114:
            if keys[K_UP]:
                if self.rect.y - self.speed * time <= 114:
                    self.rect.y = 114
                else:
                    self.rect.y -= self.speed * time
        if self.rect.bottom < 439:
            if keys[K_DOWN]:
                if self.rect.y + self.speed * time >= 439:
                    self.rect.bottom = 439
                else:
                    self.rect.y += self.speed * time

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
    fich = Fichas()
    clock = pygame.time.Clock()

    while not terminar:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar = True
        bola.actualizar(time, fich)#, pala_jug)
        fich.mover(time, keys)

        tablero.pintar()
        tablero.screen.blit(bola.image, bola.rect)
        tablero.screen.blit(fich.image, fich.rect)
        pygame.display.flip()
