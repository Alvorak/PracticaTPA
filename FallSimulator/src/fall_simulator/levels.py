import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any
from . import config


@dataclass
class LevelSpec:
    id: int
    points_needed: int
    platforms: List[Dict[str, Any]]
    num_targets: int = 1
    total_enemies: int = None
    max_on_screen: int = None
    max_on_screen: int = None

    def create_platforms(self, viewport_w: int, ground_y: int, PlatformFactory=None): # plataforma factory opcional (plataforma personalizada)
        """Crea objetos de plataforma usando la especificación.

        PlatformFactory: callable(x, y, w, h) -> plataforma. Si no se pasa, se devuelve dicts (en lugar de objetos).
        """
        plats = []
        for p in self.platforms: # Itera sobre cada especificación de plataforma
            w = int(p.get("w", 200))
            h = int(p.get("h", 20))
            # x_frac: posición centrada en frac (0..1). Si no existe, usa x_px o 0 
            if "x_frac" in p:
                x = int(p["x_frac"] * viewport_w) - w // 2 # Centrado en x_frac usando viewport_w para el ancho 
            else:
                x = int(p.get("x", 0))
            # y_from_ground: distancia desde el suelo hacia arriba
            if "y_from_ground" in p:
                y = int(ground_y - int(p["y_from_ground"]))
            else:
                y = int(p.get("y", ground_y - 150))

            if PlatformFactory:
                plats.append(PlatformFactory(x, y, w, h))
            else:
                plats.append({"x": x, "y": y, "w": w, "h": h})
        return plats


def load_levels(path: str = None) -> List[LevelSpec]:
    """Carga especificaciones de niveles desde un JSON. Si path es None, busca 'data/levels.json' junto a este módulo."""
    if path is None:
        path = Path(__file__).parent / "data" / "levels.json"  # Ruta por defecto de niveles
    else:
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Archivo de niveles no encontrado: {path}")  # Ruta no encontrada

    raw = json.loads(path.read_text(encoding="utf-8")) # Carga JSON en utf-8
    levels = []
    # Base de puntos por nivel (exponencial). Si no está en config, usar 3
    base = getattr(config, "LEVEL_BASE_POINTS", 3)
    # Maximo por defecto de enemigos simultaneos (si no se especifica por nivel)
    default_max_on_screen = getattr(config, "MAX_ENEMIES_ON_SCREEN", None)
    for idx, item in enumerate(raw):
        num_targets = int(item.get("num_targets", 1))
        # calcular puntos de forma exponencial: base * 2^(idx)
        points_needed = int(base * (2 ** idx))
        # soporte opcional para max_on_screen por nivel
        max_on_screen = item.get("max_on_screen", default_max_on_screen)
        if max_on_screen is not None:
            max_on_screen = int(max_on_screen)
            num_targets = min(num_targets, max_on_screen)

        # No crear más enemigos que puntos necesarios para superar el nivel
        if points_needed is not None:
            num_targets = min(num_targets, int(points_needed))
        # total_enemies: máximo total que puede aparecer en el nivel (si no se indica, igual a points_needed)
        total_enemies = int(item.get("total_enemies", points_needed))

        levels.append(LevelSpec(
            id=int(item.get("id", idx + 1)),
            points_needed=points_needed,
            platforms=item.get("platforms", []),
            num_targets=num_targets,
            total_enemies=total_enemies,
            max_on_screen=max_on_screen
        ))
    return levels
