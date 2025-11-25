import sys

import pygame

import config
from game import Game
from game_state import GameState


class FlappyBird:
    """
    Classe principal que gerencia o ciclo de vida da aplicação Flappy Bird.

    Esta classe é responsável pela inicialização da biblioteca Pygame,
    configuração da janela de exibição e execução do loop principal do jogo (Game Loop).

    Attributes:
        screen (pygame.Surface): A superfície principal onde tudo é renderizado.
        clock (pygame.time.Clock): Gerencia a taxa de quadros (FPS) e o delta time.
        game (Game): A instância da lógica central do jogo.
    """

    def __init__(self) -> None:
        """
        Inicializa o ambiente do jogo e configurações de vídeo/áudio.

        Configura o mixer, inicia o Pygame, cria a janela com VSync habilitado
        para suavidade, e instancia a lógica do jogo (Game).
        """
        pygame.mixer.pre_init(channels=config.MIXER_CHANNELS)
        pygame.init()

        # Reserva o canal 0 exclusivamente para sons críticos (Hit -> Die)
        # Isso impede que sons de pontuação ou voo interrompam a sequência de morte
        pygame.mixer.set_reserved(1)

        # Configuração da Janela
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
            config.SCREEN_FLAGS,
            vsync=True,
        )
        pygame.display.set_caption(config.SCREEN_TITLE)

        # Configurações de Input e Tempo
        pygame.mouse.set_visible(False)

        # Inicialização da Lógica
        self.clock = pygame.time.Clock()
        self.game = Game(self.screen)
        self.game.start_level()

    def start(self) -> None:
        """
        Inicia o loop principal do jogo (Main Loop).

        Este método mantém o jogo rodando indefinidamente até que o estado
        do jogo mude para EXIT. Ele coordena:
        1. Processamento de eventos (handle_events).
        2. Atualização lógica (update).
        3. Renderização (draw).
        4. Controle de tempo (tick).
        """
        dt = 0

        while not self.game.level_manager.state == GameState.EXIT:
            self.game.handle_events()
            self.game.update(dt)
            self.game.draw()

            # Calcula o delta time em segundos (t / 1000) para movimento independente de FPS
            dt = self.clock.tick(config.FPS) / 1_000

        # Limpeza e saída segura
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    FlappyBird().start()
