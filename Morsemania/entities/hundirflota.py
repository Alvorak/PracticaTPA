import pygame  # Librería para gráficos y eventos
import random  # Para posiciones aleatorias
import time    # Para control de tiempo
import sys     # Para salir del programa
from config import *

class HundirLaFlota:
    """
    Minijuego Hundir la Flota:
    - El usuario debe disparar a enemigos que cruzan la pantalla usando coordenadas en morse.
    - El objetivo es evitar que los enemigos lleguen al bunker aliado (rectángulo GREEN a la derecha).
    - El usuario tiene 20 vidas.
    """
    def __init__(self, screen, font):
        # Main variables
        self.screen = screen
        self.font = font
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.grid_size = 40
        self.rows = 10
        self.cols = 9
        self.grid_left = (self.WIDTH - self.cols * self.grid_size) // 2
        self.grid_top = max(30, (self.HEIGHT - self.rows * self.grid_size) // 2 - 40)
        self.bunker_width = self.grid_size * 2
        self.bunker_height = self.grid_size * 2
        self.bunker_x = self.grid_left + self.cols * self.grid_size + 60
        self.bunker_y = self.grid_top + (self.rows * self.grid_size - self.bunker_height) // 2
        self.player_rect = pygame.Rect(self.bunker_x, self.bunker_y + self.bunker_height//4, self.bunker_width, self.bunker_height//2)
        self.enemies = [self.create_enemy()]
        self.enemy_rects = self.enemies
        self.projectiles = []
        self.last_shot = 0
        self.shot_cooldown = 1.0
        self.letters = [chr(ord('A')+i) for i in range(10)]
        self.numbers = [str(i+1) for i in range(9)]
        self.morse_input = ''
        self.last_input_time = None
        self.guide_table = self.build_guide_table()
        self.running = True
        self.progress_rect = pygame.Rect(*PROGRESS_RECT)
        self.progress = 0
        self.progress_max = PROGRESS_MAX
        self.press_time = None
        self.detected_letter = ''
        self.detected_number = ''
        self.input_stage = 0
        self.lives = 20

    def build_guide_table(self):
        """Builds the reference table of letters and numbers in morse to display as a legend."""
        table = []
        for l in self.letters:
            table.append(f"{l}: {MORSE_CODE.get(l, '')}")
        for n in self.numbers:
            table.append(f"{n}: {MORSE_CODE.get(n, '')}")
        return table

    def create_enemy(self):
        """Creates a new enemy (red rectangle) at a random position to the left of the grid."""
        y = self.grid_top + self.grid_size * random.randint(0, self.rows-1)
        return pygame.Rect(self.grid_left - 400, y, self.grid_size, self.grid_size)

    def draw_grid(self):
        """Draws the game grid, letters, numbers, and the allied bunker."""
        for i in range(self.rows+1):
            pygame.draw.line(self.screen, GREEN, (self.grid_left, self.grid_top + i*self.grid_size), (self.grid_left + self.cols*self.grid_size, self.grid_top + i*self.grid_size), 2)
        for j in range(self.cols+1):
            pygame.draw.line(self.screen, GREEN, (self.grid_left + j*self.grid_size, self.grid_top), (self.grid_left + j*self.grid_size, self.grid_top + self.rows*self.grid_size), 2)
        # Letter labels
        for i, l in enumerate(self.letters):
            label = self.font.render(l, True, GREEN)
            self.screen.blit(label, (self.grid_left - 30, self.grid_top + i*self.grid_size + 5))
        for j, n in enumerate(self.numbers):
            label = self.font.render(n, True, GREEN)
            self.screen.blit(label, (self.grid_left + j*self.grid_size + 10, self.grid_top - 30))
        # Draw the bunker
        pygame.draw.rect(self.screen, (0, 180, 0), (self.bunker_x, self.bunker_y, self.bunker_width, self.bunker_height), border_radius=10)

    def draw_player(self):
        """Dibuja el rectángulo GREEN del bunker aliado."""
        pygame.draw.rect(self.screen, (0,255,0), self.player_rect, border_radius=8)

    def draw_enemies(self):
        """Dibuja todos los enemigos (rectángulos rojos) en pantalla."""
        for rect in self.enemy_rects:
            pygame.draw.rect(self.screen, (200, 0, 0), rect)

    def draw_projectiles(self):
        """Draws the blue projectiles shot by the player."""
        for proj in self.projectiles:
            pygame.draw.rect(self.screen, (0, 100, 255), proj['rect'])

    def draw_guide(self):
        """Dibuja la leyenda de referencia de letras y números en morse debajo de la cuadrícula."""
        # Leyenda debajo de la cuadrícula, bien alineada
        x = self.grid_left
        y = self.grid_top + self.grid_size * self.rows + 40
        col_width = 200  # Más separación entre columnas
        rows_per_col = 9
        for i, row in enumerate(self.guide_table):
            col = i // rows_per_col
            row_in_col = i % rows_per_col
            label = self.font.render(row, True, GREEN)
            self.screen.blit(label, (x + col * col_width, y + row_in_col * 38))

    def draw_input_status(self):
        """Always show the current Morse input, last detected letter, and last detected number under the progress bar."""
        x = self.progress_rect.x
        y = self.progress_rect.y + self.progress_rect.height + 20
        morse_text = self.font.render(f"Morse: {self.morse_input}", True, (0,200,255))
        self.screen.blit(morse_text, (x, y))
        letra_text = self.font.render(f"Letter: {self.detected_letter}", True, (255,255,0))
        self.screen.blit(letra_text, (x + 350, y))
        numero_text = self.font.render(f"Number: {self.detected_number}", True, (255,255,0))
        self.screen.blit(numero_text, (x + 600, y))

    def draw_progress_bar(self):
        """Dibuja la barra de progreso para distinguir punto/raya en el input morse."""
        pygame.draw.rect(self.screen, (40, 80, 40), self.progress_rect, border_radius=8)
        if self.progress > 0:
            fill_width = int((self.progress / self.progress_max) * self.progress_rect.width)
            pygame.draw.rect(self.screen, GREEN, (self.progress_rect.x, self.progress_rect.y, fill_width, self.progress_rect.height), border_radius=8)

    def handle_input(self, event):
        """Gestiona la entrada de teclado para el input morse y la detección de letras/números."""
        if event.type == pygame.KEYDOWN:
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
                if self.input_stage == 0:
                    self.detected_letter = MORSE_CODE.get(self.morse_input, '')
                    if self.detected_letter in self.letters:
                        self.input_stage = 1
                        self.morse_input = ''
                    else:
                        self.morse_input = ''
                elif self.input_stage == 1:
                    self.detected_number = MORSE_CODE.get(self.morse_input, '')
                    if self.detected_number in self.numbers:
                        self.shoot(self.detected_letter, self.detected_number)
                    self.input_stage = 0
                    self.morse_input = ''

    def shoot(self, letter, number):
        """Create a larger blue projectile in the cell indicated by letter and number if valid."""
        row = self.letters.index(letter)
        if number in self.numbers:
            col = self.numbers.index(number)
        else:
            return
        x = self.grid_left + col * self.grid_size
        y = self.grid_top + row * self.grid_size
        # Make projectile larger for visibility
        proj_size = int(self.grid_size * 1.2)
        offset = (proj_size - self.grid_size) // 2
        rect = pygame.Rect(x - offset, y - offset, proj_size, proj_size)
        self.projectiles.append({'rect': rect, 'time': time.time()})

    def update_enemies(self):
        """Mueve los enemigos hacia la derecha y gestiona la pérdida de vidas si llegan al bunker."""
        for rect in self.enemy_rects:
            rect.x += 1  # mucho más lento
        for rect in self.enemy_rects:
            # Si llega al bunker, perder vida
            if rect.x + rect.width >= self.bunker_x:
                self.lives -= 1
                rect.x = self.grid_left - 400
                rect.y = self.grid_top + self.grid_size * random.randint(0, self.rows-1)
            elif rect.x > self.grid_left + self.cols*self.grid_size + 200:
                rect.x = self.grid_left - 400
                rect.y = self.grid_top + self.grid_size * random.randint(0, self.rows-1)

    def check_collisions(self):
        """Detecta colisiones entre proyectiles y enemigos, y reinicia enemigos destruidos."""
        for proj in self.projectiles:
            for rect in self.enemy_rects:
                if proj['rect'].colliderect(rect):
                    rect.x = 0
                    rect.y = self.grid_top + self.grid_size * random.randint(0, self.rows-1)
                    self.projectiles.remove(proj)
                    break

    def update_projectiles(self):
        """Removes projectiles that have been on screen for more than 2.5 seconds (longer for visibility)."""
        now = time.time()
        self.projectiles = [p for p in self.projectiles if now - p['time'] < 2.5]

    def draw_lives(self):
        """Dibuja el contador de vidas en pantalla."""
        text = self.font.render(f"Vidas: {self.lives}", True, (255,255,255))
        self.screen.blit(text, (self.bunker_x, self.bunker_y - 60))

    def run(self):
        """Main game loop: handles events, updates and draws all elements."""
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                self.handle_input(event)
            if self.press_time:
                self.progress = time.time() - self.press_time
                if self.progress > self.progress_max:
                    self.progress = self.progress_max
            else:
                self.progress = 0
            if self.morse_input and self.last_input_time and not self.press_time:
                if time.time() - self.last_input_time > AUTO_TRANSLATE_TIME:
                    if self.input_stage == 0:
                        self.detected_letter = MORSE_CODE.get(self.morse_input, '')
                        if self.detected_letter in self.letters:
                            self.input_stage = 1
                            self.morse_input = ''
                        else:
                            self.morse_input = ''
                    elif self.input_stage == 1:
                        self.detected_number = MORSE_CODE.get(self.morse_input, '')
                        if self.detected_number in self.numbers:
                            self.shoot(self.detected_letter, self.detected_number)
                        self.input_stage = 0
                        self.morse_input = ''
            self.update_enemies()
            self.update_projectiles()
            self.check_collisions()
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_player()
            self.draw_enemies()
            self.draw_projectiles()
            self.draw_guide()
            self.draw_progress_bar()
            self.draw_input_status()
            self.draw_lives()
            if self.lives <= 0:
                game_over = self.font.render("GAME OVER", True, (255,0,0))
                self.screen.blit(game_over, (self.WIDTH//2 - 200, self.HEIGHT//2 - 50))
                pygame.display.flip()
                pygame.time.wait(2500)
                self.running = False
            else:
                pygame.display.flip()
            clock.tick(60)
