"""
Configurações Globais do Jogo (Game Constants).

Este arquivo centraliza todos os parâmetros ajustáveis (tweakables),
caminhos de recursos (assets) e constantes de física/renderização.
Isso permite ajustar a dificuldade e a aparência sem alterar a lógica do código.
"""

import os

import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configurações do Sistema (Engine) ---
FPS = 120  # Taxa de quadros alvo
MIXER_CHANNELS = 10  # Número de canais de áudio simultâneos
SCREEN_TITLE = "Flappy Bird"
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
# Flags: Tela cheia + Escala (para manter pixel art nítida em monitores grandes)
SCREEN_FLAGS = pygame.FULLSCREEN | pygame.SCALED

# --- Física e Mecânicas Globais ---
GRAVITY = 7  # Aceleração vertical (pixels/s²)
GAME_SPEED = 150  # Velocidade de deslocamento do cenário (pixels/s)
SCREEN_VERTICAL_OFFSET = -42  # Ajuste fino da posição vertical da câmera

# --- Caminhos de Áudio (Audio Paths) ---
SCORE_SOUND = os.path.join(BASE_DIR, "assets", "audios", "audio_point.ogg")
HIT_SOUND = os.path.join(BASE_DIR, "assets", "audios", "audio_hit.ogg")
ACTION_SOUND = os.path.join(BASE_DIR, "assets", "audios", "audio_swoosh.ogg")
MOVE_UP_SOUND = os.path.join(BASE_DIR, "assets", "audios", "audio_wing.ogg")

# Eventos Customizados
# USEREVENT é o último ID de evento reservado pelo Pygame. Somamos +1 para criar o nosso.
HIT_SOUND_END_EVENT = pygame.USEREVENT + 1

# --- Caminhos de Imagem: UI & Cenário ---
BACKGROUND_IMAGES = {
    "DAY": os.path.join(BASE_DIR, "assets", "images", "background", "background-day.png"),
    "NIGHT": os.path.join(BASE_DIR, "assets", "images", "background", "background-night.png"),
}
GAME_START_IMAGE = os.path.join(BASE_DIR, "assets", "images", "message.png")
GAME_OVER_IMAGE = os.path.join(BASE_DIR, "assets", "images", "gameover.png")
BASE_IMAGE = os.path.join(BASE_DIR, "assets", "images", "base.png")
SCORE_IMAGES_PATH = os.path.join(BASE_DIR, "assets", "images", "score")

# --- Configurações de UI ---
GAME_UI_OFFSET = 60  # Deslocamento de elementos da UI
BASE_OFFSET = 28  # Altura visual do chão

# --- Entidade: Canos (Pipes) ---
PIPE_IMAGES = {
    "GREEN": os.path.join(BASE_DIR, "assets", "images", "pipe", "pipe-green.png"),
    "RED": os.path.join(BASE_DIR, "assets", "images", "pipe", "pipe-red.png"),
}
PIPE_DISTANCE = 100  # Distância horizontal entre canos (pixels)
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
# Limites para a geração aleatória da altura dos canos
PIPE_VERTICAL_OFFSET_MIN = -90 + SCREEN_VERTICAL_OFFSET
PIPE_VERTICAL_OFFSET_MAX = 90 + SCREEN_VERTICAL_OFFSET

# --- Entidade: Jogador (Player) ---
PLAYER_COLORS = ["YELLOW", "BLUE", "RED"]
PLAYER_IMAGES = {
    "YELLOW": {
        "DOWNFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "yellowbird-downflap.png"),
        "MIDFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "yellowbird-midflap.png"),
        "UPFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "yellowbird-upflap.png"),
    },
    "BLUE": {
        "DOWNFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "bluebird-downflap.png"),
        "MIDFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "bluebird-midflap.png"),
        "UPFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "bluebird-upflap.png"),
    },
    "RED": {
        "DOWNFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "redbird-downflap.png"),
        "MIDFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "redbird-midflap.png"),
        "UPFLAP": os.path.join(BASE_DIR, "assets", "images", "player", "redbird-upflap.png"),
    },
}
PLAYER_ANIMATION_STEP = 0.075  # Tempo entre frames da animação (segundos)
PLAYER_DOWN_SPEED_LIMIT = 10  # Velocidade máxima de queda
PLAYER_IMPULSE = 2  # Força do pulo (negativo sobe, positivo desce)

# --- Entidade: Moedas (Coins) ---
COIN_ANIMATION_STEP = 0.020  # Rapidez do giro da moeda (segundos)
COIN_MOVEMENT_STEP = 0.050  # Rapidez da oscilação vertical (segundos)
COIN_IMAGES = {
    "GOLD": os.path.join(BASE_DIR, "assets", "images", "coin", "gold-coins.png"),
    "SILVER": os.path.join(BASE_DIR, "assets", "images", "coin", "silver-coins.png"),
}
COINT_TILE_SET_SIZE = 14  # Quantos quadros existem no spritesheet
COIN_TILE_SIZE = 32  # Tamanho de cada quadro (px)
