import pygame
import sys
import random
from . import config
from .constants import *
from .Entities.player import Player
from .Entities.projectile import Projectile
from .Entities.target import Target
from .Entities.platform import Platform
from .levels import load_levels

class Game:
    """Clase principal del juego. Maneja el bucle del juego, actualizaciones y renderizado (gameloop)"""
    def __init__(self, screen, lifes=3, puntos=0):
        """Constructor de la clase Game."""
        self.screen = screen # Pantalla principal
        """Pantalla principal del juego."""
        self.clock = pygame.time.Clock() # Reloj para controlar FPS
        """Reloj para los FPS del juego."""
        self.running = True
        """Chequea si el juego está corriendo."""
        self.lifes = lifes
        """Vidas del jugador."""
        self.puntos = puntos
        """Puntos del jugador."""
        # Cargar niveles
        try:
            self.levels = load_levels() # Carga niveles desde JSON
        except Exception:
            # Si no se encuentra el archivo o hay error, usar un fallback mínimo
            self.levels = []
        self.current_level_index = 0
        self.escape_pulsado_time = 0.0
        """El tiempo en segundos que hay que mantener ESC pulsado para salir del juego."""
      
        if screen is not None:
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("Arial Unicode MS", 20) # Fuente para texto en pantalla
            """Fuente para el texto en pantalla."""

        else:  #para el modo test sin pantalla
            self.clock = None
            self.font = None


    def run(self):
        """Método principal del bucle del juego."""
        #Configuración de pantalla
        screen_w, screen_h = self.screen.get_size()
        """Ancho y alto de la pantalla."""

        # Crear superficie del viewport jugable
        viewport_w = config.VIEWPORT_WIDTH
        """Ancho del viewport jugable."""
        viewport_h = screen_h
        """Alto del viewport jugable."""
        config.VIEWPORT_HEIGHT = viewport_h
        """Altura del viewport jugable."""
        viewport = pygame.Surface((viewport_w, viewport_h))
        """Superficie del viewport jugable."""
        viewport_x = (screen_w - viewport_w) // 2
        """Posición X del viewport en la pantalla."""
        viewport_y = 0
        """Posición Y del viewport en la pantalla."""

        # Inicializar entidades
        player = Player(viewport_w // 3, viewport_h - config.GROUND_HEIGHT - 90)
        """jugador del juego"""
        projectiles = []
        """Lista de proyectiles activos."""
        # Construir plataformas y objetivos a partir del nivel actual
        ground_y = viewport_h - config.GROUND_HEIGHT # Posición Y del suelo
        if self.levels and 0 <= self.current_level_index < len(self.levels): # Si hay niveles cargados
            lvl = self.levels[self.current_level_index] # Nivel actual
            platforms = lvl.create_platforms(viewport_w, ground_y, Platform) # crear plataformas
            # crear lista de objetivos segun num_targets 
            targets = [Target() for _ in range(lvl.num_targets)] 
            current_points_needed = lvl.points_needed # puntos necesarios para completar el nivel
        else:
            # Fallback: plataformas hardcodeadas (comportamiento original)
            platforms = [
                Platform(100, ground_y - 150, 200, 20),
                Platform(viewport_w // 2 - 100, ground_y - 300, 200, 20),
                Platform(viewport_w - 300, ground_y - 450, 200, 20)
            ]
            targets = [Target()]
            current_points_needed = 999999

        # ground_y ya inicializado arriba
        arrow_keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        """Flechas de dirección para disparar."""
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

            # Colisiones con los objetivos
            hit_index = None
            for i, t in enumerate(targets):
                if any(proj.rect.colliderect(t.rect) for proj in projectiles):
                    hit_index = i
                    break
            if hit_index is not None:
                targets[hit_index].respawn()
                self.puntos += 1

                # Comprobar si alcanzamos el umbral para pasar de nivel
                if self.levels and self.current_level_index < len(self.levels): # Si hay niveles cargados
                    lvl = self.levels[self.current_level_index] # Nivel actual
                    if self.puntos >= lvl.points_needed: # Si se alcanzaron los puntos necesarios
                        # Mostrar pantalla de transición y cargar siguiente nivel
                        self._show_next_level_popup(self.screen, viewport, viewport_x, viewport_y, self.current_level_index + 1)
                        self.current_level_index += 1 # avanzar al siguiente nivel
                        # reset de estado que puede quedar activo al cambiar de nivel (asi evitamos apariciones raras)
                        projectiles = [] 
                        shoot_timer = 0.0
                        # limpiar teclas de flecha presionadas para evitar disparo continuo
                        arrow_keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
                        # resetear velocidades y posición ligera del jugador para evitar inercia entre niveles
                        try:
                            player.vx = 0 
                            player.vy = 0
                        except Exception:
                            pass
                        # si hay siguiente nivel, recargar plataformas y targets
                        if self.current_level_index < len(self.levels):
                            lvl = self.levels[self.current_level_index]
                            platforms = lvl.create_platforms(viewport_w, ground_y, Platform)
                            targets = [Target() for _ in range(lvl.num_targets)]
                        else:
                            # No hay más niveles -> mostrar mensaje de victoria y game over
                            self._show_victory_popup(self.screen, viewport, viewport_x, viewport_y)
                            return "salir"

            # Dibujo 
            viewport.fill(config.BG_COLOR)
            pygame.draw.rect(viewport, config.GROUND_COLOR, (0, viewport_h - config.GROUND_HEIGHT, viewport_w, config.GROUND_HEIGHT))
            for platform in platforms:
                platform.draw(viewport)
            player.draw(viewport)
            for proj in projectiles:
                proj.draw(viewport)
            for t in targets:
                t.draw(viewport)

            # Info debug => texto en pantalla
            lines = [
                "Controles: A/D = mover | Space/W = saltar | S = agacharse | Flechas = disparar (puedes combinar para diagonales)",
                f"Vel: {player.vx:.0f}px/s | Suelo: {'Sí' if player.on_ground else 'No'} | Agachado: {'Sí' if player.crouching else 'No'}",
                f"Vidas: {self.lifes} | Puntos : {self.puntos}"
            ]
            """Lista de líneas de texto para mostrar en pantalla."""
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

    def _show_next_level_popup(self, screen, viewport, viewport_x, viewport_y, next_level_number): 
        """Muestra un overlay modal indicando el siguiente nivel y espera interacción del jugador."""
        if screen is None: # Si no hay pantalla, no se puede mostrar el popup
            return
        overlay = pygame.Surface(viewport.get_size(), pygame.SRCALPHA) # Superficie transparente
        clock = self.clock or pygame.time.Clock() # Reloj para controlar FPS
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            # Dibujar overlay
            overlay.fill((0, 0, 0, 180))
            viewport.blit(overlay, (0, 0))
            title = self.font.render(f"Nivel {next_level_number} completado!", True, (255, 255, 255))
            hint = self.font.render("Pulsa Espacio o haz click para continuar", True, (200, 200, 200))
            viewport.blit(title, (viewport.get_width() // 2 - title.get_width() // 2, viewport.get_height() // 2 - 30))
            viewport.blit(hint, (viewport.get_width() // 2 - hint.get_width() // 2, viewport.get_height() // 2 + 10))
            screen.fill((0, 0, 0))
            screen.blit(viewport, (viewport_x, viewport_y))
            pygame.display.flip()
            clock.tick(30)

    def _show_victory_popup(self, screen, viewport, viewport_x, viewport_y):
        """Muestra un overlay final indicando victoria y espera interacción para salir."""
        if screen is None: # Si no hay pantalla, no se puede mostrar el popup
            return
        overlay = pygame.Surface(viewport.get_size(), pygame.SRCALPHA) # Superficie transparente
        clock = self.clock or pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            # Dibujar overlay
            overlay.fill((0, 0, 0, 200))
            viewport.blit(overlay, (0, 0))
            title = self.font.render("¡Has completado todos los niveles!", True, (255, 220, 100)) #game over
            hint = self.font.render("Pulsa Espacio para salir", True, (220, 220, 220))
            viewport.blit(title, (viewport.get_width() // 2 - title.get_width() // 2, viewport.get_height() // 2 - 30))
            viewport.blit(hint, (viewport.get_width() // 2 - hint.get_width() // 2, viewport.get_height() // 2 + 10))
            screen.fill((0, 0, 0))
            screen.blit(viewport, (viewport_x, viewport_y))
            pygame.display.flip()
            clock.tick(30)
    #PARA EL MODO TEST que pruebe jugar solo
    def auto_play(self, steps=200):
            """
            Demo automática: mueve al personaje de formna aleatoria y dispara aleatoriamente. 
            Solo para pruebas automáticas y testing.
            steps: número de pasos (movimientos) de actualización a simular
            """
            if self.screen is None:
                return  # no se puede jugar sin pantalla

            # Configuración inicial igual que en run()
            screen_w, screen_h = self.screen.get_size()
            viewport_w = config.VIEWPORT_WIDTH
            viewport_h = screen_h
            config.VIEWPORT_HEIGHT = viewport_h
            viewport = pygame.Surface((viewport_w, viewport_h))
            viewport_x = (screen_w - viewport_w) // 2
            viewport_y = 0

            player = Player(viewport_w // 3, viewport_h - config.GROUND_HEIGHT - 90)
            projectiles = []
            target = Target()

            ground_y = viewport_h - config.GROUND_HEIGHT
            
            platforms = [
                Platform(100, ground_y - 150, 200, 20),
                Platform(viewport_w // 2 - 100, ground_y - 300, 200, 20),
                Platform(viewport_w - 300, ground_y - 450, 200, 20)
            ]
            """Lista de plataformas en el juego."""

            shoot_timer = 0.0 # tiempo desde el último disparo
            shoot_interval = 0.15 # intervalo mínimo entre disparos
            """Intervalo mínimo entre disparos."""

            for step in range(steps): # cada paso 
                dt = self.clock.tick(config.FPS) / 1000.0 # tiempo delta
                """Tiempo delta entre frames en segundos."""

                # Movimientos aleatorios
                move_dir = random.choice([-1, 0, 1]) # izquierda, quieto, derecha
                jump = random.random() < 0.1  # saltar aleatoriamente
                crouch = random.random() < 0.05# agacharse aleatoriamente

                # Aplicamos el movimiento al jugador
                player.vx = move_dir * player.speed
                if jump:
                    player.jump()
                if crouch:
                    player.crouch({'S': True}) # simulamos tecla S presionada

                player.apply_physics(dt, player.vx, platforms, ground_y) # actualizar física del jugador => movimiento y colisiones

                # Disparo aleatorio
                if random.random() < 0.3:
                    #elegimos aletoriamente una dirección de disparo en 8 direcciones (incluyendo diagonales)
                    dx = random.choice([-1, 0, 1]) 
                    dy = random.choice([-1, 0, 1])
                    if dx != 0 or dy != 0:
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

                # Actualizar proyectiles
                for proj in projectiles:
                    proj.update(dt)
                projectiles = [p for p in projectiles if p.active]

                # Colisiones con el objetivo
                hit = any(proj.rect.colliderect(target.rect) for proj in projectiles)
                if hit:
                    target.respawn()
                    self.puntos += 1

                # Dibujo (sin gestión de eventos ni escape)
                viewport.fill(config.BG_COLOR)
                pygame.draw.rect(viewport, config.GROUND_COLOR, (0, viewport_h - config.GROUND_HEIGHT, viewport_w, config.GROUND_HEIGHT))
                for platform in platforms:
                    platform.draw(viewport)
                player.draw(viewport)
                for proj in projectiles:
                    proj.draw(viewport)
                target.draw(viewport)

                self.screen.fill((0,0,0))
                self.screen.blit(viewport, (viewport_x, viewport_y))
                pygame.display.flip()