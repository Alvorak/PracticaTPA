import pygame
from .. import config
from .. constants import *

class Platform:
    """Clase simple para una plataforma estática"""
    def __init__(self, x, y, w, h, color=(100, 100, 120)):
        """Constructor de la plataforma"""
        self.rect = pygame.Rect(x, y, w, h)
        """Rectángulo que representa la posición y tamaño de la plataforma"""
        self.color = color
        """Color de la plataforma"""

    def draw(self, surface):
        """Dibuja la plataforma en la superficie dada"""
        # Dibuja la plataforma
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.line(surface, (150, 150, 180), self.rect.topleft, self.rect.topright, 3) #línea superior de la estructura