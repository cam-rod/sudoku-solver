# Goals

## File formats

- **INPUT:** ```00#000#0#``` (x9) wherein a zero represents a spot to be filled.
- **OUTPUT:** (x9) {or Pygame fancy output in a grid}

```
|----------------------|
|1 2 3 | 4 5 6 | 7 8 9 |
```

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

- Each spot will be checked vertically, horizontally, and 3x3 for possible solutions *indepedently* of each other
  - Any spots that must be filled (only number in space) in do so immediately and enter the "hard-coded" base, causing the previous step to repeat immediately
  - *Repeat these steps until no new spaces are forced to be added*
- Select, in this order, rows/columns/3x3
  - Check by number generally following the previous pattern (i.e. if any number appears once) "hard-code" the number and restart from step 1
- ***{Specialized brute force}*** In top-left bottom-right order, select a valid number for a square
  - Check that square's column/row/3x3 for any numbers affected by this choice; **RECURSION AS NECESSARY**
  - After all filled, move to next spot
  - If fails, hop down recursion and try another valid number
  - Continue until all spaces are filled.
