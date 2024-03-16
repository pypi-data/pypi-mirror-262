# cli-grid

cli-grid is a simple Python package for creating, managing, and visualizing grids.

This library allows you to create a grid with any number of rows and columns. Each cell in the grid can then be accessed and updated. By default, a visual representation of the grid can be displayed, but this can be disabled.

## Usage

To start, simply initialize the library like so:

```python
from py_grid import Grid

grid = Grid()
```

This creates a 3*3 grid by default.
### Parameters:
    > row(int) => The number of rows
    > columns(int) => The number of columns
    > no_visual(bool) => Boolean flag to indicate if visualization of the grid is disabled (set to False by default)
    > no_border(bool) => Boolean flag to indicate if borders are disabled when visualizing the grid (set to False by default). Note that this will have no effect if `no-viual` is set to True


To get a particular cell:

```Python
grid.get_cell(3, 2)
```

This returns the value of the cell on row 3, column 2 of the grid


To update a particular cell:

```Python
grid.update(3, 2, 'X')
```

This updates the value of the cell on row 3, column 2 of the grid to the string 'X'


To display the grid:

```Python
grid.show_grid()
```

This prints outs a visual reprsentation of the grid and returns the string value of this reepresentation