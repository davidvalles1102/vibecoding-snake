"""Pruebas automáticas de la lógica del juego (no requieren abrir la ventana).

Se ejecutan con:  python test_snake.py
"""
from snake import (
    next_head,
    hits_wall,
    hits_self,
    is_reversal,
    speed_for_score,
    random_food_position,
    GRID_WIDTH,
    GRID_HEIGHT,
    INITIAL_SPEED_MS,
    MIN_SPEED_MS,
)


def test_next_head_moves_in_each_direction():
    assert next_head((5, 5), "Right") == (6, 5)
    assert next_head((5, 5), "Left") == (4, 5)
    assert next_head((5, 5), "Up") == (5, 4)
    assert next_head((5, 5), "Down") == (5, 6)


def test_hits_wall_detects_out_of_bounds():
    assert hits_wall((-1, 0)) is True
    assert hits_wall((GRID_WIDTH, 0)) is True
    assert hits_wall((0, -1)) is True
    assert hits_wall((0, GRID_HEIGHT)) is True
    assert hits_wall((0, 0)) is False
    assert hits_wall((GRID_WIDTH - 1, GRID_HEIGHT - 1)) is False


def test_hits_self_detects_body_collision():
    body = [(5, 5), (4, 5), (3, 5)]
    assert hits_self((4, 5), body) is True
    assert hits_self((9, 9), body) is False


def test_is_reversal_blocks_the_snake_from_going_into_its_own_neck():
    # Este es el bug que se detectó al jugar la v1: si la serpiente iba
    # a la derecha y se presionaba "Left" muy rápido, se movía directo
    # sobre su propio cuello y perdía sin razón aparente para quien jugaba.
    assert is_reversal("Right", "Left") is True
    assert is_reversal("Left", "Right") is True
    assert is_reversal("Up", "Down") is True
    assert is_reversal("Down", "Up") is True
    assert is_reversal("Right", "Up") is False
    assert is_reversal("Right", "Down") is False
    assert is_reversal("Right", "Right") is False


def test_speed_for_score_increases_but_has_a_floor():
    assert speed_for_score(0) == INITIAL_SPEED_MS
    assert speed_for_score(5) < speed_for_score(0)
    assert speed_for_score(1000) == MIN_SPEED_MS  # nunca queda imposible de jugar


def test_food_never_spawns_on_top_of_the_snake():
    body = [(x, 0) for x in range(GRID_WIDTH)] + [(x, 1) for x in range(GRID_WIDTH - 1)]
    for _ in range(50):
        food = random_food_position(body)
        assert food not in body


def run_all():
    tests = [obj for name, obj in globals().items() if name.startswith("test_")]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"OK  - {test.__name__}")
    print(f"\n{passed}/{len(tests)} pruebas pasaron correctamente.")


if __name__ == "__main__":
    run_all()
