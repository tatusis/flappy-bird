from enum import Enum


class PlayerState(Enum):
    """
    Enumeração que define os comportamentos físicos do Jogador (Pássaro).

    Usada dentro da classe Player para alternar entre lógicas de movimento
    (ex: flutuar vs cair) sem precisar de muitos 'if/else' complexos.
    """

    IDLE = 0
    """
    Estado de espera (Tela 'Get Ready').
    O pássaro ignora a gravidade e flutua em um padrão de onda senoidal suave.
    """

    FLYING = 1
    """
    Estado normal de jogo.
    A gravidade é aplicada constantemente e o jogador pode aplicar impulso (pulo).
    """

    DYING = 2
    """
    Estado pós-colisão.
    O input do jogador é ignorado, a animação de asas para, e o pássaro
    cai livremente até tocar o chão.
    """

    DEAD = 3
    """
    Estado final do jogador.
    Necessário reiniciar para jogar novamente.
    """
