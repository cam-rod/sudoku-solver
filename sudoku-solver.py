# Cameron Rodriguez
# Date
# This program will dynamically solve a sudoku grid.

"""
Data Dictionary

grid: LIST: stores sudoku grid in 3D array; in third dimension, the first element is the number and the second indicates permanent
predictions: LIST: a 3D array parallel to grid; the third dimension is a list of potential values for each spot in grid
result:  LIST: stores returned value of fill_grid() with confirmation of puzzle solution and the updated grid if so
y: INT: indicates the row the program is checking from the top
x: INT: indicates the column the program is checking from the left
grid_location: STR: contains the user inputted location of the game data

values: LIST: a list of values found in the same 3x3 grid, row, or column as grid[y][x]
inner_y: INT: indicates the row of grid[y][x] relative to its 3x3 grid
inner_x: INT: indicates the column of grid[y][x] relative to its 3x3 grid
grid_raw: FILE: the opened file of the source puzzle
grid_text: LIST: list of sudoku puzzle rows
temp_predictions: LIST: temporarily stores a list of all values not found in a row/column/3x3 inner grid
"""

import re # Used to verify the puzzle as valid

# Loads empty 3D arrays with 9 lists within 9 lists
grid = [[[] for i in range(9)] for j in range(9)]
predictions=[[[] for i in range(9)] for j in range(9)]

result = []
values = []
y = 0
x = 0
grid_location = ''

# This function returns the value of the 8 other spaces in the same 3x3 inner grid as the indicated character
# region: STR: indicates whether to get values of a grid, row, or column
# y: INT: the row in which the spot is located
# x: INT: the column in which the spot is located
# grid: LIST: the 3D array storing the sudoku puzzle
# Returns the other values in the same 3x3 grid, row, or column
def check(region, y, x, grid):
    inner_y = 0
    inner_x = 0
    
    if region is '3x3':
        inner_y = y % 3
        inner_x = x % 3
        
        # Retrieve the values of the 8 other spaces in a 3x3 grid based on inner_y and inner_x position
        if inner_y == 0 and inner_x == 0: # Top left position
            values = [grid[y+1][x][0], grid[y+2][x][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y+2][x+1][0], grid[y][x+2][0], grid[y+1][x+2][0], grid[y+2][x+2][0]]
        elif inner_y == 0 and inner_x == 1: # Top centre position
            values = [grid[y][x-1], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0], grid[y][x+1][0], grid[y+1][x+2][0], grid[y+2][x+2][0]]
        elif inner_y == 0 and inner_x == 2: # Top right position
            values = [grid[y][x-2][0], grid[y+1][x-2][0], grid[y+2][x-2][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0]]
        elif inner_y == 1 and inner_x == 0: # Centre left position
            values = [grid[y-1][x], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y-1][x+2][0], grid[y][x+2][0], grid[y+1][x+2][0]]
        elif inner_y == 1 and inner_x == 1: # Centre centre position
            values = [grid[y-1][x-1], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0]]
        elif inner_y == 1 and inner_x == 2: # Centre right position
            values = [grid[y-1][x-2], grid[y][x-2][0], grid[y+1][x-2][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0]]
        elif inner_y == 2 and inner_x == 0: # Bottom left position
            values = [grid[y-2][x], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y-2][x+2][0], grid[y-1][x+2][0], grid[y][x+2][0]]
        elif inner_y == 2 and inner_x == 1: # Bottom centre position
            values = [grid[y-2][x-1], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0]]
        elif inner_y == 2 and inner_x == 2: # Bottom right position
            values = [grid[y-2][x-2], grid[y-1][x-2][0], grid[y][x-2][0], grid[y-2][x-1][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0]]
        # End if inner_y
        
        return values

    elif region is 'row':
        # Retrieve all values in the same row and delete the current spot
        values = [grid[y][i] for i in range(9)]
        del values[x]
        return values
    else:
        # Retrieve all values in the same column and delete the current spot
        values = [grid[i][x] for i in range(9)]
        del values[y]
        return values
    # End if region
# End check

# This function opens, verifies, and saves the grid indicated by the user
# Returns a list of the location of the file and the grid
def load_grid():
    grid_text = []
    grid_location = input('Please enter the location of the sudoku puzzle to solve: ')

    with open(grid_location, 'r') as grid_raw:
        grid_text = grid_raw.read().splitlines()
    # End with open
    
    # Check for 9 rows, 9 columns, and not all zeroes
    if len(grid_text) == 9:
        return False
    # End if len(grid_text)
    for i in grid_text:
        if len(i) <> 9:
            return False
        # End if len(i)
    # End for i
    if not re.search(r'[^0]', ''.join(grid_text)):
        return False
    # End if not re.search

    # Transfer grid_text to grid
    for y in len(grid):
        for x in len(grid[y]):
            grid[y][x].append(int(grid_text[y][x]))
            
            # Append 1 if the number is permanent or 0 if the number is not
            if grid[y][x][0] == 0:
                grid[y][x].append(0)
            else:
                grid[y][x].append(1)
            # End if grid[y][x][0]
        # End for x
    # End for y
    
    # Check if any numbers are repeated in rows, columns, or 3x3 grids
    for y in len(grid):
        for x in len(grid[y]):
            if grid[y][x][0] is 0:
                continue
            # End if grid[y][x][0]

            if grid[y][x][0] in check('row', y, x, grid):
                return False
            elif grid[y][x][0] in check('column', y, x, grid):
                return False
            elif grid[y][x][0] in check('3x3', y, x, grid):
                return False
            # End if grid[y][x][0]
        # End for x
    # End for y

    return [grid_location, grid]
# End load_grid

# This function fills in spaces that are required to be filled in based on the only available values for a spot
# grid: LIST: the 3D array storing the sudoku puzzle
# Returns a list containing the updated grid and predictions
def mandatory_values(grid, predictions):
    temp_predictions = []
    
    # Check if any row/column/3x3 grid is only missing one number, and insert it permanently if so
    for y in len(grid):
        for x in len(grid[y]):
            # Check row
            values = check('row', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                    predictions[y][x].append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                grid[y][x] = [temp_predictions[0], 1]
                predictions = predictions=[[[] for i in range(9)] for j in range(9)]
                grid, predictions = mandatory_values(grid, predictions)
            else:
                temp_predictions = []
            # End if len(temp_predictions)
            
            # Check column
            values = check('column', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                    predictions[y][x].append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                grid[y][x] = [temp_predictions[0], 1]
                predictions = predictions=[[[] for i in range(9)] for j in range(9)]
                grid, predictions = mandatory_values(grid, predictions)
            else:
                temp_predictions = []
            # End if len(temp_predictions)
            
            # Check 3x3 grid
            values = check('3x3', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                    predictions[y][x].append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                grid[y][x] = [temp_predictions[0], 1]
                predictions = predictions=[[[] for i in range(9)] for j in range(9)]
                grid, predictions = mandatory_values(grid, predictions)
            else:
                temp_predictions = []
            # End if len(temp_predictions)
            
            predictions[y][x] = list(set(predictions[y][x])) # Remove duplicate predictions
        # End for x
    # End for y
    
    # If any predicted number only appears once in a row/column/3x3 grid, permanently set it
    # Check row
    for y in range(9):
        for x in range(9):
            for i in predictions[y][x]:
                temp_predictions.append(i)
            # End for i
        # End for x
        
        temp_predictions = ''.join(temp_predictions)     
        for i in range(1, 10):
            if len(re.findall(i, temp_predictions)) == 1: # Predicted value found only once in row
                
