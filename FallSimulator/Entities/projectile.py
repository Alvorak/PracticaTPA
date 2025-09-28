
import pygame
import config

# Clase que representa un proyectil disparado por el jugador
class Projectile:
    def __init__(self, x, y, direction, speed=600, w=12, h=6, color=(255,255,80)):
        # Inicializa el proyectil en la posición (x, y) con dirección y velocidad
        self.rect = pygame.Rect(int(x), int(y), w, h)  # Rectángulo del proyectil
        self.direction = direction  # Dirección de movimiento (1: derecha, -1: izquierda)
        self.speed = speed  # Velocidad del proyectil
        self.color = color  # Color del proyectil
        self.active = True  # Si el proyectil está activo

    # Actualiza la posición del proyectil
    def update(self, dt):
        self.rect.x += int(self.speed * self.direction * dt)
        # Desactiva el proyectil si sale de la pantalla
        if self.rect.right < 0 or self.rect.left > config.SCREEN_WIDTH:
            self.active = False

    # Dibuja el proyectil en pantalla
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
