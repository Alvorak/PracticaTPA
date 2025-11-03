# tests/test_game.py
from fall_simulator.game import Game


def test_game_init():
    """Un test simple para verificar la inicialización del juego."""
    g = Game(None)
    assert g.lifes == 3
    assert g.puntos == 0
