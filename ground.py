import pygame

from base import Base


class Ground:
    """
    Gerenciador do chão (solo) com efeito de rolagem infinita (Infinite Scroll).

    Esta classe abstrai a complexidade de gerenciar dois segmentos de chão (`Base`).
    Ela monitora a posição de ambos e os reposiciona automaticamente para garantir
    que nunca haja buracos visuais na parte inferior da tela.

    Attributes:
        bases (list[Base]): Lista contendo os dois segmentos ativos para fácil adição a grupos.
    """

    def __init__(self, base_image: pygame.Surface) -> None:
        """
        Inicializa e posiciona os dois segmentos de chão.

        O primeiro segmento começa na posição 0. O segundo é posicionado
        imediatamente ao final do primeiro, criando uma linha contínua.

        Args:
            base_image (pygame.surface.Surface): A textura visual do chão.
        """
        self.left_base = Base(base_image)
        # O segundo segmento começa exatamente onde o primeiro termina (rect.right)
        self.right_base = Base(base_image, self.left_base.rect.right)

        self.bases = [self.left_base, self.right_base]

    def update(self, dt: float) -> None:
        """
        Verifica a posição dos segmentos e recicla (teleporta) os que saíram da tela.

        Lógica de Carrossel:
        Se um segmento sair totalmente da tela pela esquerda (rect.right < 0),
        ele é movido instantaneamente para a direita do outro segmento.
        """
        # Se o segmento esquerdo saiu da tela...
        if self.left_base.rect.right < 0:
            self.left_base.rect.left = self.right_base.rect.right

        # Se o segmento direito saiu da tela...
        if self.right_base.rect.right < 0:
            self.right_base.rect.left = self.left_base.rect.right
