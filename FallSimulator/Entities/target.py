import pygame
import random
import config

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
        x = random.randint(50, config.SCREEN_WIDTH - 50 - self.w)
        min_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - 200
        max_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - self.h
        y = random.randint(min_y, max_y)
        return pygame.Rect(x, y, self.w, self.h)

    # Reaparece el objetivo en una nueva posición aleatoria
    def respawn(self):
        self.rect = self.random_position()

    # Dibuja el objetivo en pantalla
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
