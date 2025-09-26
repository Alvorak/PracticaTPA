import pygame
import config

class Projectile:
    def __init__(self, x, y, direction, speed=600, w=12, h=6, color=(255,255,80)):
        self.rect = pygame.Rect(int(x), int(y), w, h)
        self.direction = direction
        self.speed = speed
        self.color = color
        self.active = True

    def update(self, dt):
        self.rect.x += int(self.speed * self.direction * dt)
        if self.rect.right < 0 or self.rect.left > config.SCREEN_WIDTH:
            self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
