import pygame

import config


class Helper:
    """
    Coleção de métodos estáticos utilitários para operações gráficas.

    Esta classe fornece funções auxiliares para posicionamento de UI e
    manipulação de texturas (como recorte de spritesheets), evitando
    repetição de código matemático complexo em outras classes.
    """

    @staticmethod
    def display_centered_image(screen: pygame.Surface, image: pygame.Surface) -> None:
        """
        Renderiza uma imagem centralizada na tela, respeitando offsets de UI.

        Calcula o centro exato baseado nas dimensões da tela e da imagem,
        aplicando ajustes verticais definidos no config (SCREEN_VERTICAL_OFFSET
        e GAME_UI_OFFSET) para ajustar a posição de logos e mensagens.

        Args:
            screen (pygame.Surface): A superfície de destino.
            image (pygame.Surface): A imagem a ser desenhada.
        """
        screen.blit(
            image,
            (
                # Centraliza no eixo X
                config.SCREEN_WIDTH // 2 - image.get_rect().width // 2,
                # Centraliza no eixo Y e aplica os ajustes finos de design
                config.SCREEN_HEIGHT // 2
                - image.get_rect().height // 2
                + config.SCREEN_VERTICAL_OFFSET
                + config.GAME_UI_OFFSET,
            ),
        )

    @staticmethod
    def display_cursor_image(screen: pygame.Surface, cursor_image: pygame.Surface):
        """
        Desenha uma imagem na posição atual do ponteiro do mouse.

        Útil para substituir o cursor do sistema por um sprite personalizado do jogo.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_image_rect = cursor_image.get_rect(center=(mouse_x, mouse_y))
        screen.blit(cursor_image, cursor_image_rect)

    @staticmethod
    def get_tile(x: int, y: int, tile_size: int, tile_set: pygame.Surface) -> pygame.Surface:
        """
        Extrai (recorta) um único sprite de uma folha de sprites (tileset/spritesheet).

        Cria uma nova superfície transparente e copia apenas a região desejada
        da imagem original baseada em coordenadas de grade (grid).

        Args:
            x (int): O índice da coluna na grade (0, 1, 2...).
            y (int): O índice da linha na grade.
            tile_size (int): O tamanho quadrado do sprite (em pixels).
            tile_set (pygame.Surface): A imagem original contendo todos os sprites.

        Returns:
            pygame.Surface: Uma nova superfície contendo apenas o sprite recortado.
        """
        rect = pygame.rect.Rect(
            tile_size * x,
            tile_size * y,
            tile_size,
            tile_size,
        )
        # Cria uma superfície vazia com suporte a transparência (Alpha Channel)
        tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)

        # Copia o pedaço da imagem original para a nova superfície
        tile.blit(tile_set, (0, 0), rect)

        return tile
