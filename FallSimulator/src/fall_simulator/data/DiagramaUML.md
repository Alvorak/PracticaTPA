classDiagram
%% Diagrama UML

class Juego {
  - screen
  - clock
  - levels
  - current_level_index
  - lifes
  - puntos
  - running
  - starting_lifes
  - escape_pulsado_time
  - font
  + run()
  + auto_play(steps)
  + _show_next_level_popup(screen, viewport, viewport_x, viewport_y, next_level_number)
  + _show_victory_popup(screen, viewport, viewport_x, viewport_y)
  + _show_game_over_popup(screen, viewport, viewport_x, viewport_y)
}

class Menu {
  - screen
  - font
  - options
  - title_font
  - selected
  + run()
  + draw()
}

class Jugador {
  - base_w
  - base_h
  - crouch_h
  - rect
  - vx
  - vy
  - color
  - on_ground
  - facing
  - crouching
  - speed
  + handle_input_axis(keys)
  + apply_physics(dt, ax, platforms, ground_y)
  + jump()
  + short_jump_cut()
  + crouch(keys)
  + draw(surface)
  + check_horizontal_collisions(platforms)
  + check_vertical_collisions(platforms, ground_y, prev_bottom, dt)
}

class Objetivo {
  - w
  - h
  - color
  - rect
  + random_position()
  + respawn()
  + respawn_away(player_rect, min_y_from_ground, min_x_distance)
  + draw(surface)
}

class Proyectil {
  - rect
  - direction
  - speed
  - color
  - active
  + update(dt)
  + draw(surface)
}

class Plataforma {
  - rect
  - color
  + draw(surface)
}

class Nivel {
  + id
  + points_needed
  + platforms
  + num_targets
  + total_enemies
  + max_on_screen
  + create_platforms(viewport_w, ground_y, PlatformFactory)
}

%% Relaciones entre clases
Juego --> Menu : muestra
Juego --> Jugador : crea / contiene
Juego --> Nivel : carga / usa
Nivel o-- Plataforma : contiene
Juego --> Proyectil : crea (proyectiles jugador)
Jugador --> Proyectil : dispara / crea
Objetivo --> Proyectil : dispara / crea (proyectil enemigo)
Objetivo --> Jugador : apunta_a
Proyectil --> Jugador : puede_impactar
Proyectil --> Objetivo : puede_impactar
Juego --> savegame.py : guarda / carga estado