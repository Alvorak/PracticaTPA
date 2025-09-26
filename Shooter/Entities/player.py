import pygame
import config

class Player:
    def __init__(self, x, y, w=50, h=90, color=config.PLAYER_COLOR):
        self.base_w = w
        self.base_h = h
        self.crouch_h = h // 2
        self.rect = pygame.Rect(int(x), int(y), w, h)
        self.vx = 0.0
        self.vy = 0.0
        self.color = color
        self.on_ground = False
        self.facing = 1
        self.crouching = False

    def handle_input_axis(self, keys):
        ax = 0.0
        if keys[pygame.K_a]:
            ax -= config.MOVE_ACCEL
            self.facing = -1
        if keys[pygame.K_d]:
            ax += config.MOVE_ACCEL
            self.facing = 1
        return ax

    def jump(self):
        if self.on_ground:
            self.vy = -config.JUMP_VELOCITY
            self.on_ground = False

    def short_jump_cut(self):
        if self.vy < 0:
            self.vy *= 0.45

    def crouch(self, keys):
        want_crouch = keys[pygame.K_s]
        if want_crouch and not self.crouching:
            self.crouching = True
            self.rect.height = self.crouch_h
            self.rect.y += self.base_h - self.crouch_h
        elif not want_crouch and self.crouching:
            self.crouching = False
            old_bottom = self.rect.bottom
            self.rect.height = self.base_h
            self.rect.bottom = old_bottom

    def apply_physics(self, dt, ax):
        self.vx += ax * dt
        if ax == 0:
            if self.vx > 0:
                self.vx -= config.FRICTION * dt
                if self.vx < 0:
                    self.vx = 0.0
            elif self.vx < 0:
                self.vx += config.FRICTION * dt
                if self.vx > 0:
                    self.vx = 0.0
        if self.vx > config.MAX_SPEED:
            self.vx = config.MAX_SPEED
        if self.vx < -config.MAX_SPEED:
            self.vx = -config.MAX_SPEED
        self.vy += config.GRAVITY * dt
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH
            self.vx = 0
        ground_y = config.SCREEN_HEIGHT - config.GROUND_HEIGHT
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vy = 0.0
            self.on_ground = True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        head_w = 10
        cx = self.rect.centerx + (self.facing * (self.rect.width // 2 + 1))
        cy_top = self.rect.top + 18
        points = [(cx, cy_top), (cx + (-self.facing)*head_w, cy_top+7), (cx + (-self.facing)*head_w, cy_top-7)]
        pygame.draw.polygon(surface, (200,200,200), points)
