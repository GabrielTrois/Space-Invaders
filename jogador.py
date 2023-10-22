import pygame
from laser import Laser


class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, limite, velocidade):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/spaceship.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.velocidade = velocidade
        self.limite_x = limite
        self.pronto = True
        self.laser_timer = 0
        self.tempo_recarga_laser = 600

        self.lasers = pygame.sprite.Group()

        self.laser_som = pygame.mixer.Sound('assets/sounds/laser.wav')
        self.laser_som.set_volume(0.3)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade

        if keys[pygame.K_SPACE] and self.pronto:
            self.atira_laser()
            self.pronto = False
            self.laser_timer = pygame.time.get_ticks()
            self.laser_som.play()

    def recarrega(self):
        if not self.pronto:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.laser_timer >= self.tempo_recarga_laser:
                self.pronto = True

    def limita(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.limite_x:
            self.rect.right = self.limite_x

    def atira_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.limita()
        self.recarrega()
        self.lasers.update()
