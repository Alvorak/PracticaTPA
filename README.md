<img width="867" height="425" alt="{181AD750-2DAA-4AFB-81F9-8D0C1334D164}" src="https://github.com/user-attachments/assets/98740e9d-2851-44ce-93db-40cd2fc0c173" /># PracticaTPA – FallSimulator

Repositorio para el proyecto de la asignatura de Técnicas de Programación Avanzada (TPA).

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **juego de plataformas y acción en un entorno vertical**, creado con **Python** y **Pygame**.  

El jugador controla un personaje que puede **saltar**, **agacharse** y **disparar**, habilidades esenciales para avanzar entre plataformas y superar distintos obstáculos y enemigos.  

El objetivo principal es **progresar lo máximo posible**, combinando precisión, tiempo de reacción y estrategia.

---

## Tecnologías Utilizadas

- **Python 3.11** – Lenguaje de programación principal.  
- **Pygame 2.x** – Biblioteca para gráficos, sonidos y eventos.  
- **pytest** – Framework para pruebas unitarias.  
- **python-dotenv** – Manejo de variables de entorno desde archivos .env.

## Herramientas de desarrollo
- **black** – Formateador automático de código.
- **ruff** – Analizador estático y linter para mantener la calidad del código.
- **pdoc** – Generador de documentación automática a partir de docstrings.
- **GitHub Copilot** (opcional) – Asistente de programación basado en IA.

---

## Estructura del Proyecto

```text
FallSimulator/
│
├─ pyproyect.toml
├─ src/
│  └─ requirements.txt
│  └─ fall_simulator/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ game.py
│     ├─ menu.py
│     ├─ config.py
│     ├─ constants.py
│     ├─ levels.py
│     ├─ savegame.py
│     ├─ Entities/
│     │  ├─ player.py
│     │  ├─ projectile.py
│     │  ├─ target.py
│     │  └─ platform.py
│     └─ tests/
│        └─ test_game.py
│     └─ data/
│        └─ DiagramaUML.md
│        └─ levels.json
├─ gendocs.bat
├─ gendocs.sh
├─ .pre-commit-config.yaml
├─ README.md
└─ .gitignore
```
## Instalación y Configuración
### 1. Clonar el repositorio
```
git clone https://github.com/tu_usuario/PracticaTPA.git
cd PracticaTPA/FallSimulator/src
```

### 2. Crear y activar entorno virtual
- Crear entorno virtual
```cmd
python -m venv .venv
```

### 3. Activar entorno virtual en Windows PowerShell
```cmd
.venv\Scripts\Activate.ps1
```
**si da error de ejecución adjuntar en la terminal** 
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
es cuestion de permisos D: (sad, i know!)

 **En Linux / Mac**
```cmd
source .venv/bin/activate
```
### 4. Instalar dependencias
```cmd
pip install -r requirements.txt
```
## Ejecución del Juego
### Modo normal
```cmd
python -m fall_simulator
```
### Modo demo 
"se explica mas adelante"
```cmd
python -m fall_simulator --demo
```

## Controles:
- A/D – Moverse
- Space/W – Saltar
- S – Agacharse
- Flechas – Disparar (puede combinarse diagonalmente)

## Modo demo / auto_play
```python
from fall_simulator.game import Game
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
game = Game(screen)
game.auto_play()  # Juega automáticamente un nivel corto
```

El modo demo simula movimientos aleatorios de izquierda a derecha, saltos, agacharse y disparos para revisión rápida.


## Testing con Pytest

### 1.Activar entorno virtual si no lo está
```cmd
.venv\Scripts\Activate.ps1
```

### 2.Ejecutar tests
```cmd
pytest
```

Los tests comprueban la inicialización del juego sin necesidad de abrir la ventana de Pygame.
Para modo más detallado:
```cmd
pytest -v
```

## Notas Importantes

Mantener .venv **fuera del control de versiones** (ya está en .gitignore).

Los tests y el modo demo están diseñados para evitar errores por falta de pantalla **(screen=None)**.
