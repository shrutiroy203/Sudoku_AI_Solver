from utils import *
import time
import numpy as np


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist.append([r+c for r,c in zip(rows,cols)] ) #add diagonal1
unitlist.append([r+c for r,c in zip(rows[::-1],cols)]) # add diagonal2

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.
    """
    new_values = values.copy()
    #find the twins:
    two_digits = [t for t in values if len(new_values[t])==2]
    
    #Create a dictionary for the same values
    same_values =  {i:p for i in two_digits for p in peers[i] if (new_values[i]==new_values[p])}
 
    #Replace numbers            
    for v in same_values:
        all_peers = set(peers[v]).intersection(set(peers[same_values[v]]))
        for p in all_peers:
            for n in new_values[v]:
                new_values[p]=new_values[p].replace(n,'')
    
    return new_values
    

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        

        # Use the Only Choice Strategy
        values = only_choice(values)
        
        # Use the naked twins strategy

        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # Add for visualization
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    
    values = reduce_puzzle(values)

    if values is False:
        return False
    if all(len(values[s])==1 for s in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    s = min(values.items(),key=lambda x:len(x[1]) if len(x[1])>1 else 1000)[0]
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = v
        attempt = search(new_sudoku)
        if attempt:
            return attempt



def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    answer = input("would you like to input 3x3 sudoku? (y/n)")
    if answer=='y':
        sudoku_solve=''
        print("Enter numbers as you go on sudoku bord from left to right")
        for i in range(len(diag_sudoku_grid)):
            c=input(f"Input number {i}: ")
            sudoku_solve+=''
        print("Here is the input sudoku puzzle:")
        display(convert2grid(sudoku_solve))
    else: 
        print("Using the default generated sudoku puzzle:")
        display(convert2grid(diag_sudoku_grid))
    t0 = time.time()
    result = solve(diag_sudoku_grid)
    t1 = time.time()
    print(f"Here is the result solved in {np.round(t1-t0,3)}seconds")
    display(result)
