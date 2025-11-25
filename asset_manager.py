import random

import pygame

import config
from helper import Helper


class AssetManager:
    """
    Gerenciador central de ativos (assets) do jogo.

    Responsável por carregar imagens e sons do disco para a memória,
    além de definir aleatoriamente o tema visual da partida atual
    (cor do pássaro, cenário dia/noite, cor dos canos, etc.).

    Attributes:
        background_image (pygame.Surface): Imagem de fundo (Dia ou Noite).
        player_images (list[pygame.Surface]): Sequência de quadros de animação do pássaro.
        pipe_image (pygame.Surface): Imagem do obstáculo (cano).
        coin_images (list[pygame.Surface]): Quadros de animação da moeda.
        score_display_images (list[pygame.Surface]): Imagens dos números 0-9 para o placar.
        sounds (dict): (Implícito) Vários efeitos sonoros carregados via pygame.mixer.
        channel (pygame.mixer.Channel): Canal reservado (ID 0) para sequência de sons de morte.
    """

    def __init__(self) -> None:
        """
        Carrega todos os ativos, define as variações aleatórias da sessão e configura o sistema de áudio prioritário.
        """

        # --- Cenário (Background) ---
        background_color = random.choice(["DAY", "NIGHT"])
        background_image = config.BACKGROUND_IMAGES[background_color]
        self.background_image = pygame.image.load(background_image).convert()

        # --- Interface (UI) ---
        self.game_start_image = pygame.image.load(config.GAME_START_IMAGE).convert_alpha()
        self.game_over_image = pygame.image.load(config.GAME_OVER_IMAGE).convert_alpha()
        self.base_image = pygame.image.load(config.BASE_IMAGE).convert()

        # --- Jogador (Player) ---
        # Seleciona aleatoriamente a cor e carrega os 3 estados de asa
        player_color = random.choice(["YELLOW", "BLUE", "RED"])
        player_images = config.PLAYER_IMAGES[player_color]
        self.player_images = [
            pygame.image.load(player_images["DOWNFLAP"]).convert_alpha(),
            pygame.image.load(player_images["MIDFLAP"]).convert_alpha(),
            pygame.image.load(player_images["UPFLAP"]).convert_alpha(),
            pygame.image.load(player_images["MIDFLAP"]).convert_alpha(),
        ]

        # --- Placar (Score) ---
        self.score_display_images = [
            pygame.image.load(f"{config.SCORE_IMAGES_PATH}/{i}.png").convert_alpha() for i in range(10)
        ]

        # --- Obstáculos (Pipes) ---
        pipe_color = random.choice(["GREEN", "RED"])
        pipe_image = config.PIPE_IMAGES[pipe_color]
        self.pipe_image = pygame.image.load(pipe_image).convert_alpha()

        # --- Colecionáveis (Coins) ---
        # Recorta os sprites da moeda de uma folha de sprites (spritesheet)
        coin_color = random.choice(["GOLD", "SILVER"])
        coin_images = config.COIN_IMAGES[coin_color]
        coin_tile_set = pygame.image.load(coin_images).convert_alpha()
        self.coin_images = [
            Helper.get_tile(i, 0, config.COIN_TILE_SIZE, coin_tile_set) for i in range(config.COINT_TILE_SET_SIZE)
        ]

        # --- Áudio (Sounds) ---
        self.score_sound = pygame.mixer.Sound(config.SCORE_SOUND)
        self.hit_sound = pygame.mixer.Sound(config.HIT_SOUND)
        self.action_sound = pygame.mixer.Sound(config.ACTION_SOUND)
        self.move_up_sound = pygame.mixer.Sound(config.MOVE_UP_SOUND)
        self.die_sound = pygame.mixer.Sound("assets/audios/audio_die.ogg")

        # Configuração de canal prioritário
        # O canal 0 foi reservado na inicialização do pygame. Aqui nós pegamos a referência dele.
        self.channel = pygame.mixer.Channel(0)

        # Configura um evento customizado para ser disparado quando o som
        # tocando neste canal terminar. Usado para encadear HIT -> DIE.
        self.channel.set_endevent(config.HIT_SOUND_END_EVENT)
