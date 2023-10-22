import pygame

class Bloco(pygame.sprite.Sprite):
    def __init__(self, tamanho, cor, x, y):
        super().__init__()
        self.image = pygame.Surface((tamanho, tamanho))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))


formato = [
'XX      XX',
'XXX    XXX',
'XXXXXXXXXX',
'XXXXXXXXXX',
'XXXXXXXXXX',
' XXXXXXXX',
'  XXXXXX']
