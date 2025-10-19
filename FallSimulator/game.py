import pygame
import sys
import config
from constants import *
from Entities.player import Player
from Entities.projectile import Projectile
from Entities.target import Target
from Entities.platform import Platform

class Game:
    def __init__(self, screen, lifes=3, puntos=0):
        self.screen = screen # Pantalla principal
        self.clock = pygame.time.Clock() # Reloj para controlar FPS
        self.font = pygame.font.SysFont("Arial Unicode MS", 20) # Fuente para texto en pantalla
        self.running = True
        self.lifes = lifes
        self.puntos = puntos

    def run(self):
        #Configuración de pantalla
        screen_w, screen_h = self.screen.get_size()

        # Crear superficie del viewport jugable
        viewport_w = config.VIEWPORT_WIDTH
        viewport_h = screen_h
        config.VIEWPORT_HEIGHT = viewport_h
        viewport = pygame.Surface((viewport_w, viewport_h))
        viewport_x = (screen_w - viewport_w) // 2
        viewport_y = 0

        # Inicializar entidades
        player = Player(viewport_w // 3, viewport_h - config.GROUND_HEIGHT - 90)
        projectiles = []
        target = Target()

        ground_y = viewport_h - config.GROUND_HEIGHT
        platforms = [
            Platform(100, ground_y - 150, 200, 20),
            Platform(viewport_w // 2 - 100, ground_y - 300, 200, 20),
            Platform(viewport_w - 300, ground_y - 450, 200, 20)
        ]

        arrow_keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        shoot_timer = 0.0
        shoot_interval = 0.15
        
        escape_hold_time = getattr(config, "ESCAPE_HOLD_TIME", 5.0)
        # Bucle principal del juego
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            keys = pygame.key.get_pressed()
            # Manejo de la tecla ESC para salir
            if keys[pygame.K_ESCAPE]:
                self.escape_pulsado_time += dt
                # Si se supera el límite, salir del juego
                if self.escape_pulsado_time >= config.escape_limite:
                    pygame.quit()
                    sys.exit()
            else:
                self.escape_pulsado_time = 0.0  # Reinicia si suelta la tecla

            # Eventos normales
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_w):
                        player.jump()
                    if event.key in arrow_keys:
                        arrow_keys[event.key] = True
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_SPACE, pygame.K_w):
                        player.short_jump_cut()
                    if event.key in arrow_keys:
                        arrow_keys[event.key] = False

            # Dirección de disparo
            shoot_x = (1 if arrow_keys[pygame.K_RIGHT] else 0) + (-1 if arrow_keys[pygame.K_LEFT] else 0)
            shoot_y = (1 if arrow_keys[pygame.K_DOWN] else 0) + (-1 if arrow_keys[pygame.K_UP] else 0)
            shoot_dir = (shoot_x, shoot_y) if shoot_x or shoot_y else None

            if shoot_dir:
                shoot_timer += dt
                while shoot_timer >= shoot_interval:
                    dx, dy = shoot_dir
                    mag = (dx**2 + dy**2) ** 0.5
                    dx, dy = dx / mag, dy / mag
                    proj = Projectile(player.rect.centerx, player.rect.centery, 0)
                    proj.vx, proj.vy = 600 * dx, 600 * dy
                    def custom_update(self, dt):
                        self.rect.x += int(self.vx * dt)
                        self.rect.y += int(self.vy * dt)
                        if (self.rect.right < 0 or self.rect.left > viewport_w or
                            self.rect.bottom < 0 or self.rect.top > viewport_h):
                            self.active = False
                    proj.update = custom_update.__get__(proj)
                    projectiles.append(proj)
                    shoot_timer -= shoot_interval
            else:
                shoot_timer = 0.0

            # Actualizaciones de entidades del jugador
            ax = player.handle_input_axis(keys)
            player.crouch(keys)
            player.apply_physics(dt, ax, platforms, ground_y)
            # Actualizar proyectiles
            for proj in projectiles:
                proj.update(dt)
            projectiles = [p for p in projectiles if p.active]

            # Colisiones con el objetivo
            hit = any(proj.rect.colliderect(target.rect) for proj in projectiles)
            if hit:
                target.respawn()
                self.puntos += 1

            # Dibujo 
            viewport.fill(config.BG_COLOR)
            pygame.draw.rect(viewport, config.GROUND_COLOR, (0, viewport_h - config.GROUND_HEIGHT, viewport_w, config.GROUND_HEIGHT))
            for platform in platforms:
                platform.draw(viewport)
            player.draw(viewport)
            for proj in projectiles:
                proj.draw(viewport)
            target.draw(viewport)

            # Info debug => texto en pantalla
            lines = [
                "Controles: A/D = mover | Space/W = saltar | S = agacharse | Flechas = disparar (puedes combinar para diagonales)",
                f"Vel: {player.vx:.0f}px/s | Suelo: {'Sí' if player.on_ground else 'No'} | Agachado: {'Sí' if player.crouching else 'No'}",
                f"Vidas: {self.lifes} | Puntos : {self.puntos}"
            ]
            for i, line in enumerate(lines):
                txt = self.font.render(line, True, config.TEXT_COLOR)
                viewport.blit(txt, (10, 10 + i*18))

            self.screen.fill((0, 0, 0))
            self.screen.blit(viewport, (viewport_x, viewport_y))
            # Mostrar mensaje de aviso (si ESC está pulsado más de 1s)
            if self.escape_pulsado_time > 1.0:
                msg = self.font.render(
                    f"Mantén ESC {config.escape_limite - self.escape_pulsado_time:.1f}s para salir",
                    True, (255, 100, 100)
                )
                msg_rect = msg.get_rect(center=(screen_w // 2, 40))
                self.screen.blit(msg, msg_rect)
            # Actualizar pantalla    
            pygame.display.flip()

        return "salir"
