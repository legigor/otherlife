from gameoflife import GameOfLife


def test_survive_2():
    # * *
    # * <- must survive

    game = GameOfLife([(0, 0), (0, 1), (1, 1)])
    game.turn()
    state = game.get_state()
    assert (0, 0) in state


def test_survive_3():
    # * * *
    #   * <- must survive

    game = GameOfLife([(0, 0), (-1, 1), (0, 1), (1, 1)])
    game.turn()
    state = game.get_state()
    assert (0, 0) in state


def test_die_lonely():
    game = GameOfLife([(0, 0)])
    game.turn()
    state = game.get_state()
    assert (0, 0) not in state


def test_die_overcrowded():
    # * * *
    # * * *

    game = GameOfLife([(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0)])
    game.turn()
    state = game.get_state()
    assert (0, 0) not in state


def test_new_cell():
    # * * *

    game = GameOfLife([(-1, 1), (0, 1), (1, 1)])
    game.turn()
    state = game.get_state()
    assert (0, 0) in state
