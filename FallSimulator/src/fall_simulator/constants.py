# Para tener todas las constantes en un solo lugar
"""
Constantes globales del juego.
Warning: cuidado con que toquetees aquí, puede romper cosas.
"""

GameTitle = "Fall Simulator"

"""Esto es el titulo del juego. Cambiarlo aquí cambiará el título en la ventana del juego."""

# Variables dinámicas de pantalla (se ajustan en main.py)
SCREEN_WIDTH = 0  # Se define en main.py si FULLSCREEN=True
"""Anchura de la ventana (funciona si FULLSCREEN está desactivado, osea false)."""
SCREEN_HEIGHT = 0
"""Altura de la ventana (funciona si FULLSCREEN está desactivado, osea false)."""

# Resolución por defecto del área jugable
VIEWPORT_WIDTH = 900
"""Resolución del área jugable (viewport) del juego."""
VIEWPORT_HEIGHT = 700

"""Resolución del área jugable (viewport) del juego."""

# Modo pantalla completa
FULLSCREEN = True  # Cambia a False para modo ventana
"""Pantalla completa o modo ventana."""

# Físicas y juego
FPS = 60
"""Frames por segundo del juego."""
GROUND_HEIGHT = 80
"""Altura del suelo (ground) en píxeles."""
GRAVITY = 2000.0
"""Aceleración de la gravedad en píxeles/segundo²."""
MOVE_ACCEL = 8000.0
"""Aceleración horizontal del jugador en píxeles/segundo²."""
MAX_SPEED = 380.0
"""Velocidad máxima horizontal del jugador en píxeles/segundo."""
FRICTION = 6000.0
"""Rozamiento del jugador en píxeles/segundo²."""
JUMP_VELOCITY = 900.0
"""Velocidad inicial de salto del jugador en píxeles/segundo."""
# Colores
BG_COLOR = (30, 30, 40)
"""Color del fondo del juego."""
GROUND_COLOR = (40, 40, 50)
"""Color del suelo del juego."""
PLAYER_COLOR = (220, 40, 40)
"""Color del jugador."""
TEXT_COLOR = (230, 230, 230)
"""Color del texto."""


MENU_OPTIONS = [ # ("Texto que se muestra", "accion que retorna el menú")
    ("New Game!", "juego"),
    ("Continue :D", "juego"),
    ("Close :(", "salir")
]
"""Opciones del menú principal."""

escape_pulsado_time = 0.0
escape_limite = 4.0  # segundos necesarios para salir del juego
""" Variables para controlar la salida del juego al mantener Escape pulsado."""
