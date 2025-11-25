import random

import pygame

import config
from coin import Coin
from pipe import Pipe


class Obstacle:
    """
    Representa um conjunto completo de obstáculos (Par de Canos + Moeda).

    Esta classe atua como um 'Container'. Ela gerencia um retângulo invisível (`self.rect`)
    que serve de âncora posicional. Ao mover este retângulo, os sprites filhos
    (top_pipe, bottom_pipe e coin) recalculam suas posições automaticamente.

    Attributes:
        rect (pygame.Rect): O retângulo 'pai' invisível usado para posicionamento.
        pipes (list[Pipe]): Lista contendo os objetos Pipe superior e inferior.
        coin (Coin): O objeto moeda centralizado entre os canos.
    """

    def __init__(self, x_offset: int, pipe_image: pygame.Surface, coin_images: list[pygame.Surface]) -> None:
        """
        Inicializa o par de canos e a moeda em uma posição aleatória.

        Args:
            x_offset (int): Distância inicial no eixo X (usado para espaçar múltiplos obstáculos).
            pipe_image (pygame.Surface): Imagem base para os canos.
            coin_images (list): Lista de imagens para a animação da moeda.
        """
        # Define a altura aleatória do vão (gap) entre os canos
        y_offset = random.randint(config.PIPE_VERTICAL_OFFSET_MIN, config.PIPE_VERTICAL_OFFSET_MAX)

        # Cria o 'Retângulo Pai' invisível
        # Ele abrange toda a altura da estrutura (cano cima + vão + cano baixo)
        self.rect = pygame.Rect(
            config.SCREEN_WIDTH + x_offset,
            (config.SCREEN_HEIGHT // 2) - (config.PIPE_DISTANCE // 2) - config.PIPE_HEIGHT + y_offset,
            config.PIPE_WIDTH,
            (config.PIPE_HEIGHT * 2) + config.PIPE_DISTANCE,
        )
        self.change_x = 0

        # Sprites Filhos (recebem self.rect como referência)
        self._top_pipe = Pipe(self.rect, pipe_image, flip=True)
        self._bottom_pipe = Pipe(self.rect, pipe_image)
        self.pipes = [self._top_pipe, self._bottom_pipe]

        # Moeda
        self.coin = Coin(self.rect, coin_images)

    def reset(self, dt: float) -> None:
        """
        Recicla o obstáculo, enviando-o de volta para o início com nova altura.

        Chamado quando o obstáculo sai da tela pela esquerda (Object Pooling).
        Isso evita ter que destruir e recriar objetos na memória.
        """
        y_offset = random.randint(config.PIPE_VERTICAL_OFFSET_MIN, config.PIPE_VERTICAL_OFFSET_MAX)

        # Reposiciona o retângulo pai lá no início (direita da tela)
        self.rect.x = config.SCREEN_WIDTH
        self.rect.y = (config.SCREEN_HEIGHT // 2) - (config.PIPE_DISTANCE // 2) - config.PIPE_HEIGHT + y_offset

        # Avisa os filhos para se realinharem
        self._top_pipe.reset(dt)
        self._bottom_pipe.reset(dt)
        self.coin.reset(dt)

    def update(self, dt: float) -> None:
        """
        Move o obstáculo (container) para a esquerda.

        Utiliza a mesma lógica de acumulador (change_x) da classe Base
        para garantir movimento suave independente do frame rate.
        """
        self.change_x += config.GAME_SPEED * dt

        if self.change_x >= 1:
            self.rect.x -= round(self.change_x)
            self.change_x = 0
