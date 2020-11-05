#!/usr/bin/env python
#coding:utf-8
import sys
import time
'''
AI code for solving sudoku puzzles
Zachery Macintyre zim2103
'''

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)



class Variable(object):
    '''
    creates a variable object for all the variables on the board
    '''
    def __init__(self, name):
        
        self.domain = set(range(1,10))
        self.name = name
        self.relations = set()
        self.value = 0


def make_relations(var, assignment):
    '''
    Method to make relations of every unassigned variable
    allows to forward and consistent check easy
    '''    
    for key in assignment:
        if assignment[key].name == var.name:
            pass
        else:
            if assignment[key].name[0] == var.name[0]:         #checks the row
                var.relations.add(assignment[key])
    
            if assignment[key].name[1] == var.name[1]:         #checks the row
                var.relations.add(assignment[key])
                
            if get_grid(assignment[key].name) == get_grid(var.name):   #checks the grid
                var.relations.add(assignment[key])         


def update_domain(var, assignment):
    '''
    Method to update the domains of unassigned variables
    '''    
    for key in assignment:
        if assignment[key].name[0] == var.name[0]:         #updates the row
            if assignment[key].value in var.domain:
                var.domain.remove(assignment[key].value)

        if assignment[key].name[1] == var.name[1]:         #updates the row
            if assignment[key].value in var.domain:
                var.domain.remove(assignment[key].value)
            
        if get_grid(assignment[key].name) == get_grid(var.name):   #updates the grid
            if assignment[key].value in var.domain:
                var.domain.remove(assignment[key].value)         

    
def get_grid(name):
    '''
    Helper method to get the grid that each variable is assinged to
    '''    
    grid = ''
    if name[0] in 'ABC':
        grid += '0'
    elif name[0] in 'DEF':
        grid += '1'
    else:
        grid += '2'
    grid += str((int(name[1]) -1)  // 3) 
    return grid
    
    
    
def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    assignments = {}
    
    for key in board:
        new_variable = Variable(key)            #creates a new variable
        if board[key] != 0: 
            new_variable.value = board[key]
            new_variable.domain.clear()                
        assignments[key] = new_variable         #adds variable to assignment
        
    for key in assignments:
        if assignments[key].value == 0:
            update_domain(assignments[key], assignments)   #updates domins of variables
            make_relations(assignments[key], assignments)  #creates a relation set 
    
    
    backtrack(assignments, board) 

    solved_board =  board  
    return solved_board
    


def backtrack(assignments, board):
    '''
    takes in a dictionary of assignments and the sudoku board
    outputs False or the correct sudoku board if it is solveable
    Follows book psuedo code 
    '''
    
    if(complete(assignments, board)):
        return assignments
    
    var = unassigned_MRV(assignments)      #gets MRV Variable 
    domain = set(var.domain)               #gets domain
    
    for i in domain:
        #print(i)
        if (consistent(var, i)):           #consistency check
            #print('CONS')
            undo_state = state_saver(assignments)   #state saver if the i is consistent for domain
            if (forward(var, i)):
                var.value = i
                var.domain.clear()
                
                result = backtrack(assignments, board)    
                
                if result != False:
                    return result
                
                var.value = 0                #undoes any assignment
        
        for states in undo_state:
            #print(states[0].name, states[1])
            assignments[states[0]].domain = states[1]
    
    return False


def unassigned_MRV(assignment):
    '''
    Is a function that gets the MRV variable in the assignment
    in put is assignment dictionary
    '''        
    
    low = 10
    return_node = None
    for name in assignment:
        if len(assignment[name].domain) < low and len(assignment[name].domain) != 0:
            low = len(assignment[name].domain)
            return_node = assignment[name]
    
    return return_node


def consistent(variable, value):  
    '''
    Chacks to make sure the the variable is allowed to be placed in that position
    by making sure it wouldnt break the board by having the same number in the same row
    col, or grid
    returns true or false
    '''
    
    for relate in variable.relations:
        if relate.value == value:
            return False 

    return True 


def forward(variable, value):
    '''
    checks the board to make sure that by placing the value it does not limit 
    future values to a domain of 0.  IF that is true it will update the domains 
    of future variables
    '''
        
    for relate in variable.relations:
        if value in relate.domain:
            if len(relate.domain) == 1:
                return False
    
    for relate in variable.relations:
        if value in relate.domain:        
            relate.domain.remove(value)
    
        
    return True 
    
def state_saver(assignment):
    '''
    In in order to back track we need to keep track of previous states
    this method does so by making a list of tuples that have the name and the 
    domain set.  It will be readded if a state is false
    '''
    
    state = []
    for key in assignment:
        state.append((assignment[key].name, set(assignment[key].domain)))
    
    return state 

def complete(assignment, board):
    '''
    Checks to see if all assignments have been filled
    if this is true it returns the filled out board
    '''
    
    for key in assignment:
        if assignment[key].value == 0:
            return False
    
    for key in assignment:
        board[assignment[key].name] = assignment[key].value
    
    return True



if __name__ == '__main__':

    if len(sys.argv) > 1:

        #  Read individual board from command line arg.
        sudoku = sys.argv[1]

        if len(sudoku) != 81:
            print("Error reading the sudoku string %s" % sys.argv[1])
        else:
            board = { ROW[r] + COL[c]: int(sudoku[9*r+c])
                      for r in range(9) for c in range(9)}
            
            print_board(board)

            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()

            print_board(solved_board)

            out_filename = 'output.txt'
            outfile = open(out_filename, "w")
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

    else:

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        li = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                    for r in range(9) for c in range(9)}

            # Print starting board.
            print_board(board)

            # Solve with backtracking
            start_time = time.time()
            solved_board = backtracking(board)
            end_time = time.time()
            li.append(end_time-start_time)
            
            
            # Print solved board. 
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

print("Finishing all boards in file.")  








              