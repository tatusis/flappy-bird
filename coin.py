import pygame

import config


class Coin(pygame.sprite.Sprite):
    """
    Representa uma moeda colecionável com animação de rotação e efeito de flutuação.

    A moeda se posiciona relativamente a um retângulo pai (geralmente os canos)
    e oscila verticalmente para dar dinamismo visual.

    Attributes:
        _layer (int): 9. Renderizada acima da maioria dos elementos.
        vertical_offset (int): Deslocamento atual para o efeito de "flutuar".
    """

    def __init__(self, parent_rect: pygame.Rect, coin_images: list[pygame.Surface]) -> None:
        """
        Inicializa a moeda vinculada a uma posição pai.

        Args:
            parent_rect (pygame.rect.Rect): Referência para centralizar a moeda (ex: meio dos canos).
            coin_images (list): Lista de superfícies para a animação de rotação.
        """
        super().__init__()
        self._layer = 9
        self.parent_rect = parent_rect
        self.images = coin_images

        # Estado da animação
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.animation_step = config.COIN_ANIMATION_STEP

        # Posicionamento
        self.rect = self.image.get_rect()
        self.rect.centerx = parent_rect.centerx
        self.rect.centery = parent_rect.centery

        # Configuração do efeito de "Flutuar" (Bobbing)
        self.movement_step = config.COIN_MOVEMENT_STEP
        self.vertical_offset = 0
        self.vertical_direction = 1
        self.vertical_offset_max = 5

        # --- Configuração da Máscara de Colisão (Hitbox) ---
        # Cria uma superfície vazia do tamanho da moeda
        mask = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Desenha um círculo branco no centro para representar a moeda
        # Isso cria uma colisão mais "justa" que ignora os cantos do sprite
        mask_center = (self.rect.width // 2, self.rect.height // 2)
        mask_radius = min(self.rect.width, self.rect.height) // 3
        pygame.draw.circle(mask, (255, 255, 255), mask_center, mask_radius)

        # Converte a superfície desenhada em uma máscara de bits para colisão pixel-perfect
        self.mask = pygame.mask.from_surface(mask)

    def reset(self, dt: float) -> None:
        """Reinicia a posição da moeda baseada no pai."""
        self.handle_movement(dt)

    def handle_animation(self, dt: float) -> None:
        """
        Alterna os frames da imagem para criar o efeito de rotação.

        Mantém o centro do retângulo estável mesmo se o tamanho da imagem mudar.
        """
        if self.animation_step < 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0

            self.image = self.images[self.image_index]
            # Importante: Recalcula o rect mantendo o centro para evitar "pulos" visuais
            rect_center = self.rect.center
            self.rect.size = self.image.get_size()
            self.rect.center = rect_center
            self.animation_step = config.COIN_ANIMATION_STEP
        else:
            self.animation_step -= dt

    def handle_movement(self, dt: float) -> None:
        """
        Sincroniza a moeda com o pai (eixo X) e aplica o efeito de flutuação (eixo Y).

        A moeda oscila para cima e para baixo (vertical_offset) dentro de um
        limite máximo (vertical_offset_max).
        """
        # Sincronia horizontal com o objeto pai (ex: canos se movendo)
        self.rect.centerx = self.parent_rect.centerx

        # Lógica de oscilação vertical (Bobbing)
        if self.movement_step < 0:
            self.vertical_offset += self.vertical_direction

            if abs(self.vertical_offset) >= self.vertical_offset_max:
                self.vertical_direction *= -1

            self.movement_step = config.COIN_MOVEMENT_STEP
        else:
            self.movement_step -= dt

        self.rect.centery = self.parent_rect.centery + self.vertical_offset

    def update(self, dt: float) -> None:
        """Atualiza a lógica de movimento e animação a cada frame."""
        self.handle_movement(dt)
        self.handle_animation(dt)
