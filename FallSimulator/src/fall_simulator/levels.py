import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class LevelSpec:
    id: int
    points_needed: int
    platforms: List[Dict[str, Any]]
    num_targets: int = 1

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
    for item in raw: 
        levels.append(LevelSpec(
            id=int(item.get("id", 0)), # ID del nivel
            points_needed=int(item.get("points_needed", 0)), # Puntos necesarios para completar el nivel
            platforms=item.get("platforms", []), # Plataformas del nivel
            num_targets=int(item.get("num_targets", 1)) # Número de objetivos
        ))
    return levels
