

import pygame
import sys
import time
import config
from config import *
from entities.modoentrenamiento import ModoEntrenamiento
from entities.global_events import check_esc_close

def draw_menu(screen, FONT):
	screen.fill(BLACK)
	title = FONT.render('MORSEMANIA', True, GREEN)
	screen.blit(title, (50, 40))
	subtitle = FONT.render('Selecciona el modo de juego:', True, GREEN)
	screen.blit(subtitle, (50, 120))
	option1 = FONT.render('1. Modo entrenamiento', True, GREEN)
	screen.blit(option1, (50, 180))
	option2 = FONT.render('2. Salir', True, GREEN)
	screen.blit(option2, (50, 240))
	info = FONT.render('Pulsa el número y Enter para elegir', True, GREEN)
	screen.blit(info, (50, 300))
	pygame.display.flip()

def modo_entrenamiento(screen, FONT):
	morse_input = ''
	detected_letter = ''
	last_input_time = None
	show_letter_time = SHOW_LETTER_TIME
	auto_translate_time = AUTO_TRANSLATE_TIME
	progress_rect = pygame.Rect(*PROGRESS_RECT)
	progress = 0
	progress_max = PROGRESS_MAX
	press_time = None
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					press_time = time.time()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE and press_time:
					duration = time.time() - press_time
					if duration < progress_max:
						morse_input += '.'
					else:
						morse_input += '-'
					press_time = None
					last_input_time = time.time()
					progress = 0
				elif event.key == pygame.K_RETURN:
					detected_letter = MORSE_DECODE.get(morse_input, '')
					morse_input = ''
					last_input_time = time.time()
		# Actualizar barra de progreso si se está pulsando
		if press_time:
			progress = time.time() - press_time
			if progress > progress_max:
				progress = progress_max
		else:
			progress = 0
		# Traducción automática tras 3 segundos de pausa
		if morse_input and last_input_time and not press_time:
			if time.time() - last_input_time > auto_translate_time:
				detected_letter = MORSE_DECODE.get(morse_input, '')
				morse_input = ''
				last_input_time = time.time()
		# Borrar letra y morse tras 8 segundos de inactividad
		if last_input_time and (detected_letter or morse_input):
			if time.time() - last_input_time > show_letter_time:
				detected_letter = ''
				morse_input = ''
				last_input_time = None
		# Dibujo
		screen.fill(BLACK)
		pygame.draw.rect(screen, (40, 80, 40), progress_rect, border_radius=8)
		if progress > 0:
			fill_width = int((progress / progress_max) * progress_rect.width)
			pygame.draw.rect(screen, GREEN, (progress_rect.x, progress_rect.y, fill_width, progress_rect.height), border_radius=8)
		morse_text = FONT.render(morse_input, True, GREEN)
		screen.blit(morse_text, (50, 100))
		if detected_letter:
			letter_text = FONT.render(detected_letter, True, GREEN)
			screen.blit(letter_text, (50, 180))
		pygame.display.flip()
		pygame.time.Clock().tick(60)

def main():
	pygame.init()
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	pygame.display.set_caption('Morsemania')
	FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
	menu_active = True
	selected = ''
	esc_pressed_time = None
	while menu_active:
		draw_menu(screen, FONT)
		esc_pressed_time = check_esc_close(screen, FONT, esc_pressed_time)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.unicode == '1':
					selected = '1'
				elif event.unicode == '2':
					selected = '2'
				elif event.key == pygame.K_RETURN:
					if selected == '1':
						ModoEntrenamiento(screen, FONT).run()
						selected = ''
					elif selected == '2':
						pygame.quit()
						sys.exit()
		pygame.time.Clock().tick(30)

if __name__ == '__main__':
	main()
