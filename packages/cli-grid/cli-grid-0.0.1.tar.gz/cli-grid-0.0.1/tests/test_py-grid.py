import pytest
from ..src.cli_grid import Grid

@pytest.fixture
def grid():
    return Grid()

def test_grid_creation(grid):
    assert grid.rows == 3
    assert grid.cols == 3
    assert not grid.no_visual
    assert not grid.no_border

def test_get_cell(grid):
    assert grid.get_cell(1, 1) == ' '
    assert grid.get_cell(2, 2) == ' '

def test_update(grid):
    grid.update(1, 1, 'X')
    grid.update(2, 2, 'O')

    assert grid.get_cell(1, 1) == 'X'
    assert grid.get_cell(2, 2) == 'O'

def test_show_grid(grid, capsys):
    grid.show_grid()
    captured = capsys.readouterr()
    assert captured.out == "+---+---+---+\n|   |   |   |\n+---+---+---+\n|   |   |   |\n+---+---+---+\n|   |   |   |\n+---+---+---+\n"
