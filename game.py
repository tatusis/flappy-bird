import pygame

import config
from asset_manager import AssetManager
from coin import Coin
from game_state import GameState
from helper import Helper
from level_manager import LevelManager
from player_state import PlayerState


class Game:
    """
    Controlador central da lógica de gameplay.

    Esta classe orquestra a interação entre a entrada do usuário,
    o gerenciamento de estados (LevelManager) e a renderização (Draw).
    Ela não contém o loop `while` principal (que fica na classe FlappyBird),
    mas executa a lógica de cada frame.

    Attributes:
        screen (pygame.Surface): Superfície onde o jogo é desenhado.
        asset_manager (AssetManager): Carregador de sons e imagens.
        level_manager (LevelManager): Gerenciador de entidades (player, canos, score).
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Inicializa os gerenciadores essenciais do jogo."""
        self.screen = screen
        self.asset_manager = AssetManager()
        self.level_manager = LevelManager(self.asset_manager)

    def start_level(self) -> None:
        """Solicita ao LevelManager a criação de um novo nível limpo."""
        self.level_manager.create_fresh_level()

    def handle_events(self) -> None:
        """
        Processa a fila de eventos do Pygame (Inputs).

        Mapeamento:
            ESC: Encerra o jogo.
            P: Alterna entre PAUSED e RUNNING.
            Mouse Esq (Click): Inicia o jogo (se IDLE) ou faz o pássaro voar.
            Mouse Dir (Click): Reinicia o jogo se estiver em GAMEOVER.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.level_manager.state = GameState.EXIT

            # Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.level_manager.state = GameState.EXIT
                elif event.key == pygame.K_p:
                    if self.level_manager.state == GameState.RUNNING:
                        self.level_manager.state = GameState.PAUSED
                    elif self.level_manager.state == GameState.PAUSED:
                        self.level_manager.state = GameState.RUNNING

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Botão Esquerdo: Ação principal (Voar / Iniciar)
                if event.button == 1:
                    if self.level_manager.state == GameState.IDLE:
                        self.level_manager.state = GameState.RUNNING
                        self.level_manager.player.state = PlayerState.FLYING
                        self.level_manager.sprites.add(self.level_manager.score_display)
                        self.level_manager.player.move_up()
                    elif self.level_manager.state in [GameState.IDLE, GameState.RUNNING]:
                        self.level_manager.player.move_up()

                # Botão Direito: Reiniciar após morte
                elif event.button == 3:
                    # Só reinicia se a animação de morte acabou
                    if (
                        self.level_manager.state == GameState.GAMEOVER
                        and self.level_manager.player.state == PlayerState.DEAD
                    ):
                        self.asset_manager.action_sound.play()
                        self.start_level()

            # Evento customizado de som (Hit acabou -> Toca Die)
            if event.type == config.HIT_SOUND_END_EVENT:
                self.asset_manager.die_sound.play()

    def update(self, dt: float) -> None:
        """
        Atualiza a física, colisões e lógica de pontuação.

        Verifica colisões pixel-perfect (máscaras) diferenciando entre
        coletar uma moeda (Score) e bater em um cano/chão (Game Over).
        """
        if self.level_manager.state in [GameState.IDLE, GameState.RUNNING]:
            self.level_manager.sprites.update(dt)
            self.level_manager.ground.update(dt)

            if self.level_manager.state == GameState.RUNNING:
                # Lógica de reciclagem de obstáculos
                for obstacle in self.level_manager.obstacles:
                    obstacle.update(dt)

                    # Se o obstáculo saiu da tela, reseta e reativa a moeda
                    if obstacle.rect.right < 0:
                        obstacle.reset(dt)
                        self.level_manager.hit_sprites.add(obstacle.coin)
                        self.level_manager.sprites.add(obstacle.coin)

                # Detecção de Colisões (Pixel-Perfect)
                collided_sprite = pygame.sprite.spritecollideany(
                    self.level_manager.player,  # type: ignore
                    self.level_manager.hit_sprites,
                    pygame.sprite.collide_mask,
                )

                if collided_sprite:
                    if isinstance(collided_sprite, Coin):
                        # Colisão boa: Coletou moeda
                        self.level_manager.hit_sprites.remove(collided_sprite)
                        self.level_manager.sprites.remove(collided_sprite)
                        self.asset_manager.score_sound.play()
                        self.level_manager.score += 1
                        self.level_manager.score_display.set(str(self.level_manager.score))
                    else:
                        # Colisão ruim: Bateu no cano ou chão
                        # Toca o som em um canal específico para monitorar o fim dele
                        self.asset_manager.channel.play(self.asset_manager.hit_sound)

                        # Muda o estado do jogo
                        self.level_manager.state = GameState.GAMEOVER

                        # Inicia o tratamento da morte do jogador após a colisão
                        self.level_manager.player.handle_death()

        # Se estiver em GAMEOVER, continuamos atualizando APENAS o player
        # para que ele continue caindo (DYING) até virar DEAD
        if self.level_manager.state == GameState.GAMEOVER:
            if self.level_manager.player.state != PlayerState.DEAD:
                self.level_manager.player.update(dt)

    def draw(self) -> None:
        """
        Renderiza todos os elementos visuais na tela.

        Ordem de desenho (Layering):
        1. Fundo (Background)
        2. Sprites (Pássaro, Canos, Moedas, Chão, Score)
        3. UI Overlays (Mensagens de Início ou Game Over)
        """
        self.screen.blit(self.asset_manager.background_image, (0, 0))
        self.level_manager.sprites.draw(self.screen)

        if self.level_manager.state == GameState.IDLE:
            Helper.display_centered_image(self.screen, self.asset_manager.game_start_image)

        # Só mostra Game Over quando o corpo esfriar (DEAD)
        if self.level_manager.state == GameState.GAMEOVER and self.level_manager.player.state == PlayerState.DEAD:
            Helper.display_centered_image(self.screen, self.asset_manager.game_over_image)

        pygame.display.flip()
