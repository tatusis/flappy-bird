from enum import Enum


class GameState(Enum):
    """
    Enumeração que define os estados da Máquina de Estados do jogo.

    Utilizada pelo gerenciador de nível (LevelManager) para decidir qual lógica
    deve ser executada e o que deve ser desenhado na tela a cada frame.
    """

    IDLE = 0
    """Estado inicial ou de espera. O pássaro voa no lugar e aguarda o primeiro input (Tela 'Get Ready')."""

    RUNNING = 1
    """Estado de jogo ativo. A física, colisão e pontuação estão sendo processadas."""

    PAUSED = 2
    """Estado de pausa. A lógica de atualização para, mas o desenho continua (congelado)."""

    GAMEOVER = 3
    """Estado de fim de jogo. Ocorre após colisão, exibindo o placar e botões de reinício."""

    EXIT = 4
    """Sinalizador para encerrar o loop principal e fechar a aplicação."""
