# Configuraciones del juego

# Utilidad para obtener un rectángulo dentro del viewport jugable
import random
import pygame
from .constants import * # Importando todas las constantes desde constants.py

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

def is_pressed(keys, key):
	"""La función is_pressed verifica si una tecla específica está presionada."""
	try:
		return keys[key]
	except (TypeError, IndexError, KeyError, AttributeError):
			# Si es diccionario, probamos con key directamente, o con la representación en str
			return keys.get(key, keys.get('S', False) if key == pygame.K_s else False)



