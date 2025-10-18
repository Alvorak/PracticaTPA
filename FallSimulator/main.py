import pygame
from menu import Menu
from game import Game
import config
from constants import GameTitle

def main():
    pygame.init()

    # Configuración inicial de pantalla
    if config.FULLSCREEN:
        display_info = pygame.display.Info()
        screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((config.VIEWPORT_WIDTH, config.VIEWPORT_HEIGHT))
    pygame.display.set_caption(GameTitle)

    estado = "menu"
    menu = Menu(screen)
    game = Game(screen)

    while estado != "salir":
        if estado == "menu":
            estado = menu.run()
        elif estado == "juego":
            estado = game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
