# Para tener todas las constantes en un solo lugar
"""
Constantes globales del juego.
Warning: cuidado con que toquetees aquí, puede romper cosas.
"""

# Título del juego
GameTitle = "Fall Simulator"

# Variables dinámicas de pantalla (se ajustan en main.py)
SCREEN_WIDTH = 0  # Se define en main.py si FULLSCREEN=True
SCREEN_HEIGHT = 0

# Resolución por defecto del área jugable
VIEWPORT_WIDTH = 900
VIEWPORT_HEIGHT = 700

# Modo pantalla completa
FULLSCREEN = True  # Cambia a False para modo ventana

# Físicas y juego
FPS = 60
GROUND_HEIGHT = 80
GRAVITY = 2500.0
MOVE_ACCEL = 8000.0
MAX_SPEED = 380.0
FRICTION = 6000.0
JUMP_VELOCITY = 900.0

# Colores
BG_COLOR = (30, 30, 40)
GROUND_COLOR = (40, 40, 50)
PLAYER_COLOR = (220, 40, 40)
TEXT_COLOR = (230, 230, 230)
