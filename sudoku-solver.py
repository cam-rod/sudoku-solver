# Cameron Rodriguez
# April 25, 2019
# This program will dynamically solve a sudoku grid.

"""
Data Dictionary

grid: LIST: stores sudoku grid in 3D array; in third dimension, the first element is the number and the second indicates permanent
predictions: LIST: a 3D array parallel to grid; the third dimension is a list of potential values for each spot in grid
result:  LIST: stores returned value of fill_grid() with confirmation of puzzle solution and the updated grid if so
y: INT: indicates the row the program is checking from the top
x: INT: indicates the column the program is checking from the left
grid_location: STR: contains the user inputted location of the game data
end_screen: CLASS: calls the endgame class
root: CLASS: contains the tkinter frame

values: LIST: a list of values found in the same 3x3 grid, row, or column as grid[y][x]
inner_y: INT: indicates the row of grid[y][x] relative to its 3x3 grid
inner_x: INT: indicates the column of grid[y][x] relative to its 3x3 grid
grid_raw: FILE: the opened file of the source puzzle
grid_text: LIST: list of sudoku puzzle rows
temp_predictions: LIST: temporarily stores a list of all values not found in a row/column/3x3 inner grid
successful: BOOL: indicates if all mandatory values in rows/column are saved, or if puzzle was successfully solved
updated: BOOL: indicates if any values have been added due to being the only missing spot in a line
final_grid: LIST: stores a boolean if the puzzle has been successfully solved, and the grid itself if True
"""

import re # Used to verify the puzzle as valid
import Tkinter as tk # Used to generate graphical output

# Loads empty 3D arrays with 9 lists within 9 lists
grid = [[[] for i in range(9)] for j in range(9)]
predictions=[[[] for i in range(9)] for j in range(9)]

result = []
values = []
y = 0
x = 0
grid_location = ''
successful = False
end_screen = None
root = None

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
            values = [grid[y][x-1][0], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y+2][x+1][0]]
        elif inner_y == 0 and inner_x == 2: # Top right position
            values = [grid[y][x-2][0], grid[y+1][x-2][0], grid[y+2][x-2][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y+2][x-1][0], grid[y+1][x][0], grid[y+2][x][0]]
        elif inner_y == 1 and inner_x == 0: # Centre left position
            values = [grid[y-1][x][0], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0], grid[y-1][x+2][0], grid[y][x+2][0], grid[y+1][x+2][0]]
        elif inner_y == 1 and inner_x == 1: # Centre centre position
            values = [grid[y-1][x-1][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y+1][x+1][0]]
        elif inner_y == 1 and inner_x == 2: # Centre right position
            values = [grid[y-1][x-2][0], grid[y][x-2][0], grid[y+1][x-2][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y+1][x-1][0], grid[y-1][x][0], grid[y+1][x][0]]
        elif inner_y == 2 and inner_x == 0: # Bottom left position
            values = [grid[y-2][x][0], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0], grid[y-2][x+2][0], grid[y-1][x+2][0], grid[y][x+2][0]]
        elif inner_y == 2 and inner_x == 1: # Bottom centre position
            values = [grid[y-2][x-1][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0], grid[y-2][x+1][0], grid[y-1][x+1][0], grid[y][x+1][0]]
        elif inner_y == 2 and inner_x == 2: # Bottom right position
            values = [grid[y-2][x-2][0], grid[y-1][x-2][0], grid[y][x-2][0], grid[y-2][x-1][0], grid[y-1][x-1][0], grid[y][x-1][0], grid[y-2][x][0], grid[y-1][x][0]]
        # End if inner_y
        
        return values

    elif region is 'row':
        # Retrieve all values in the same row and delete the current spot
        values = [grid[y][i][0] for i in range(9)]
        del values[x]
        return values
    else:
        # Retrieve all values in the same column and delete the current spot
        values = [grid[i][x][0] for i in range(9)]
        del values[y]
        return values
    # End if region
# End check

# This function opens, verifies, and saves the grid indicated by the user
# Returns a list of the location of the file and the grid
def load_grid():
    grid_text = []
    grid_location = raw_input('Please enter the location of the sudoku puzzle to solve: ')

    with open(grid_location, 'r') as grid_raw:
        grid_text = grid_raw.read().splitlines()
    # End with open
    
    # Check for 9 rows, 9 columns, and not all zeroes
    if len(grid_text) <> 9:
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
    for y in range(len(grid)):
        for x in range(len(grid[y])):
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
    for y in range(len(grid)):
        for x in range(len(grid[y])):
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

