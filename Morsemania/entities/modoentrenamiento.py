import pygame
import time
import sys
from config import *
from entities.global_events import check_esc_close

class ModoEntrenamiento:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.morse_input = ''
        self.detected_letter = ''
        self.last_input_time = None
        self.show_letter_time = SHOW_LETTER_TIME
        self.auto_translate_time = AUTO_TRANSLATE_TIME
        self.progress_rect = pygame.Rect(*PROGRESS_RECT)
        self.progress = 0
        self.progress_max = PROGRESS_MAX
        self.press_time = None
        self.running = True

    def run(self):
        esc_pressed_time = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.press_time = time.time()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and self.press_time:
                        duration = time.time() - self.press_time
                        if duration < self.progress_max:
                            self.morse_input += '.'
                        else:
                            self.morse_input += '-'
                        self.press_time = None
                        self.last_input_time = time.time()
                        self.progress = 0
                    elif event.key == pygame.K_RETURN:
                        self.detected_letter = MORSE_DECODE.get(self.morse_input, '')
                        self.morse_input = ''
                        self.last_input_time = time.time()
            # Actualizar barra de progreso si se está pulsando
            if self.press_time:
                self.progress = time.time() - self.press_time
                if self.progress > self.progress_max:
                    self.progress = self.progress_max
            else:
                self.progress = 0
            # Traducción automática tras 3 segundos de pausa
            if self.morse_input and self.last_input_time and not self.press_time:
                if time.time() - self.last_input_time > self.auto_translate_time:
                    self.detected_letter = MORSE_DECODE.get(self.morse_input, '')
                    self.morse_input = ''
                    self.last_input_time = time.time()
            # Borrar letra y morse tras 8 segundos de inactividad
            if self.last_input_time and (self.detected_letter or self.morse_input):
                if time.time() - self.last_input_time > self.show_letter_time:
                    self.detected_letter = ''
                    self.morse_input = ''
                    self.last_input_time = None
            # Dibujo
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, (40, 80, 40), self.progress_rect, border_radius=8)
            if self.progress > 0:
                fill_width = int((self.progress / self.progress_max) * self.progress_rect.width)
                pygame.draw.rect(self.screen, GREEN, (self.progress_rect.x, self.progress_rect.y, fill_width, self.progress_rect.height), border_radius=8)
            morse_text = self.font.render(self.morse_input, True, GREEN)
            self.screen.blit(morse_text, (50, 100))
            if self.detected_letter:
                letter_text = self.font.render(self.detected_letter, True, GREEN)
                self.screen.blit(letter_text, (50, 180))
            # Evento global de cerrado por ESC
            esc_pressed_time = check_esc_close(self.screen, self.font, esc_pressed_time)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
