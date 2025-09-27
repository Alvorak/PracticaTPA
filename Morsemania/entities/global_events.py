import pygame
import sys
import time
from config import *

def check_esc_close(screen, font, esc_pressed_time):
    """
    Comprueba si ESC está pulsado y gestiona el cierre global y el mensaje de aviso.
    Devuelve el nuevo valor de esc_pressed_time (None si se ha soltado ESC).
    """
    esc_duration = None
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if esc_pressed_time is None:
            esc_pressed_time = time.time()
        esc_duration = time.time() - esc_pressed_time
        if esc_duration > 1:
            warning = font.render('¡El juego se cerrará en breves!', True, GREEN)
            screen.blit(warning, (50, HEIGHT - 100))
        if esc_duration > 5:
            pygame.quit()
            sys.exit()
    else:
        esc_pressed_time = None
    return esc_pressed_time
