# Configuraciones del juego

# Utilidad para obtener un rectángulo dentro del viewport jugable
import random
import pygame
def get_rect_in_viewport(w, h, margin_x=0, margin_y=0, ground=True):
	"""
	Devuelve un pygame.Rect dentro del área jugable (viewport), respetando márgenes opcionales
	Si ground=True, el rectángulo estará sobre el suelo (no flotando sobre el HUD)
	"""
	x = random.randint(margin_x, VIEWPORT_WIDTH - margin_x - w)
	if ground:
		min_y = margin_y
		max_y = VIEWPORT_HEIGHT - GROUND_HEIGHT - h
	else:
		min_y = margin_y
		max_y = VIEWPORT_HEIGHT - margin_y - h
	y = random.randint(min_y, max_y)
	return pygame.Rect(x, y, w, h)

# Resolución de la ventana jugable (viewport) => WIDTH es ANCHO y HEIGHT es ALTO
VIEWPORT_WIDTH = 900
VIEWPORT_HEIGHT = 0  # Se ajusta dinámicamente en main.py para ocupar todo el alto
VIEWPORT_HEIGHT = 700  # Altura estándar para modo ventana, ajustable durante el juego

# Resolución de la pantalla (se ajusta automáticamente si FULLSCREEN=True)
SCREEN_WIDTH = 0  # Se define en main.py si FULLSCREEN=True
SCREEN_HEIGHT = 0

# Modo pantalla completa
FULLSCREEN = True  # Para definir si jugamos en pantalla completa o ventana

FPS = 60
GROUND_HEIGHT = 80
GRAVITY = 2500.0
MOVE_ACCEL = 8000.0
MAX_SPEED = 380.0
FRICTION = 6000.0
JUMP_VELOCITY = 900.0
BG_COLOR = (30, 30, 40)
GROUND_COLOR = (40, 40, 50)
PLAYER_COLOR = (220, 40, 40)
TEXT_COLOR = (230, 230, 230)
GameTitle = "Fall Simulator"
