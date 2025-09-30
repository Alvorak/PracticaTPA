# main.py
import pygame
import sys
import random
import config
from constants import *
from Entities.player import Player
from Entities.projectile import Projectile
from Entities.target import Target
# Función principal - El Game Loop del juego
def main():
    pygame.init()
    #Obtener resolución de pantalla si FULLSCREEN 
    if config.FULLSCREEN: #Si es pantalla completa, obtener resolución actual
        display_info = pygame.display.Info()
        screen_w, screen_h = display_info.current_w, display_info.current_h
        config.SCREEN_WIDTH = screen_w
        config.SCREEN_HEIGHT = screen_h
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    else:# Modo ventana
        screen_w, screen_h = config.VIEWPORT_WIDTH, config.VIEWPORT_HEIGHT
        config.SCREEN_WIDTH = screen_w
        config.SCREEN_HEIGHT = screen_h
        screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(GameTitle) # Título del Juego
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial Unicode MS", 20)

    #Crear superficie del viewport jugable
    #Ajustar viewport para que ocupe todo el alto de la pantalla
    viewport_w = config.VIEWPORT_WIDTH
    viewport_h = screen_h  # Ocupa todo el alto de la pantalla
    config.VIEWPORT_HEIGHT = viewport_h  # Actualiza el valor global
    viewport = pygame.Surface((viewport_w, viewport_h))
    # Coordenadas para centrar el viewport horizontalmente
    viewport_x = (screen_w - viewport_w) // 2
    viewport_y = 0

    #Inicializar entidades usando el viewport (Utilizar config para límites)
    player = Player(viewport_w // 3, viewport_h - config.GROUND_HEIGHT - 90)
    projectiles = []
    target = Target()

    running = True # Para controlar el bucle principal del juego, false para salir
    # Llevar registro de qué flechas están presionadas
    arrow_keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    shoot_timer = 0.0
    shoot_interval = 0.15  # segundos entre disparos
    while running:
        dt = clock.tick(config.FPS) / 1000.0 
        keys = pygame.key.get_pressed()
        # Determinar dirección de disparo según flechas (puede ser diagonal)
        shoot_x = (1 if arrow_keys[pygame.K_RIGHT] else 0) + (-1 if arrow_keys[pygame.K_LEFT] else 0)
        shoot_y = (1 if arrow_keys[pygame.K_DOWN] else 0) + (-1 if arrow_keys[pygame.K_UP] else 0)
        shoot_dir = (shoot_x, shoot_y) if shoot_x or shoot_y else None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    player.jump()
                # Flecha presionada: actualizar estado
                if event.key in arrow_keys:
                    arrow_keys[event.key] = True
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_w):
                    player.short_jump_cut()
                # Flecha soltada: actualizar estado
                if event.key in arrow_keys:
                    arrow_keys[event.key] = False

        # Disparar continuamente mientras se mantenga alguna flecha
        if shoot_dir:
            shoot_timer += dt
            while shoot_timer >= shoot_interval:
                dx, dy = shoot_dir
                mag = (dx**2 + dy**2) ** 0.5
                dx /= mag
                dy /= mag
                px = player.rect.centerx
                py = player.rect.centery
                proj = Projectile(px, py, 0)
                proj.vx = 600 * dx
                proj.vy = 600 * dy
                def custom_update(self, dt):
                    self.rect.x += int(self.vx * dt)
                    self.rect.y += int(self.vy * dt)
                    # Limitar proyectil al área jugable (viewport)
                    if (self.rect.right < 0 or self.rect.left > viewport_w or
                        self.rect.bottom < 0 or self.rect.top > viewport_h):
                        self.active = False
                proj.update = custom_update.__get__(proj)
                projectiles.append(proj)
                shoot_timer -= shoot_interval
        else:
            shoot_timer = 0.0

        ax = player.handle_input_axis(keys)
        player.crouch(keys)  # Manejar agacharse
        player.apply_physics(dt, ax)

        # Actualizar proyectiles
        for proj in projectiles:
            proj.update(dt)
        # Eliminar proyectiles inactivos
        projectiles = [p for p in projectiles if p.active]

        # Verificar colisión con el objetivo
        hit = False
        for proj in projectiles:
            if proj.rect.colliderect(target.rect):
                proj.active = False
                hit = True
        if hit:
            target.respawn()

        #Dibujo: primero limpiar viewport
        viewport.fill(config.BG_COLOR)
        ground_rect = pygame.Rect(0, viewport_h - config.GROUND_HEIGHT, viewport_w, config.GROUND_HEIGHT)
        pygame.draw.rect(viewport, config.GROUND_COLOR, ground_rect)
        player.draw(viewport)
        # Dibujar flecha de dirección de disparo si existe
        if shoot_dir:
            dx, dy = shoot_dir
            mag = (dx**2 + dy**2) ** 0.5
            if mag:
                dx /= mag
                dy /= mag
                arrow_len = 50
                cx = player.rect.centerx
                cy = player.rect.centery
                tip = (int(cx + dx * arrow_len), int(cy + dy * arrow_len))
                pygame.draw.line(viewport, (80,200,255), (cx, cy), tip, 5)
                # Dibujar cabeza de la flecha
                perp = (-dy, dx)
                head_len = 12
                head_w = 7
                left = (int(tip[0] - dx * head_len + perp[0] * head_w), int(tip[1] - dy * head_len + perp[1] * head_w))
                right = (int(tip[0] - dx * head_len - perp[0] * head_w), int(tip[1] - dy * head_len - perp[1] * head_w))
                pygame.draw.polygon(viewport, (80,200,255), [tip, left, right])
        for proj in projectiles:
            proj.draw(viewport)
        target.draw(viewport)

        lines = [
            "Controles: A/D = mover | Space/W = saltar | S = agacharse | Flechas = disparar (puedes combinar para diagonales)",
            f"Vel: {player.vx:.0f} px/s | En suelo: {'Sí' if player.on_ground else 'No'} | Agachado: {'Sí' if player.crouching else 'No'} | Proyectiles: {len(projectiles)} | Objetivo: verde"
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, config.TEXT_COLOR)
            viewport.blit(txt, (10, 10 + i*18))

        #Limpiar pantalla y dibujar bandas negras
        screen.fill((0,0,0))  # Bandas negras
        # Blitear viewport centrado
        screen.blit(viewport, (viewport_x, viewport_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
