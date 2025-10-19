# PracticaTPA – FallSimulator

Repositorio para el proyecto de la asignatura de Técnicas de Programación Avanzada (TPA).

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **juego de plataformas y acción en un entorno vertical**, creado con **Python** y **Pygame**.  

El jugador controla un personaje que puede **saltar**, **agacharse** y **disparar**, habilidades esenciales para avanzar entre plataformas y superar distintos obstáculos y enemigos.  

El objetivo principal es **progresar lo máximo posible**, combinando precisión, tiempo de reacción y estrategia.

---

## Tecnologías Utilizadas

- **Python 3.11** – Lenguaje de programación principal.  
- **Pygame 2.x** – Biblioteca para gráficos, sonidos y eventos.  
- **pytest** – Para pruebas unitarias.  
- **GitHub Copilot** – Asistente de programación (opcional).  

---

## Estructura del Proyecto

```text
FallSimulator/
│
├─ src/
│  └─ fall_simulator/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ game.py
│     ├─ menu.py
│     ├─ config.py
│     ├─ constants.py
│     ├─ Entities/
│     │  ├─ player.py
│     │  ├─ projectile.py
│     │  ├─ target.py
│     │  └─ platform.py
│     └─ tests/
│        └─ test_game.py
├─ requirements.txt
└─ .gitignore
```
## Instalación y Configuración
1. Clonar el repositorio
```
git clone https://github.com/tu_usuario/PracticaTPA.git
cd PracticaTPA/FallSimulator/src
```

2. Crear y activar entorno virtual
# Crear entorno virtual
```
python -m venv .venv
```

# Activar entorno virtual en Windows PowerShell
```
.venv\Scripts\Activate.ps1
```
# (si da error de ejecución: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass) es cuestion de permisos D: (sad, i know!)

# En Linux / Mac
# source .venv/bin/activate

3. Instalar dependencias

pip install -r requirements.txt

## Ejecución del Juego
# Modo normal
```
python -m fall_simulator
```

# Controles:

- A/D – Moverse
- Space/W – Saltar
- S – Agacharse
- Flechas – Disparar (puede combinarse diagonalmente)

# Modo demo / auto_play (PROTOTIPO AUN)
```
from fall_simulator.game import Game
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
game = Game(screen)
game.auto_play()  # Juega automáticamente un nivel corto
```

El modo demo simula movimientos aleatorios de izquierda a derecha, saltos, agacharse y disparos para revisión rápida.


# Testing con Pytest

# Activar entorno virtual si no lo está
```
.venv\Scripts\Activate.ps1
```

# Ejecutar tests
```
pytest
```

Los tests comprueban la inicialización del juego sin necesidad de abrir la ventana de Pygame.
Para modo más detallado:
```
pytest -v
```

## Notas Importantes

Mantener .venv **fuera del control de versiones** (ya está en .gitignore).

Los tests y el modo demo están diseñados para evitar errores por falta de pantalla **(screen=None)**.