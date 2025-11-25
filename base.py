import pygame

import config


class Base(pygame.sprite.Sprite):
    """
    Representa o chão (base) do jogo em movimento.

    Esta classe é geralmente instanciada duas vezes com offsets diferentes
    para criar o efeito de 'scroll infinito' (paralaxe).

    Attributes:
        _layer (int): Camada de renderização (6). Fica acima dos canos e fundo.
        change_x (float): Acumulador de movimento sub-pixel para suavidade.
    """

    def __init__(self, base_image: pygame.Surface, offset: int = 0) -> None:
        """
        Inicializa um segmento do chão.

        Args:
            base_image (pygame.Surface): A imagem texturizada do chão.
            offset (int): Posição inicial no eixo X (usado para encadear segmentos).
        """
        super().__init__()
        self._layer = 6
        self.image = base_image
        self.rect = self.image.get_rect()

        # Posicionamento inicial
        self.rect.left = offset
        self.rect.bottom = config.SCREEN_HEIGHT + config.BASE_OFFSET

        self.change_x = 0

    def update(self, dt: float) -> None:
        """
        Atualiza a posição horizontal do chão.

        Utiliza um acumulador (change_x) para lidar com movimentos fracionados
        (float) resultantes do cálculo de delta time, convertendo para pixels
        inteiros apenas quando necessário.

        Args:
            dt (float): Delta time em segundos.
        """
        self.change_x += config.GAME_SPEED * dt

        if self.change_x >= 1:
            self.rect.x -= round(self.change_x)
            self.change_x = 0
