import os
import json


def _save_path():
    # Guardar dentro de la carpeta 'data' del paquete: data/savegame.json
    here = os.path.dirname(__file__)
    data_dir = os.path.join(here, "data")
    # Asegurarse de que existe la carpeta data (por si no se creó aún)
    try:
        os.makedirs(data_dir, exist_ok=True)
    except Exception:
        pass
    return os.path.join(data_dir, "savegame.json")


def save_game(state: dict):
    """Guarda el diccionario state en disco como JSON.

    state puede contener claves: level_index (int), puntos (int), lifes (int)
    """
    try:
        with open(_save_path(), "w", encoding="utf-8") as f:
            json.dump(state, f)
    except Exception:
        # no queremos romper el juego por problemas de IO
        pass


def load_game():
    """Carga el estado guardado y lo devuelve como dict, o None si no existe/da error."""
    try:
        p = _save_path()
        if not os.path.exists(p):
            return None
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def clear_save():
    """Elimina el fichero de guardado si existe."""
    try:
        p = _save_path()
        if os.path.exists(p):
            os.remove(p)
    except Exception:
        pass