# This function recursively fills spaces where a prediction is the only one in its row or column.
# grid: LIST: the 3D array storing the sudoku puzzle
# predictions: LIST: parallel to array; stores potential values for grid
# successful: BOOL: indicates if all mandatory values in rows/column are saved
# form: STR: indicates whether to check rows or columns
# Returns a list containing the updated grid, predictions, and successful
def mandatory_predictions(grid, predictions, successful, form):
    for i in range(9):
        temp_predictions = []
        
        # Add all predictions to a list
        for j in range(9):
            if form == 'row':
                for k in predictions[i][j]:
                    if grid[i][j][1] <> 1:
                        temp_predictions.append(k)
                    # End if grid[i][j][1]
                # End for k
            else:
                for k in predictions[j][i]:
                    if grid[j][i][1] <> 1:
                        temp_predictions.append(k)
                    # End if grid[j][i][1]
                # End for k
            # End if form
        # End for j
        
        # Check if a number is only predicted once in row/column, and add if so     
        for k in range(1, 10):
            if temp_predictions.count(k) == 1:
                for j in range(9):
                    if form =='row':
                        for l in predictions[i][j]:
                            if l == k:
                                if grid[i][j][1] <> 1:
                                    grid[i][j] = [k, 1]
                                    predictions = [[[] for a in range(9)] for b in range(9)]
                                    grid, predictions, successful = mandatory_values(grid, predictions, successful)
                                # End if predictions[i][j][1]
                            # End if l
                            if successful:
                                break
                            # End if successful
                        # End for l
                        if successful:
                            break
                        # End if successful
                    else:
                        for l in predictions[j][i]:
                            if l == k:
                                if grid[j][i][1] <> 1:
                                    grid[j][i] = [k, 1]
                                    predictions = [[[] for a in range(9)] for b in range(9)]
                                    grid, predictions, successful = mandatory_values(grid, predictions, successful)
                                # End if predictions[j][i][1]
                            # End if l
                            if successful:
                                break
                            # End if successful
                        # End for l
                        if successful:
                            break
                        # End if successful                        
                    # End if form
                # End for j
            # End if len
            if successful:
                break
        # End for k
        if successful:
            break
        # End if successful
    # End for i
    
    return [grid, predictions, successful]
# End mandatory_predictions

