import pygame
import random
import config
from constants import *

# Clase que representa el objetivo a golpear
class Target:
    def __init__(self, w=30, h=30, color=(80,255,80)):
        # Inicializa el objetivo con tamaño y color, y lo coloca en una posición aleatoria
        self.w = w  # Ancho del objetivo
        self.h = h  # Alto del objetivo
        self.color = color  # Color del objetivo
        self.rect = self.random_position()  # Posición inicial aleatoria

    # Genera una posición aleatoria válida para el objetivo
    def random_position(self):
        # Usar la utilidad para asegurar que el objetivo esté dentro del viewport
        return config.get_rect_in_viewport(self.w, self.h, margin_x=50, margin_y=50, ground=True)

    # Reaparece el objetivo en una nueva posición aleatoria
    def respawn(self):
        self.rect = self.random_position()

    # Dibuja el objetivo en pantalla
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
