import pygame
import random
import config

class Target:
    def __init__(self, w=30, h=30, color=(80,255,80)):
        self.w = w
        self.h = h
        self.color = color
        self.rect = self.random_position()

    def random_position(self):
        x = random.randint(50, config.SCREEN_WIDTH - 50 - self.w)
        min_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - 200
        max_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - self.h
        y = random.randint(min_y, max_y)
        return pygame.Rect(x, y, self.w, self.h)

    def respawn(self):
        self.rect = self.random_position()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
