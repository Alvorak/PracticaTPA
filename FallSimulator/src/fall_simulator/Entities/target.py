import pygame
import random
from .. import config
from ..constants import *


# Clase que representa el objetivo a golpear
class Target:
    """Clase que representa el objetivo a golpear en el juego."""

    def __init__(self, w=30, h=30, color=(80, 255, 80)):
        """Constructor del objetivo, inicializando tamaño, color y posición aleatoria."""
        # Inicializa el objetivo con tamaño y color, y lo coloca en una posición aleatoria
        self.w = w  # Ancho del objetivo
        """Ancho del objetivo."""
        self.h = h  # Alto del objetivo
        """Alto del objetivo."""
        self.color = color  # Color del objetivo
        """Color del objetivo."""
        self.rect = self.random_position()  # Posición inicial aleatoria
        """Posición inicial aleatoria del objetivo."""

    # Genera una posición aleatoria válida para el objetivo
    def random_position(self):
        """Una posición aleatoria en la que aparecerá el objetivo."""
        # Usar la utilidad para asegurar que el objetivo esté dentro del viewport
        return config.get_rect_in_viewport(
            self.w, self.h, margin_x=50, margin_y=50, ground=True
        )

    # Reaparece el objetivo en una nueva posición aleatoria
    def respawn(self):
        """Sirve para reaparecer el objetivo en una nueva posición aleatoria."""
        self.rect = self.random_position()

    def respawn_away(self, player_rect, min_y_from_ground=150, min_x_distance=200):
        """Reaparece el objetivo en una posición alejada del jugador y a una altura mínima.
        player_rect: pygame.Rect del jugador para calcular distancia mínima en X.
        min_y_from_ground: píxeles mínimos desde el suelo hacia arriba para colocar el objetivo.
        min_x_distance: distancia mínima en X respecto al centro del jugador.
        """
        w, h = self.w, self.h
        # calcular límites
        ground_y = config.VIEWPORT_HEIGHT - config.GROUND_HEIGHT
        max_y = max(0, ground_y - min_y_from_ground - h)
        # si no cabe con min_y_from_ground, usar la funcionalidad normal
        if max_y <= 0:
            self.rect = self.random_position()
            return

        # intentar hasta N veces encontrar una posición suficientemente alejada
        for _ in range(30):
            x = random.randint(50, max(50, config.VIEWPORT_WIDTH - 50 - w))
            # y en rango [0, max_y]
            y = random.randint(0, max_y)
            candidate = pygame.Rect(x, y, w, h)
            if abs(candidate.centerx - player_rect.centerx) >= min_x_distance:
                self.rect = candidate
                return

        # fallback: posición aleatoria clásica
        self.rect = self.random_position()

    # Dibuja el objetivo en pantalla
    def draw(self, surface):
        """Dibuja el objetivo en la superficie dada."""
        pygame.draw.rect(surface, self.color, self.rect)
