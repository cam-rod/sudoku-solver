# Cameron Rodriguez
# Date
# This program will dynamically solve a sudoku grid.

"""
Data Dictionary

grid: LIST: stores sudoku grid in 3D array; in third dimension, the first element is the number and the second indicates permanent
predictions: LIST: a 3D array parallel to grid; the third dimension is a list of potential values for each spot in grid
temp_predictions: LIST: temporarily stores a list of all values not found in a row/column/3x3 inner grid
result:  LIST: stores returned value of fill_grid() with confirmation of puzzle solution and the updated grid if so
y: INT: indicates the row the program is checking from the top
x: INT: indicates the column the program is checking from the left
grid_location: STR: contains the user inputted location of the game data

inner_values: LIST: a list of values found in the same 3x3 grid as grid[y][x]
inner_y: INT: indicates the row of grid[y][x] relative to its 3x3 grid
inner_x: INT: indicates the column of grid[y][x] relative to its 3x3 grid
"""

# Loads empty 3D arrays with 9 lists within 9 lists
grid = [[[] for i in range(9)] for j in range(9)]
predictions=[[[] for i in range(9)] for j in range(9)]

temp_predictions = []
result = []
y = 0
x = 0
grid_location = ''

def inner_grid(y, x, grid):
    inner_values = []
    inner_y = 0
    inner_x = 0
    
    inner_y = y % 3
    inner_x = x % 3
    
    # Retrieve the values of the 8 other spaces in a 3x3 grid based on inner_y and inner_x position
    if inner_y == 0 and inner_x == 0: # Top left position
        inner_values = [grid[y+1][x][0], grid[y+2][x][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y+2][x+1][0], grid[y][x+2][0], grid[y+1][x+2][0], grid[y+2][x+2][0]]
    elif inner_y == 0 and inner_x == 1: # Top centre position
        inner_values = [grid[y][x-1], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0], grid[y][x+1][0], grid[y+1][x+2][0], grid[y+2][x+2][0]]
    elif inner_y == 0 and inner_x == 2: # Top right position
        inner_values = [grid[y][x-2][0], grid[y+1][x-2][0], grid[y+2][x-2][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0]]
    elif inner_y == 1 and inner_x == 0: # Centre left position
        inner_values = [grid[y-1][x], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y-1][x+2][0], grid[y][x+2][0], grid[y+1][x+2][0]]
    elif inner_y == 1 and inner_x == 1: # Centre centre position
        inner_values = [grid[y-1][x-1], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0]]
    elif inner_y == 1 and inner_x == 2: # Centre right position
        inner_values = [grid[y-1][x-2], grid[y][x-2][0], grid[y+1][x-2][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0]]
    elif inner_y == 2 and inner_x == 0: # Bottom left position
        inner_values = [grid[y-2][x], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y-2][x+2][0], grid[y-1][x+2][0], grid[y][x+2][0]]
    elif inner_y == 2 and inner_x == 1: # Bottom centre position
        inner_values = [grid[y-2][x-1], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0]]
    elif inner_y == 2 and inner_x == 2: # Bottom right position
        inner_values = [grid[y-2][x-2], grid[y-1][x-2][0], grid[y][x-2][0], grid[y-2][x-1][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0]]
    # End if inner_y
    
    return inner_values