# This function fills in spaces that are required to be filled in based on the only available values for a spot
# grid: LIST: the 3D array storing the sudoku puzzle
# predictions: LIST: parallel to array; stores potential values for grid
# successful: BOOL: indicates if all mandatory values in rows/column are saved
# Returns a list containing the updated grid, predictions, and a True boolean
def mandatory_values(grid, predictions, successful):
    temp_predictions = []
    updated = False
    
    # Check if any row/column/3x3 grid is only missing one number, and insert it permanently if so
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Check row
            values = check('row', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                    predictions[y][x].append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                if grid[y][x][1] <> 1:
                    grid[y][x] = [temp_predictions[0], 1]
                    updated = True
                # End if grid[y][x][1]
            # End if len(temp_predictions)
            temp_predictions = []
            
            # Check column
            values = check('column', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                if grid[y][x][1] <> 1:
                    grid[y][x] = [temp_predictions[0], 1]
                    updated = True
                # End if grid[y][x][1]
            elif len(temp_predictions) > 1:
                # Remove any predictions that cannot also exist in the column in reverse order
                for i in range(len(predictions[y][x])-1, -1, -1):
                    if predictions[y][x][i] not in temp_predictions:
                        del predictions[y][x][i]
                    # End if i
                # End for i
            # End if len(temp_predictions)
            temp_predictions = []
            
            # Check 3x3 grid
            values = check('3x3', y, x, grid)
            for i in range(1, 10):
                if i not in values:
                    temp_predictions.append(i)
                # End if i
            # End for i
            
            if len(temp_predictions) == 1:
                if grid[y][x][1] <> 1:
                    grid[y][x] = [temp_predictions[0], 1]
                    updated = True
                # End if grid[y][x][1]
            elif len(temp_predictions) > 1:
                # Remove any predictions that cannot also exist in the 3x3 grid in reverse order
                for i in range(len(predictions[y][x])-1, -1, -1):
                    if predictions[y][x][i] not in temp_predictions:
                        del predictions[y][x][i]
                    # End if i
                # End for i
            # End if len(temp_predictions)
            temp_predictions = []
        # End for x
    # End for y
    
    if updated:
        predictions = [[[] for i in range(9)] for j in range(9)]
        grid, predictions, successful = mandatory_values(grid, predictions, successful)    
    
    # If any predicted number only appears once in a row or column, permanently set it
    grid, predictions, successful = mandatory_predictions(grid, predictions, successful, 'row')
    
    # Check column, skip if all mandatory values saved
    if not successful:
        grid, predictions, successful = mandatory_predictions(grid, predictions, successful, 'column')    
    # End if not successful
    
    return [grid, predictions, True]
# End mandatory_values

# This function recursively fills the remaining spaces in the puzzle based on predictions
# grid: LIST: the 3D array storing the sudoku puzzle
# predictions: LIST: parallel to array; stores potential values for grid
def fill_grid(grid, predictions):
    final_grid = []
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Skip if permanent number or previously guesses
            if grid[y][x][1] == 1 or grid[y][x][0] <> 0:
                continue
            # End if grid[y][x][1]
            
            # Test the validity of each prediction, and set value if so
            for i in predictions[y][x]:
                if i in check('row', y, x, grid):
                    continue
                elif i in check('column', y, x, grid):
                    continue
                elif i in check ('3x3', y, x, grid):
                    continue
                else:
                    grid[y][x][0] = i
                    
                    final_grid = fill_grid(grid, predictions)
                    if final_grid[0] is True:
                        # The puzzle is solved successfully
                        return final_grid
                    else:
                        continue
                    # End if final_grid
                # End if i
            # End for i
            
            # Returns False if the program cannot successfully enter a value
            grid[y][x][0] = 0
            return [False]
        # End for x
    # End for y
    
    # Returns True and grid if all spots filled successfully
    return [True, grid]
# End fill_grid

# This class creates a Tkinter window to either display a solved puzzle and save it, or deliver an error message
# tk.Frame: CLASS: provides the Tkinter frame to the class
class DeliverResult(tk.Frame):
    # This function imports variables into the class and initializes the Tkinter window
    # grid: LIST: the 3D array storing the sudoku puzzle
    # grid_location: STR: contains the user inputted location of the game data
    # successful: BOOL: indicates if the puzzle was solved successfully
    def __init__(self, grid, grid_location, successful, master=None):
        self.grid = grid
        self.grid_location = grid_location
        self.successful = successful

        # Initialize window
        tk.Frame.__init__(self, master)
        self.create_window()
    # End __init__

    # This function creates the window to display the result, varying based on whether the puzzle was solved.
    def create_window(self):
        root.lift()
        root.configure(bg='white')
        root.wm_attributes('-topmost', 'true')
        try:
            root.wm_iconbitmap('icon.ico')        
        except tk.TclError:
            pass
        # End try/except
        if self.successful:
            # Save the solution file in the same location as the initial file
            self.grid_location = self.grid_location[:-4] + '_solution.txt'
            with open(self.grid_location, 'w') as grid_raw:
                for y in range(len(self.grid)):
                    for x in range(len(self.grid[y])):
                        grid_raw.write('{}'.format(self.grid[y][x][0]))
                    # End for x
                    if y <> 8:
                        grid_raw.write('\n')
                    # End if y
                # End for y
            # End with open(self.grid_location)

            # Create a window with a grid of the solution and a message on the location of the file
            self.master.title('Solution')
            for y in range(len(self.grid)):
                for x in range(len(self.grid[x])):
                    tk.Label(text = '{}'.format(str(self.grid[y][x][0])), justify='center', width=1, bg='white',
                             borderwidth=1, relief='solid').grid(column = x, row = y, sticky='NSEW')
                # End for x
            # End for y

            tk.Label(text = 'The solution file is saved at {}.'.format(self.grid_location), wraplength=200,
                     justify='center', anchor='center', height=6, bg='white').grid(column=0,
                     columnspan=9, row=9)
            tk.Button(text = 'Ok', command = root.destroy).grid(column=10, row=9)
        else:
            # Create a window telling the user that the puzzle cannot be solved
            self.master.title('Invalid Puzzle')
            tk.Label(text='This sudoku puzzle cannot be solved.', width=36, bg='white',
                     justify='center').grid(column=0, row=0, sticky='NSEW')
            tk.Button(text = 'Ok', command = root.destroy, anchor='center').grid(row=1)

# Request and load the puzzle into the solver
grid = load_grid()

if grid == False:
    root = tk.Tk()
    end_screen = DeliverResult(grid, grid_location, successful, master=root)
    end_screen.mainloop()
else:
    grid_location, grid = grid

    # Fill in spaces that cannot have other values
    grid, predictions, successful = mandatory_values(grid, predictions, successful)
    successful = False
    
    # Fill in all other spaces
    result = fill_grid(grid, predictions)
    
    # Deliver solution or failure message
    if result[0] == True:
        successful, grid = result
    # End if result[0]
    
    root = tk.Tk()
    end_screen = DeliverResult(grid, grid_location, successful, master=root)
    end_screen.mainloop()
# End if grid
