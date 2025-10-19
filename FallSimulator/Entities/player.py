# player.py
import pygame
import config
from constants import *

# Clase que representa al jugador
class Player:
    def __init__(self, x, y, w=50, h=90, color=config.PLAYER_COLOR):
        # Inicializa el jugador en la posición (x, y) con tamaño y color
        self.base_w = w  # Ancho base
        self.base_h = h  # Alto base
        self.crouch_h = h // 2  # Alto al agacharse
        self.rect = pygame.Rect(int(x), int(y), w, h)  # Rectángulo del jugador
        self.vx = 0.0  # Velocidad horizontal
        self.vy = 0.0  # Velocidad vertical
        self.color = color  # Color del jugador
        self.on_ground = False  # ¿Está en el suelo?
        self.facing = 1  # Dirección a la que mira (1: derecha, -1: izquierda)
        self.crouching = False  # ¿Está agachado?

    # Maneja el input de movimiento horizontal (A/D)
    def handle_input_axis(self, keys):
        ax = 0.0
        if keys[pygame.K_a]:
            ax -= config.MOVE_ACCEL  # Mover a la izquierda
            self.facing = -1
        if keys[pygame.K_d]:
            ax += config.MOVE_ACCEL  # Mover a la derecha
            self.facing = 1
        return ax

    # Hace saltar al jugador si está en el suelo
    def jump(self):
        if self.on_ground:
            self.vy = -config.JUMP_VELOCITY
            self.on_ground = False

    # Corta el salto si se suelta la tecla antes de tiempo
    def short_jump_cut(self):
        if self.vy < 0:
            self.vy *= 0.45

    # Maneja el estado de agacharse
    def crouch(self, keys):
        want_crouch = keys[pygame.K_s]
        if want_crouch and not self.crouching:
            self.crouching = True
            self.rect.height = self.crouch_h
            self.rect.y += self.base_h - self.crouch_h  # Baja el rectángulo
        elif not want_crouch and self.crouching:
            self.crouching = False
            old_bottom = self.rect.bottom
            self.rect.height = self.base_h
            self.rect.bottom = old_bottom  # Sube el rectángulo
    # Aplica física al jugador (movimiento y colisiones)
    def apply_physics(self, dt, ax, platforms, ground_y):
        #Parte horizontal
        self.vx += ax * dt
        if ax == 0:
            if self.vx > 0:
                self.vx -= config.FRICTION * dt
                if self.vx < 0:
                    self.vx = 0
            elif self.vx < 0:
                self.vx += config.FRICTION * dt
                if self.vx > 0:
                    self.vx = 0

        self.vx = max(-config.MAX_SPEED, min(config.MAX_SPEED, self.vx))
        self.rect.x += int(self.vx * dt)
        self.check_horizontal_collisions(platforms)

        # Parte vertical
        prev_bottom = self.rect.bottom
        self.vy += config.GRAVITY * dt
        self.rect.y += int(self.vy * dt)
        self.check_vertical_collisions(platforms, ground_y, prev_bottom, dt)

        # Mantener dentro del viewport
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = 0
        if self.rect.right > config.VIEWPORT_WIDTH:
            self.rect.right = config.VIEWPORT_WIDTH
            self.vx = 0

    #Cplisiones horizontales => para plataformas
    def check_horizontal_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                vertical_overlap = min(self.rect.bottom, platform.rect.bottom) - max(self.rect.top, platform.rect.top)
                if vertical_overlap <= 0:
                    continue
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                elif self.vx < 0:
                    self.rect.left = platform.rect.right
                self.vx = 0

    #Colisiones verticales => para plataformas y suelo
    def check_vertical_collisions(self, platforms, ground_y, prev_bottom, dt):
        # --- Suelo base ---
        if self.rect.bottom >= ground_y:
            if self.vy > 0:  #solo frena si cae => evita bugs al saltar justo en el suelo
                self.vy = 0
            self.rect.bottom = ground_y
            self.on_ground = True
        else:
            self.on_ground = False

        snap_margin = max(3, abs(int(self.vy * dt)), 1) # Margen para "aterrizar" en plataformas rápidas => no traspasarlas

        #Plataformas del juego y sus colisiones
        for platform in platforms:
            plat_top = platform.rect.top
            # detectar cruzando top desde arriba
            if self.vy >= 0 and prev_bottom <= plat_top + snap_margin and self.rect.bottom >= plat_top - snap_margin:
                if self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                    self.rect.bottom = plat_top
                    self.vy = 0
                    self.on_ground = True
                    break


    
    
    #Draw que muestra al jugador en pantalla
    def draw(self, surface): # Dibuja el jugador en pantalla
        pygame.draw.rect(surface, self.color, self.rect)
        head_w = 10
        cx = self.rect.centerx + (self.facing * (self.rect.width // 2 + 1))
        cy_top = self.rect.top + 18
        points = [(cx, cy_top), (cx + (-self.facing)*head_w, cy_top+7), (cx + (-self.facing)*head_w, cy_top-7)]
        pygame.draw.polygon(surface, (200,200,200), points) # Dibuja un triangulo como orientacion de los ojos del jugador => mira hacia donde se mueve