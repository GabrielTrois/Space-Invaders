import pygame
import sys

import virus
from jogador import Jogador
import obstaculo
from virus import Virus, Extra
from random import choice, randint
from laser import Laser


class Jogo:
    def __init__(self):
        # Jogador
        jogador_nave = Jogador((tela_largura / 2, tela_altura), tela_largura, 5)
        self.jogador = pygame.sprite.GroupSingle(jogador_nave)

        # Vida e pontos
        self.vidas = 3
        self.vida_surf = pygame.image.load('assets/sprites/spaceship.png').convert_alpha()
        self.vida_posicao_x = tela_largura - (self.vida_surf.get_size()[0] * 2 + 20)
        self.pontos = 0
        self.fonte = pygame.font.Font('assets/Pixeled.ttf', 20)

        # Obstaculo
        self.formato = obstaculo.formato
        self.tamanho_bloco = 6
        self.blocos = pygame.sprite.Group()
        self.qtd_obstaculos = 4
        self.obstaculo_x_posicao = [num * (tela_largura / self.qtd_obstaculos) for num in range(self.qtd_obstaculos)]
        self.cria_barreira(*self.obstaculo_x_posicao, x_inicio=tela_largura / 15, y_inicio=480)

        # Inimigos Virus
        self.inimigos = pygame.sprite.Group()
        self.virus_lasers = pygame.sprite.Group()
        self.inimigo_setup(rows=6, cols=8)
        self.virus_direcao = 1
        self.distancia_abaixo = 2
        self.velocidade_virus = 0

        # Virus extra
        self.extra = pygame.sprite.GroupSingle()
        self.virus_extra_timer = randint(200, 500)
        self.erros = pygame.sprite.Group()

        # Audio
        musica = pygame.mixer.Sound('assets/sounds/music.mp3')
        musica.set_volume(0.3)
        musica.play(loops=-1)

        self.laser_som = pygame.mixer.Sound('assets/sounds/laser.wav')
        self.laser_som.set_volume(0.1)
        self.explosao_som = pygame.mixer.Sound('assets/sounds/audio_explosion.wav')
        self.explosao_som.set_volume(0.3)
        self.extra_morte_som = pygame.mixer.Sound('assets/sounds/VENUSBACKTOFIGHT.wav')
        self.extra_morte_som.set_volume(2)
        self.jogador_dano_som = pygame.mixer.Sound('assets/sounds/critShoot.wav')
        self.jogador_dano_som.set_volume(2)

    def cria_obstaculo(self, x_inicial, y_inicial, offset_x):
        for lin_index, row in enumerate(self.formato):
            for col_index, col in enumerate(row):
                if col == 'X':
                    x = x_inicial + col_index * self.tamanho_bloco + offset_x
                    y = y_inicial + lin_index * self.tamanho_bloco
                    bloco = obstaculo.Bloco(self.tamanho_bloco, (241, 79, 80), x, y)
                    self.blocos.add(bloco)

    def cria_barreira(self, *offset, x_inicio, y_inicio):
        for offset_x in offset:
            self.cria_obstaculo(x_inicio, y_inicio, offset_x)

    def inimigo_setup(self, rows, cols, x_distancia=60, y_distancia=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distancia + x_offset
                y = row_index * y_distancia + y_offset

                if row_index < 1:
                    tipo_inimigo = 1
                elif row_index < 2:
                    tipo_inimigo = 2
                elif row_index < 4:
                    tipo_inimigo = 3
                elif row_index < 6:
                    tipo_inimigo = 4
                virus_sprite = Virus(tipo_inimigo, x, y)
                self.inimigos.add(virus_sprite)

    def checa_virus_posicao(self):
        todos_os_virus = self.inimigos.sprites()
        for virus in todos_os_virus:
            if virus.rect.right >= tela_largura:
                self.virus_direcao = -1 - self.velocidade_virus
                self.virus_move_abaixo(self.distancia_abaixo)
            elif virus.rect.left <= 0:
                self.virus_direcao = 1 + self.velocidade_virus
                self.virus_move_abaixo(self.distancia_abaixo)

    def virus_move_abaixo(self, distancia):
        if self.inimigos:
            for virus in self.inimigos.sprites():
                virus.rect.y += distancia

    def virus_atira(self):
        if self.inimigos.sprites():
            inimigo_aleatorio = choice(self.inimigos.sprites())
            laser_sprite = Laser(inimigo_aleatorio.rect.center, 6, tela_altura)
            self.virus_lasers.add(laser_sprite)
            self.laser_som.play()

    def extra_aparece(self):
        self.virus_extra_timer -= 1
        if self.virus_extra_timer <= 0:
            self.extra.add(Extra(randint(0, 1), tela_largura))
            self.virus_extra_timer = randint(250, 300)

    def checa_colisao(self):
        # ‘Laser’ do Jogador
        if self.jogador.sprite.lasers:
            for laser in self.jogador.sprite.lasers:
                # Obstaculos
                if pygame.sprite.spritecollide(laser, self.blocos, True):
                    laser.kill()
                # Virus
                virus_atingido = pygame.sprite.spritecollide(laser, self.inimigos, True)
                if virus_atingido:
                    for virus in virus_atingido:
                        self.pontos += virus.valor
                    laser.kill()
                    self.explosao_som.play()
                # Extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.pontos += 500
                    pygame.draw.rect(tela, 'red', (randint(0, 500), randint(0, 500), 100, 100))
                    pygame.draw.rect(tela, 'black', (randint(0, 500), randint(0, 500), 100, 100))
                    self.velocidade_virus += 1
                    self.distancia_abaixo += 1
                    self.virus_atira()
                    self.extra_morte_som.play()

        # Laser do virus
        if self.virus_lasers:
            for laser in self.virus_lasers:
                # Obstaculos
                if pygame.sprite.spritecollide(laser, self.blocos, True):
                    laser.kill()
                # Jogador
                if pygame.sprite.spritecollide(laser, self.jogador, False):
                    laser.kill()
                    self.jogador_dano_som.play()
                    self.vidas -= 1
                    if self.vidas <= 0:
                        pygame.quit()
                        sys.exit()

        # Virus
        if self.inimigos:
            for virus in self.inimigos:
                if pygame.sprite.spritecollide(virus, self.blocos, True):
                    pass
                if pygame.sprite.spritecollide(virus, self.jogador, False):
                    pygame.quit()
                    sys.exit()

    def mostra_vidas(self):
        for vida in range(self.vidas - 1):
            x = self.vida_posicao_x + (vida * self.vida_surf.get_size()[0] + 10)
            tela.blit(self.vida_surf, (x, 8))

    def mostra_pontos(self):
        pontos_surf = self.fonte.render(f'Pontuacao: {self.pontos}', False, 'white')
        pontos_rect = pontos_surf.get_rect(topleft=(10, -10))
        tela.blit(pontos_surf, pontos_rect)

    def vitoria(self):
        if not self.inimigos.sprites():
            vitoria_surf = self.fonte.render('VOCE VENCEU!!!', False, 'white')
            vitoria_rect = vitoria_surf.get_rect(center=(tela_largura / 2, tela_largura / 2))
            tela.blit(vitoria_surf, vitoria_rect)

    def rodar(self):
        self.jogador.update()
        self.inimigos.update(self.virus_direcao)
        self.extra.update()
        self.virus_lasers.update()

        self.extra_aparece()
        self.checa_virus_posicao()
        self.checa_colisao()

        self.jogador.sprite.lasers.draw(tela)
        self.jogador.draw(tela)
        self.blocos.draw(tela)
        self.inimigos.draw(tela)
        self.virus_lasers.draw(tela)
        self.extra.draw(tela)

        self.mostra_vidas()
        self.mostra_pontos()

        self.vitoria()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load('assets/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (tela_largura, tela_altura))

    def cria_linhas(self):
        linha_altura = 3
        linha_qtd = int(tela_altura / linha_altura)
        for linha in range(linha_qtd):
            y = linha * linha_altura
            pygame.draw.line(self.tv, 'black', (0, y), (tela_largura, y), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 100))
        self.cria_linhas()
        tela.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    tela_altura = 600
    tela_largura = 600

    tela = pygame.display.set_mode((tela_largura, tela_altura))
    relogio = pygame.time.Clock()

    jogo = Jogo()
    crt = CRT()

    VIRUSLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(VIRUSLASER, 800)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == VIRUSLASER:
                jogo.virus_atira()

        tela.fill((30, 30, 30))

        jogo.rodar()
        crt.draw()

        pygame.display.flip()
        relogio.tick(60)
