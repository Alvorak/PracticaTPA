import pygame
from .. import config
from .. constants import *

# Clase que representa el objetivo a golpear
class Target:
    """Clase que representa el objetivo a golpear en el juego."""
    def __init__(self, w=30, h=30, color=(80,255,80)):
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
        return config.get_rect_in_viewport(self.w, self.h, margin_x=50, margin_y=50, ground=True)
        

    # Reaparece el objetivo en una nueva posición aleatoria
    def respawn(self):
        """Sirve para reaparecer el objetivo en una nueva posición aleatoria."""
        self.rect = self.random_position()

    # Dibuja el objetivo en pantalla
    def draw(self, surface):
        """Dibuja el objetivo en la superficie dada."""
        pygame.draw.rect(surface, self.color, self.rect)
