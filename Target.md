# Goals

## File formats

- **INPUT:** ```00#000#0#``` (x9) wherein a zero represents a spot to be filled.
- **OUTPUT:** (x9) {or Pygame fancy output in a grid}

```
|----------------------|
|1 2 3 | 4 5 6 | 7 8 9 |
```

- **3x3 groupings**: [0-2][0-2], [0-2][3-5], [0-2][6-8], [3-5][0-2], [3-5][3-5], [3-5][6-8], [6-8][0-2], [6-8][3-5], [6-8][6-8]

## Requirements

- Reads puzzle from text file
- Loads data into grid (source format at top)
- Brute force the solution
  - Check vertically
  - Check horizontally
  - Check 3x3 grid (dynamically and hard coded)
  - ***Optional: solve with dynamic methods***
- Display result
  - Output final solution with Pygame and save to a file
  - Identify and declare unsolvable puzzles
  
## Potential dynamic methods

### Prediction method #1

***Phase 1***

- Each spot will be checked vertically, horizontally, and 3x3 for possible solutions *independently* of each other
  - Any spots that must be filled (only number in space) in do so immediately and enter the "hard-coded" base, causing the previous step to repeat immediately
  - *Repeat these steps until no new spaces are forced to be added*
- Select, in this order, rows/columns/3x3
  - Check by number generally following the previous pattern (i.e. if any number appears once) "hard-code" the number and restart from step 1

***Phase 2***

- ***{Specialized brute force}*** In reading order, select a valid number for a square
  - Check that square's column/row/3x3 for any numbers affected by this choice; **RECURSION AS NECESSARY**
  - After all filled, move to next spot
  - If fails, hop down recursion and try another valid number
  - Continue until all spaces are filled.

## Layout

- Request the file
- Verify the file as valid (file.readlines())
  - Ensure the file is 9x9 and numbers only
  - Immediately invalidate if all numbers are 0
  - Check for repeated numbers in row/column/3x3, invalidate if necessary
  - PRINT AN ERROR MESSAGE
- Load file into system (**ARRAY + predictions, please don't actually use these names**)
  - **grid:** actual input of numbers (including 0) format [column][row], where second value is boolean for locked
  - **predictions:** overlaid onto the arrays, this contains dynamic predictions for each spot as an inner list (empty predictions read 0)
- Run *Phase 1* of dynamic method using ```while True``` loop (with 2 inner loops) and *continue* statements
  - any non-certain statements are loaded into ```Predictions```
- Run *Phase 2* using recursion within ```for``` statements
- FINISH:
  - If the puzzle is solved, print using Pygame and ```Predictions``` AND save file by modifying source file name to ```LOCATION/FILE-solution.txt```
  - If the puzzle is not solved, print message