class Grid:
    """
        Initialize the grid with the specified number of rows and columns.
        
        Parameters:
            rows (int): the number of rows for the grid (default is 3)
            cols (int): the number of columns for the grid (default is 3)
            no_visual (bool): flag to indicate if visual representation is disabled (default is False)
            no_border (bool): flag to indicate if border is disabled (default is False)
        
        Returns:
            None
    """
    def __init__(self, rows: int= 3, cols: int= 3, no_visual: bool= False, no_border: bool= False) -> None:
        self.rows = rows
        self.cols = cols
        self.no_visual = no_visual
        self.no_border = no_border

        grid = []

        for i in range(rows):
            grid.append([])

            [grid[i].append(' ') for _ in range(cols)]

        self.grid = grid

    def show_grid(self) -> str:
        """
            A function to display a grid based on the grid attribute values.
            Raises an AttributeError if 'no_visual' attribute is True.
            Returns a string representation of the grid display.
        """
        if self.no_visual:
            raise AttributeError("Invalid method 'show_grid' for grid with attribute 'no_visual'")
        
        grid_display = """\n"""

        if self.no_border == False:
            for i in range(self.cols):
                if i == (self.cols -1):  grid_display += '+---+\n'
                else:  grid_display += '+---'

        for row_index in range(self.rows):
            for col_index in range(self.cols):
                if col_index == (self.cols -1):
                    if self.no_border == False:  grid_display += f'| {self.grid[row_index][col_index]} |\n'
                    else:  grid_display += f'| {self.grid[row_index][col_index]}  \n'

                    for i in range(self.cols):
                        if row_index == (self.rows -1) and self.no_border == True:  continue

                        if i == (self.cols -1):  grid_display += '+---+\n'
                        else:  grid_display += '+---'
                else:
                    if col_index == 0:
                        print('so why are you doing this?😭😭😭')
                        if self.no_border == True:  grid_display += f'  {self.grid[row_index][col_index]} '
                        else:  grid_display += f'| {self.grid[row_index][col_index]} '
                    else:  grid_display += f'| {self.grid[row_index][col_index]} '

        print(grid_display)

        return grid_display

    def get_cell(self, row: int, col: int):
        """
            Retrieves a cell from the grid based on the specified row and column indices.
            
            Parameters:
                row (int): The index of the row.
                col (int): The index of the column.
            
            Returns:
                The value at the specified cell in the grid.
            
            Raises:
                TypeError: If the provided row or column indices are invalid.
        """
        try:  return self.grid[row -1][col -1]
        except:  raise TypeError("Invalid argument type")
    
    def update(self, row, col, value) -> list:
        """
            Updates a cell in the grid with the given value.

            Parameters:
                row (int): The row index of the cell.
                col (int): The column index of the cell.
                value : The value to be placed in the cell.

            Returns:
                list: The updated grid.

            NB:
                values with lengths more than 1 will affect the grid visualization
        """
        try:  self.grid[row -1][col -1] = value
        except:  raise TypeError("Invalid argument type")

        return self.grid

    def __str__(self) -> str:
        return f"Grid(x={self.x}, y={self.y}, no_border={self.no_border})"
    
    def __repr__(self) -> str:
        return self.__str__()