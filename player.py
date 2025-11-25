import pygame

import config
from player_state import PlayerState


class Player(pygame.sprite.Sprite):
    """
    Representa o personagem controlado pelo jogador (Pássaro).

    Esta classe gerencia três aspectos cruciais:
    1. Animação de sprites (bater de asas).
    2. Física de gravidade e impulso (pulo).
    3. Criação de uma máscara de colisão otimizada (Hitbox Circular).

    Attributes:
        _layer (int): 10. O pássaro é desenhado na frente de canos e chão.
        state (PlayerState): Estado atual (IDLE, FLYING, DEAD).
        mask (pygame.Mask): A área de colisão física (circular, menor que a imagem).
    """

    def __init__(self, player_images: list[pygame.Surface], move_up_sound: pygame.mixer.Sound) -> None:
        """
        Inicializa o pássaro e configura sua hitbox circular.

        Args:
            player_images (list): Sequência de imagens para animação.
            move_up_sound (Sound): Som tocado ao pular.
            *groups: Grupos de sprites.
        """
        super().__init__()
        self._layer = 10
        self.state = PlayerState.IDLE

        # Animação
        self.images = player_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.animation_step = config.PLAYER_ANIMATION_STEP

        # Posição Inicial
        self.rect = self.image.get_rect()
        self.rect.centerx = config.SCREEN_WIDTH // 4
        self.rect.centery = config.SCREEN_HEIGHT // 2 + config.SCREEN_VERTICAL_OFFSET

        # Física
        self.change_y = 0
        self.move_up_sound = move_up_sound

        # --- Configuração da Máscara de Colisão (Hitbox) ---
        # Cria uma superfície vazia do tamanho do pássaro
        mask = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Desenha um círculo branco no centro para representar o corpo
        # Isso cria uma colisão mais "justa" que ignora as pontas das asas
        mask_center = (self.rect.width // 2, self.rect.height // 2)
        mask_radius = min(self.rect.width, self.rect.height) // 2
        pygame.draw.circle(mask, (255, 255, 255), mask_center, mask_radius)

        # Converte a superfície desenhada em uma máscara de bits para colisão pixel-perfect
        self.mask = pygame.mask.from_surface(mask)

    def handle_animation(self, dt: float) -> None:
        """Cicla entre as imagens do pássaro baseada no tempo (dt)."""
        if self.animation_step < 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0

            self.image = self.images[self.image_index]
            self.animation_step = config.PLAYER_ANIMATION_STEP
        else:
            self.animation_step -= dt

    def handle_movement(self, dt: float) -> None:
        """
        Aplica gravidade e limites de tela.

        A gravidade aumenta a velocidade de queda (change_y) constantemente,
        limitada por uma velocidade terminal (PLAYER_DOWN_SPEED_LIMIT).
        Também impede que o pássaro voe para fora do topo da tela.

        Durante o estado DYING, o pássaro continua sofrendo ação da gravidade
        até sair da tela ou atingir o chão, momento em que transita para DEAD.
        """
        self.change_y += config.GRAVITY * dt

        # Limita a velocidade de queda (Terminal Velocity)
        if self.change_y > config.PLAYER_DOWN_SPEED_LIMIT:
            self.change_y = config.PLAYER_DOWN_SPEED_LIMIT

        # Aplica o movimento se não estiver batendo no teto (y > 0)
        if (self.rect.y + round(self.change_y)) > 0:
            self.rect.y += round(self.change_y)
        else:
            # Zera a inércia se bater no teto
            self.change_y = 0

        # Transição automática de DYING para DEAD ao sair da tela/chão
        # O player precisa estar se movento para baixo (gravidade) e não para cima (kick para cima)
        bottom_limit = config.SCREEN_HEIGHT + config.SCREEN_VERTICAL_OFFSET * 2

        if self.rect.bottom > bottom_limit and self.change_y >= 0 and self.state == PlayerState.DYING:
            self.state = PlayerState.DEAD
            self.rect.bottom = bottom_limit  # Clamping (Trava perfeita no pixel)

    def handle_death(self):
        """
        Altera o estado do jogador e aplica efeitos estéticos

        Kick da morte
        Efeito visual de morte (Jogador fica de cabeça para baixo)
        """
        # Muda o estado do jogador
        self.state = PlayerState.DYING

        # Efeito físico ("kick" para cima)
        self.move_up()

        # Efeito visual de morte (cabeça para baixo)
        self.image = pygame.transform.flip(self.image, flip_x=False, flip_y=True)

    def move_up(self) -> None:
        """
        Aplica um impulso vertical instantâneo (Pulo).

        Define a velocidade vertical como negativa para subir.
        """
        self.change_y = -config.PLAYER_IMPULSE

        # Não toca o som quando DYING
        if self.state != PlayerState.DYING:
            self.move_up_sound.play()

    def update(self, dt) -> None:
        """
        Atualiza a lógica do jogador baseada em seu estado atual.

        - IDLE: Não aplica física, apenas desenha.
        - FLYING: Aplica física (gravidade) e animação.
        - DYING: Gravidade ativa (cai), mas Animação parada (asas estáticas).
        - DEAD: Estático total
        """
        # Física aplica-se tanto voando quanto morrendo (caindo)
        if self.state in [PlayerState.FLYING, PlayerState.DYING]:
            self.handle_movement(dt)

        # Animação só ocorre se estiver vivo e voando/esperando
        if self.state not in [PlayerState.DYING, PlayerState.DEAD]:
            self.handle_animation(dt)
