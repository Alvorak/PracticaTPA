"""
	Para ejecutar el juego, hay que estar en el directorio FallSimulator/src y ejecutar:
        python -m fall_simulator
        para el modo demo (auto-juego simplificado):
        python -m fall_simulator --demo
        y para los test: pytest
"""
import pygame
import sys
from .menu import Menu
from .game import Game
from . import config
from .constants import GameTitle

def main(demo=False):
    pygame.init()

    # Configuración de pantalla
    if config.FULLSCREEN:
        display_info = pygame.display.Info()
        screen = pygame.display.set_mode(
            (display_info.current_w, display_info.current_h), pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode((config.VIEWPORT_WIDTH, config.VIEWPORT_HEIGHT))
    pygame.display.set_caption(GameTitle)

    estado = "menu"
    """El estado inicial del juego es el menú."""
    menu = Menu(screen)
    game = Game(screen)

    # Modo demo: auto-juego simplificado
    if demo:
        estado = "juego"
        game.auto_play()
        pygame.quit()
        return
    # Bucle normal
    while estado != "salir":
        if estado == "menu":
            estado = menu.run()
        elif estado == "juego":
            estado = game.run()

    pygame.quit()

if __name__ == "__main__":
    demo = "--demo" in sys.argv
    """Probamos una demo si se pasa el argumento --demo"""
    main(demo)
