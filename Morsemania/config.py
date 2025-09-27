MORSE_CODE = {
	'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
	'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
	'M': '--', 'N': '-.', 'Ñ': '--.--', 'O': '---', 'P': '.--.', 'Q': '--.-',
	'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
	'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
	'3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}
MORSE_DECODE = {v: k for k, v in MORSE_CODE.items()}

import pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Configuración de tiempos y barra de progreso
SHOW_LETTER_TIME = 8  # segundos para limpiar pantalla
AUTO_TRANSLATE_TIME = 1  # segundos para traducir automáticamente
PROGRESS_MAX = 0.3  # segundos para distinguir punto/raya
PROGRESS_RECT = (50, 50, 300, 30)  # x, y, ancho, alto

# Fuente
FONT_NAME = 'consolas'
FONT_SIZE = 48
