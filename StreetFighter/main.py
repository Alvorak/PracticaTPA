# main.py
import pygame
import sys

# -----------------------
# Configuración
# -----------------------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
FPS = 60

GROUND_HEIGHT = 80  # altura del "suelo" desde abajo

# Física
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

# -----------------------
# Clase jugador
# -----------------------
class Player:
    def __init__(self, x, y, w=50, h=90, color=PLAYER_COLOR):
        self.base_w = w
        self.base_h = h
        self.crouch_h = h // 2  # altura agachado

        self.rect = pygame.Rect(int(x), int(y), w, h)
        self.vx = 0.0
        self.vy = 0.0
        self.color = color
        self.on_ground = False
        self.facing = 1
        self.crouching = False

    def handle_input_axis(self, keys):
        ax = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax -= MOVE_ACCEL
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax += MOVE_ACCEL
            self.facing = 1
        return ax

    def jump(self):
        if self.on_ground:
            self.vy = -JUMP_VELOCITY
            self.on_ground = False

    def short_jump_cut(self):
        if self.vy < 0:
            self.vy *= 0.45

    def crouch(self, keys):
        """Maneja el estado de agachado"""
        want_crouch = keys[pygame.K_DOWN] or keys[pygame.K_s]

        if want_crouch and not self.crouching:
            # pasar a agachado
            self.crouching = True
            self.rect.height = self.crouch_h
            self.rect.y += self.base_h - self.crouch_h  # ajustar posición

        elif not want_crouch and self.crouching:
            # volver a tamaño normal
            self.crouching = False
            old_bottom = self.rect.bottom
            self.rect.height = self.base_h
            self.rect.bottom = old_bottom  # mantener pies en el mismo sitio

    def apply_physics(self, dt, ax):
        self.vx += ax * dt

        if ax == 0:
            if self.vx > 0:
                self.vx -= FRICTION * dt
                if self.vx < 0:
                    self.vx = 0.0
            elif self.vx < 0:
                self.vx += FRICTION * dt
                if self.vx > 0:
                    self.vx = 0.0

        if self.vx > MAX_SPEED:
            self.vx = MAX_SPEED
        if self.vx < -MAX_SPEED:
            self.vx = -MAX_SPEED

        # Gravedad
        self.vy += GRAVITY * dt

        # Movimiento
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)

        # Límites
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx = 0

        # Suelo
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vy = 0.0
            self.on_ground = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Indicador de dirección
        head_w = 10
        cx = self.rect.centerx + (self.facing * (self.rect.width // 2 + 1))
        cy_top = self.rect.top + 18
        points = [(cx, cy_top), (cx + (-self.facing)*head_w, cy_top+7), (cx + (-self.facing)*head_w, cy_top-7)]
        pygame.draw.polygon(surface, (200,200,200), points)


# -----------------------
# Función principal
# -----------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Street Fighter - Base con agacharse")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial Unicode MS", 20)

    player = Player(SCREEN_WIDTH // 3, SCREEN_HEIGHT - GROUND_HEIGHT - 90)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player.short_jump_cut()

        keys = pygame.key.get_pressed()
        ax = player.handle_input_axis(keys)
        player.crouch(keys)  # manejar agacharse
        player.apply_physics(dt, ax)

        screen.fill(BG_COLOR)
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(screen, GROUND_COLOR, ground_rect)
        player.draw(screen)

        lines = [
            "Controles: ←/→ o A/D = mover | Space/W/↑ = saltar | ↓ o S = agacharse",
            f"Vel: {player.vx:.0f} px/s | En suelo: {'Sí' if player.on_ground else 'No'} | Agachado: {'Sí' if player.crouching else 'No'}"
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, TEXT_COLOR)
            screen.blit(txt, (10, 10 + i*18))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
