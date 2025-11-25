import pygame


class Pipe(pygame.sprite.Sprite):
    """
    Representa um cano individual (obstáculo) no jogo.

    Esta classe gerencia a imagem (invertida ou não) e a posição do cano,
    mantendo-o sincronizado com um retângulo pai (parent_rect).

    Attributes:
        image (pygame.Surface): A imagem final processada do cano.
        rect (pygame.Rect): O retângulo de posição e colisão do sprite.
        flip (bool): Indica se o cano está invertido (topo) ou normal (base).
    """

    def __init__(self, parent_rect: pygame.Rect, pipe_image: pygame.Surface, flip: bool = False) -> None:
        """
        Inicializa um novo sprite de cano.

        Args:
            parent_rect (pygame.Rect): O retângulo de referência para o posicionamento X.
            pipe_image (pygame.Surface): A imagem base do cano.
            flip (bool, optional): Se True, inverte a imagem verticalmente (cano do topo).
                                   Padrão é False (cano de baixo).
        """
        super().__init__()
        self._layer = 5
        self.parent_rect = parent_rect
        image = pipe_image
        self.flip = flip

        # Configuração da imagem
        if self.flip:
            self.image = pygame.transform.flip(image, flip_x=False, flip_y=True)
        else:
            self.image = image

        # Configuração da posição inicial
        self.rect = self.image.get_rect()
        self.handle_movement()

    def reset(self, dt: float) -> None:
        """Reinicia o estado do cano, realinhando-o com o pai (obstáculo)."""
        self.handle_movement()

    def handle_movement(self) -> None:
        """Atualiza a posição do cano baseada na posição do retângulo pai (obstáculo)."""
        self.rect.x = self.parent_rect.x

        if self.flip:
            self.rect.top = self.parent_rect.top
        else:
            self.rect.bottom = self.parent_rect.bottom

    def update(self, dt: float) -> None:
        """Chamado a cada frame para atualizar a lógica do sprite."""
        self.handle_movement()
