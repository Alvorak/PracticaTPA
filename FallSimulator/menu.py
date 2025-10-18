import pygame
import config
from constants import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        self.options = MENU_OPTIONS
        self.title_font = pygame.font.SysFont("Comic Sans MS", 100, bold=True) #para el titulo del juego
        self.selected = 0

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        # La acción está en la segunda parte de la tupla
                        _, action = self.options[self.selected]
                        return action

            self.draw()
            pygame.display.flip()
            clock.tick(30)

    def draw(self):
        self.screen.fill((20, 20, 20))
        #Dibujar el título del juego
        title_text = config.GameTitle
        title_surf = self.title_font.render(title_text, True, (255, 215, 0))  # dorado
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_surf, title_rect)
        # Dibujar las opciones del menú
        for i, (text, _) in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            surf = self.font.render(text, True, color)
            rect = surf.get_rect(center=(self.screen.get_width()//2, 250 + i * 80))
            self.screen.blit(surf, rect)
