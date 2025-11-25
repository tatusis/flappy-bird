import pygame

import config
from asset_manager import AssetManager
from game_state import GameState
from ground import Ground
from obstacle import Obstacle
from player import Player
from score_display import ScoreDisplay


class LevelManager:
    """
    Gerencia a criação e reinicialização das entidades da sessão de jogo.

    Esta classe atua como uma 'fábrica' que instancia o Jogador, o Chão,
    os Obstáculos e o Placar, organizando-os em grupos de sprites apropriados
    para renderização (desenho) e lógica (colisão).

    Attributes:
        state (GameState): O estado atual da lógica do nível (IDLE, RUNNING, etc.).
        sprites (pygame.sprite.LayeredUpdates): Grupo para desenhar tudo na ordem correta (Z-index).
        hit_sprites (pygame.sprite.Group): Grupo otimizado contendo apenas objetos que colidem.
    """

    def __init__(self, asset_manager: AssetManager) -> None:
        """
        Prepara o gerenciador com os recursos necessários.

        Args:
            asset_manager (AssetManager): Referência ao carregador de recursos (imagens/sons).
        """
        self.asset_manager = asset_manager

    def create_fresh_level(self) -> None:
        """
        Reseta o jogo e recria todas as entidades para um novo início.

        1. Define o estado como IDLE (aguardando input).
        2. Cria grupos de sprites (Layered para desenho, Group simples para colisão).
        3. Instancia Chão, Jogador e Placar.
        4. Gera o 'pool' inicial de obstáculos que serão reciclados.
        """
        self.state = GameState.IDLE

        # --- Grupos de Sprites ---
        # LayeredUpdates permite definir o que é desenhado na frente (_layer)
        self.sprites = pygame.sprite.LayeredUpdates()

        # hit_sprites contém tudo que mata o player ou dá pontos
        self.hit_sprites = pygame.sprite.Group()

        # --- Chão (Ground) ---
        self.ground = Ground(self.asset_manager.base_image)
        self.hit_sprites.add(self.ground.bases)
        self.sprites.add(self.ground.bases)

        # --- Jogador (Player) ---
        self.player = Player(self.asset_manager.player_images, self.asset_manager.move_up_sound)
        self.sprites.add(self.player)

        # --- Placar (Score) ---
        self.score = 0
        self.score_display = ScoreDisplay(self.asset_manager.score_display_images)
        self.score_display.set(str(self.score))

        # --- Obstáculos (Obstacles) ---
        self.obstacles: list[Obstacle] = []

        # Cria 2 pares de obstáculos iniciais suficientes para cobrir a tela
        # Eles serão reciclados (reposicionados) infinitamente durante o jogo
        for i in range(2):
            obstacle = Obstacle(
                # Calcula a posição inicial baseada no índice para espaçamento correto
                (config.SCREEN_WIDTH // 2 + config.PIPE_WIDTH // 2) * i,
                self.asset_manager.pipe_image,
                self.asset_manager.coin_images,
            )
            self.obstacles.append(obstacle)

            # Adiciona as partes do obstáculo (canos e moeda) aos grupos
            self.hit_sprites.add(obstacle.pipes)
            self.hit_sprites.add(obstacle.coin)
            self.sprites.add(obstacle.pipes)
            self.sprites.add(obstacle.coin)
