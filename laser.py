import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, velocidade, tela_altura):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = velocidade
        self.limite_altura = tela_altura

    def destroi(self):
        if self.rect.y <= -50 or self.rect.y >= self.limite_altura + 50:
            self.kill()

    def update(self):
        self.rect.y += self.velocidade
        self.destroi()
