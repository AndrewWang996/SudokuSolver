from copy import deepcopy

#
# slow as fuck Sudoku Puzzle Solver
#    written by Andy
#
# Example:
#
# board(
#  [[5,3,0,0,7,0,0,0,0],
#   [6,0,0,1,9,5,0,0,0],
#   [0,9,8,0,0,0,0,6,0],
#   [8,0,0,0,6,0,0,0,3],
#   [4,0,0,8,0,3,0,0,1],
#   [7,0,0,0,2,0,0,0,6],
#   [0,6,0,0,0,0,2,8,0],
#   [0,0,0,4,1,9,0,0,5],
#   [0,0,0,0,8,0,0,7,9]]
# ).solve()
#
#

class fuckedUp(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class cell:
    def __init__(self, square, row, column, r, c):
        self.square = square
        self.row = row
        self.column = column
        self.allowed = set(range(1,10))
        self.r, self.c = r, c
        self.N = None
    
    def setTo(self, n):
        if not 1 <= n <= 9:
            return
        if not n in self.allowed:
            raise fuckedUp('not allowed to set to this value')
        self.N = n
        self.allowed = set()

                        # may raise Exception
        self.square.eliminate(n)
        self.row.eliminate(n)
        self.column.eliminate(n)

    def alreadySet(self):
        return self.N != None
        
    def eliminate(self, n):
        if n in self.allowed:
            self.allowed.remove(n)
    
class square:
    def __init__(self):
        self.cells = [[None for i in range(3)] for j in range(3)]
    
    def setCell(self, r, c, theCell):
        self.cells[r][c] = theCell
    
    def eliminate(self, n):
        for i in range(3):
            for j in range(3):
                self.cells[i][j].eliminate(n) # may raise Exception

class line:
    def __init__(self):
        self.cells = [None for i in range(9)]

    def setCell(self, i, theCell):
        self.cells[i] = theCell

    def eliminate(self, n):
        for i in range(9):
            self.cells[i].eliminate(n) # may raise Exception

class board:
    def __init__(self, numbers):
        self.squares = [[square() for i in range(3)] for j in range(3)]
        self.rows = [line() for r in range(9)]
        self.columns = [line() for c in range(9)]
        self.cells = [[None for r in range(9)] for c in range(9)]
        for r in range(9):
            for c in range(9):
                self.cells[r][c] = cell( self.squares[r/3][c/3],
                                         self.rows[r],
                                         self.columns[c],
                                         r, c )
                self.rows[r].setCell(c, self.cells[r][c])
                self.columns[c].setCell(r, self.cells[r][c])
                self.squares[r/3][c/3].setCell(r%3, c%3, self.cells[r][c])
        
        for r in range(9):
            for c in range(9):
                self.cells[r][c].setTo( numbers[r][c] )

    def copy(self):
        return deepcopy(self)

    def nextCoord(self, (r, c)):
        if r >= 8 and c >= 8:
            return None
        if c >= 8:
            return (r+1, 0)
        return (r, c+1)
    
    def recursion(self, (r,c)):
        if r >= 8 and c >= 8:
            return [str(self.copy())]

        if self.cells[r][c].alreadySet():
            return self.recursion(self.nextCoord((r,c)))
        
        solutions = []
        for n in self.cells[r][c].allowed:
            newBoard = self.copy()
            try:
                newBoard.cells[r][c].setTo(n)
                coord = newBoard.nextCoord((r,c))
                solutions.extend(newBoard.recursion(coord))
            except fuckedUp as motherfucker:
                continue
        return solutions
    
    def solve(self):
        return self.recursion((0,0))

    def __str__(self):
        return '\n'.join(
            str([c.N if c.N != None else 0 for c in L]) for L in self.cells)




b2 = board(
[[7,0,0,3,0,0,6,0,0],
 [0,0,0,0,6,0,8,0,5],
 [0,0,6,0,7,9,0,0,1],
 [0,6,0,8,3,0,1,0,9],
 [0,0,0,0,0,0,0,0,0],
 [3,0,8,0,9,4,0,6,0],
 [9,0,0,2,4,0,7,0,0],
 [8,0,2,0,1,0,0,0,0],
 [0,0,4,0,0,5,0,0,3]]
)

solutions = b2.solve()
print('number of solutions = %i' %len(solutions))
for sol in solutions:
    print(sol)
    print('\n' * 3)


# http://www.comp.nus.edu.sg/~cs1101x/3_ca/labs/07s1/lab7/img/sudoku.gif
'''
board = 
[[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]]

board.solve() ==
[[5,3,4,6,7,8,9,1,2],
[6,7,2,1,9,5,3,4,8],
[1,9,8,3,4,2,5,6,7],
[8,5,9,7,6,1,4,2,3],
[4,2,6,8,5,3,7,9,1],
[7,1,3,9,2,4,8,5,6],
[9,6,1,5,3,7,2,8,4],
[2,8,7,4,1,9,6,3,5],
[3,4,5,2,8,6,1,7,9]]
'''













    
        
