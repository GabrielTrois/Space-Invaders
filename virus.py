import pygame
from random import randint


class Virus(pygame.sprite.Sprite):
    def __init__(self, num, x, y):
        super().__init__()
        file_path = 'assets/sprites/enemy{}.png'.format(num)
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if num == 1: self.valor = 250
        if num == 2: self.valor = 200
        if num == 3: self.valor = 150
        if num == 4: self.valor = 100

    def update(self, direcao):
        self.rect.x += direcao


class Extra(pygame.sprite.Sprite):
    def __init__(self, lado, tela_largura):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/theenemy.png')

        if lado == 1:
            x = tela_largura + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, randint(50, 400)))

    def update(self):
        self.rect.x += self.speed
