import pygame

import config


class ScoreDisplay(pygame.sprite.Sprite):
    """
    Exibe a pontuação atual utilizando imagens personalizadas (fontes bitmap).

    Diferente de fontes TrueType (ttf), esta classe constrói dinamicamente
    uma única imagem contendo todos os dígitos da pontuação atual, garantindo
    que o estilo visual (pixel art) seja mantido.

    Attributes:
        _layer (int): 11. O elemento de UI mais alto, desenhado sobre tudo.
        number_width (int): Largura padrão de um dígito + 1px de espaçamento.
    """

    def __init__(self, score_display_images: list[pygame.Surface]) -> None:
        """
        Inicializa o mostrador de pontuação.

        Args:
            score_display_images (list): Lista de 10 superfícies (índices 0-9).
        """
        super().__init__()
        self._layer = 11
        self.images = score_display_images

        # Define a largura base usando o número '0' como referência
        # Adiciona +1 pixel para criar um pequeno respiro entre os números
        self.number_width = self.images[0].get_width() + 1
        self.number_height = self.images[0].get_height()
        self.score_length = 0

        # Inicializa vazio para evitar erro se alguém tentar acessar self.image antes do set()
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)

    def set(self, score: str) -> None:
        """
        Reconstrói a imagem da pontuação baseada no valor atual.

        Cria uma nova superfície transparente com a largura exata necessária
        para caber todos os dígitos e desenha ("blita") cada número nela.

        Args:
            score (str): A pontuação convertida para string (ex: "10").
        """
        score_length = len(score)

        if score_length != self.score_length:
            # Cria uma tela vazia transparente do tamanho da pontuação total.
            # Recria a superfície apenas se o tamanho mudou.
            self.image = pygame.surface.Surface(
                (len(score) * self.number_width, self.number_height),
                pygame.SRCALPHA,
            )
            self.score_length = score_length
        else:
            self.image.fill((0, 0, 0, 0))

        for index, char in enumerate(score):
            # Ajuste Fino de Kerning (Espaçamento Visual):
            # O número '1' em pixel art costuma ser muito fino e descentralizado.
            # Aqui aplicamos um offset de +4 pixels no eixo X para centralizá-lo melhor.
            if int(char) == 1:
                self.image.blit(self.images[int(char)], (index * self.number_width + 4, 0))
            else:
                self.image.blit(self.images[int(char)], (index * self.number_width, 0))

        # Recentraliza o placar na tela (se a pontuação for de 9 para 10, a largura muda)
        self.rect = self.image.get_rect()
        self.rect.centerx = config.SCREEN_WIDTH // 2
        self.rect.y = abs(config.SCREEN_VERTICAL_OFFSET) // 2
