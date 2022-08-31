def getel(s):
    """Returns the unique element in a singleton set (or list)."""
    assert len(s) == 1
    return list(s)[0]
import json

class Sudoku(object):

    def __init__(self, elements):
        """Elements can be one of:
        Case 1: a list of 9 strings of length 9 each.
        Each string represents a row of the initial Sudoku puzzle,
        with either a digit 1..9 in it, or with a blank or _ to signify
        a blank cell.
        Case 2: an instance of Sudoku.  In that case, we initialize an
        object to be equal (a copy) of the one in elements.
        Case 3: a list of list of sets, used to initialize the problem."""
        if isinstance(elements, Sudoku):
            # We let self.m consist of copies of each set in elements.m
            self.m = [[x.copy() for x in row] for row in elements.m]
        else:
            assert len(elements) == 9
            for s in elements:
                assert len(s) == 9
            # We let self.m be our Sudoku problem, a 9x9 matrix of sets.
            self.m = []
            for s in elements:
                row = []
                for c in s:
                    if isinstance(c, str):
                        if c.isdigit():
                            row.append({int(c)})
                        else:
                            row.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
                    else:
                        assert isinstance(c, set)
                        row.append(c)
                self.m.append(row)


    def show(self, details=False):
        """Prints out the Sudoku matrix.  If details=False, we print out
        the digits only for cells that have singleton sets (where only
        one digit can fit).  If details=True, for each cell, we display the
        sets associated with the cell."""
        if details:
            print("+-----------------------------+-----------------------------+-----------------------------+")
            for i in range(9):
                r = '|'
                for j in range(9):
                    # We represent the set {2, 3, 5} via _23_5____
                    s = ''
                    for k in range(1, 10):
                        s += str(k) if k in self.m[i][j] else '_'
                    r += s
                    r += '|' if (j + 1) % 3 == 0 else ' '
                print(r)
                if (i + 1) % 3 == 0:
                    print("+-----------------------------+-----------------------------+-----------------------------+")
        else:
            print("+---+---+---+")
            for i in range(9):
                r = '|'
                for j in range(9):
                    if len(self.m[i][j]) == 1:
                        r += str(getel(self.m[i][j]))
                    else:
                        r += "."
                    if (j + 1) % 3 == 0:
                        r += "|"
                print(r)
                if (i + 1) % 3 == 0:
                    print("+---+---+---+")


    def to_string(self):
        """This method is useful for producing a representation that
        can be used in testing."""
        as_lists = [[list(self.m[i][j]) for j in range(9)] for i in range(9)]
        return json.dumps(as_lists)


    @staticmethod
    def from_string(s):
        """Inverse of above."""
        as_lists = json.loads(s)
        as_sets = [[set(el) for el in row] for row in as_lists]
        return Sudoku(as_sets)


    def __eq__(self, other):
        """Useful for testing."""
        return self.m == other.m
from nose.tools import assert_equal

sd = Sudoku([
    '53__7____',
    '6__195___',
    '_98____6_',
    '8___6___3',
    '4__8_3__1',
    '7___2___6',
    '_6____28_',
    '___419__5',
    '____8__79'
])
sd.show()
sd.show(details=True)
s = sd.to_string()
sdd = Sudoku.from_string(s)
sdd.show(details=True)
assert_equal(sd, sdd)


class Unsolvable(Exception):
    pass


def sudoku_ruleout(self, i, j, x):
    """The input consists in a cell (i, j), and a value x.
    The function removes x from the set self.m[i][j] at the cell, if present, and:
    - if the result is empty, raises Unsolvable;
    - if the cell used to be a non-singleton cell and is now a singleton
      cell, then returns the set {(i, j)};
    - otherwise, returns the empty set."""
    c = self.m[i][j]
    n = len(c)
    c.discard(x)
    self.m[i][j] = c
    if len(c) == 0:
        raise Unsolvable()
    return {(i, j)} if 1 == len(c) < n else set()

Sudoku.ruleout = sudoku_ruleout


### Exercise: define cell propagation

def sudoku_propagate_cell(self, ij):
    """Propagates the singleton value at cell (i, j), returning the list
    of newly-singleton cells."""
    i, j = ij
    if len(self.m[i][j]) > 1:
        # Nothing to propagate from cell (i,j).
        return set()
    # We keep track of the newly-singleton cells.
    newly_singleton = set()
    x = getel(self.m[i][j]) # Value at (i, j).
    # Same row.
    for jj in range(9):
        if jj != j: # Do not propagate to the element itself.
            newly_singleton.update(self.ruleout(i, jj, x))
    # Same column.
    # YOUR CODE HERE
    for ii in range(9):
        if ii != i:
            newly_singleton.update(self.ruleout(ii, j, x))

    # Same block of 3x3 cells.
    # YOUR CODE HERE
    # x0 = 0
    # x1 = 3
    # y0 = 0
    # y1 = 3

    # if i > 2 and i < 6:
    #     x0 = 3
    #     x1 = 6
    # elif i >= 6:
    #     x0 = 6
    #     x1 = 9

    # if j > 2 and j < 6:
    #     y0 = 3
    #     y1 = 6
    # elif j >= 6:
    #     y0 = 6
    #     y1 = 9



    for k in range(i//3*3,i//3*3+3):
        for l in range(j//3*3,j//3*3+3):
            if self.m[k][l] != self.m[i][j]:
                newly_singleton.update(self.ruleout(k, l, x))


    # Returns the list of newly-singleton cells.
    return newly_singleton

Sudoku.propagate_cell = sudoku_propagate_cell


def sudoku_propagate_all_cells_once(self):
    """This function propagates the constraints from all singletons."""
    for i in range(9):
        for j in range(9):
            self.propagate_cell((i, j))

Sudoku.propagate_all_cells_once = sudoku_propagate_all_cells_once

### Exercise: define full propagation

def sudoku_full_propagation(self, to_propagate=None):
    """Iteratively propagates from all singleton cells, and from all
    newly discovered singleton cells, until no more propagation is possible.
    @param to_propagate: sets of cells from where to propagate.  If None, propagates
        from all singleton cells. 
    @return: nothing.
    """
    if to_propagate is None:
        to_propagate = {(i, j) for i in range(9) for j in range(9)}
    # This code is the (A) code; will be referenced later.
    # YOUR CODE HERE

    while len(to_propagate) > 0:
        to_propagate.update(self.propagate_cell(to_propagate.pop()))
    return
    


Sudoku.full_propagation = sudoku_full_propagation

def sudoku_done(self):
    """Checks whether an instance of Sudoku is solved."""
    for i in range(9):
        for j in range(9):
            if len(self.m[i][j]) > 1:
                return False
    return True

Sudoku.done = sudoku_done


def sudoku_search(self, new_cell=None):
    """Tries to solve a Sudoku instance."""
    to_propagate = None if new_cell is None else {new_cell}
    self.full_propagation(to_propagate=to_propagate)
    if self.done():
        return self # We are a solution
    # We need to search.  Picks a cell with as few candidates as possible.
    candidates = [(len(self.m[i][j]), i, j)
                   for i in range(9) for j in range(9) if len(self.m[i][j]) > 1]
    _, i, j = min(candidates)
    values = self.m[i][j]
    # values contains the list of values we need to try for cell i, j.
    # print("Searching values", values, "for cell", i, j)
    for x in values:
        # print("Trying value", x)
        sd = Sudoku(self)
        sd.m[i][j] = {x}
        try:
            # If we find a solution, we return it.
            return sd.search(new_cell=(i, j))
        except Unsolvable:
            # Go to next value.
            pass
    # All values have been tried, apparently with no success.
    raise Unsolvable()

Sudoku.search = sudoku_search


def sudoku_solve(self, do_print=True):
    """Wrapper function, calls self and shows the solution if any."""
    try:
        r = self.search()
        if do_print:
            print("We found a solution:")
            r.show()
            return r
    except Unsolvable:
        if do_print:
            print("The problem has no solutions")

Sudoku.solve = sudoku_solve


### Exercise: define full propagation with where can it go

def sudoku_full_propagation_with_where_can_it_go(self, to_propagate=None):
    """Iteratively propagates from all singleton cells, and from all
    newly discovered singleton cells, until no more propagation is possible."""
    if to_propagate is None:
        to_propagate = {(i, j) for i in range(9) for j in range(9)}
    while len(to_propagate) > 0:
        # Here is your previous solution code from (A) in full_propagation.
        # Please copy it below. No change is required. 
        # YOUR CODE HERE
        while len(to_propagate) > 0:
            to_propagate.update(self.propagate_cell(to_propagate.pop()))
        
        # Now we check whether there is any other propagation that we can
        # get from the where can it go rule.
        to_propagate = self.where_can_it_go()

### Exercise: define helper function to check once-only occurrence

from collections import defaultdict

def occurs_once_in_sets(set_sequence):
    """Returns the elements that occur only once in the sequence of sets set_sequence.
    The elements are returned as a set."""
    totalNumSet = []
    
    returnSet = set()
    dictTracker = defaultdict(int)


    if(len(set_sequence) == 0 or set_sequence == [set()]):
        return set()

    for i in set_sequence:
        for j in i:
            if j not in totalNumSet:
                totalNumSet.append(j)
    for j in range(len(totalNumSet)):
        dictTracker[totalNumSet[j]] = 0
    for i in set_sequence:
        for j in i:
            dictTracker[j] += 1 
    for k in set_sequence:
        for j in k:
            if dictTracker[j] == 1:
                returnSet.add(j)
    return returnSet





    # print(totalNumSet)
    # returnSet = set()


    # for i in totalNumSet:
    #     countr = 0

    #     for k in set_sequence:
    #         for j in k:
    #             if j == i:
    #                 countr += 1
                
    #         if countr == 1:
    #             returnSet.add(i)

    # return returnSet






    # YOUR CODE HERE

    
    ### Exercise: write where_can_it_go

def sudoku_where_can_it_go(self):
    """Sets some cell values according to the where can it go
    heuristics, by examining all rows, colums, and blocks."""
    newly_singleton = set()

    # YOUR CODE HERE
    #working with rows
    for i in range(9):
        w = [self.m[i][j] for j in range(9)]
        occurVarx = occurs_once_in_sets(w)
        for variable in occurVarx:
            for coord in range(9):
                if {variable}.issubset(self.m[i][coord]) and len(self.m[i][coord]) > 1:
                    self.m[i][coord] = {variable}
                    # newly_singleton.add(self.m[i][coord])
                    newly_singleton.add((i, coord))

    #working with columns
    for j in range(9):
        w = [self.m[i][j] for i in range(9)]
        occurVary = occurs_once_in_sets(w)
        for variable in occurVary:
            
            for coord in range(9):
                if {variable}.issubset(self.m[coord][j]) and len(self.m[coord][j]) > 1:
                    self.m[coord][j] = {variable}
                    # newly_singleton.add(self.m[coord][j])
                    newly_singleton.add((coord, j))





    #working with 3x3 cell
    for ii in range(0,9,3):
        for jj in range(0, 9, 3):
            listthreebythree = [self.m[i][j] for i in range(ii, ii+3) for j in range(jj, jj+3)]
            occurVarthree = occurs_once_in_sets(listthreebythree)
            for i in occurVarthree:
                for ic in range(ii, ii+3):
                    for jc in range(jj, jj+3):
                        if {i}.issubset(self.m[ic][jc])  and len(self.m[ic][jc]) > 1:
                            self.m[ic][jc] = {i}
                            newly_singleton.add((ic, jc))




    # Returns the list of newly-singleton cells.
    return newly_singleton

Sudoku.where_can_it_go = sudoku_where_can_it_go


### Tests for where can it go

sd = Sudoku.from_string('[[[5], [3], [1, 2, 4], [1, 2, 6], [7], [1, 2, 6, 8], [4, 8, 9], [1, 2, 4], [2, 8]], [[6], [1, 4, 7], [1, 2, 4, 7], [1, 2, 3], [9], [5], [3, 4, 8], [1, 2, 4], [2, 7, 8]], [[1, 2], [9], [8], [1, 2, 3], [4], [1, 2], [3, 5], [6], [2, 7]], [[8], [1, 5], [1, 5, 9], [1, 7, 9], [6], [1, 4, 7, 9], [4, 5], [2, 4, 5], [3]], [[4], [2], [6], [8], [5], [3], [7], [9], [1]], [[7], [1, 5], [1, 3, 5, 9], [1, 9], [2], [1, 4, 9], [4, 5, 8], [4, 5], [6]], [[1, 9], [6], [1, 5, 7, 9], [5, 7, 9], [3], [7, 9], [2], [8], [4]], [[2, 9], [7, 8], [2, 7, 9], [4], [1], [2, 7, 9], [6], [3], [5]], [[2, 3], [4, 5], [2, 3, 4, 5], [2, 5, 6], [8], [2, 6], [1], [7], [9]]]')
print("Original:")
sd.show(details=True)
new_singletons = set()
while True:
    new_s = sd.where_can_it_go()
    if len(new_s) == 0:
        break
    new_singletons |= new_s
assert_equal(new_singletons,
             {(3, 2), (2, 6), (7, 1), (5, 6), (2, 8), (8, 0), (0, 5), (1, 6),
              (2, 3), (3, 7), (0, 3), (5, 1), (0, 8), (8, 5), (5, 3), (5, 5),
              (8, 1), (5, 7), (3, 1), (0, 6), (1, 8), (3, 6), (5, 2), (1, 1)})
print("After where can it go:")
sd.show(details=True)
sdd = Sudoku.from_string('[[[5], [3], [1, 2, 4], [6], [7], [8], [9], [1, 2, 4], [2]], [[6], [7], [1, 2, 4, 7], [1, 2, 3], [9], [5], [3], [1, 2, 4], [8]], [[1, 2], [9], [8], [3], [4], [1, 2], [5], [6], [7]], [[8], [5], [9], [1, 9, 7], [6], [1, 4, 9, 7], [4], [2], [3]], [[4], [2], [6], [8], [5], [3], [7], [9], [1]], [[7], [1], [3], [9], [2], [4], [8], [5], [6]], [[1, 9], [6], [1, 5, 9, 7], [9, 5, 7], [3], [9, 7], [2], [8], [4]], [[9, 2], [8], [9, 2, 7], [4], [1], [9, 2, 7], [6], [3], [5]], [[3], [4], [2, 3, 4, 5], [2, 5, 6], [8], [6], [1], [7], [9]]]')
print("The above should be equal to:")
sdd.show(details=True)
assert_equal(sd, sdd)

sd = Sudoku([
    '___26_7_1',
    '68__7____',
    '1____45__',
    '82_1___4_',
    '__46_2___',
    '_5___3_28',
    '___3___74',
    '_4__5__36',
    '7_3_18___'
])
print("Another Original:")
sd.show(details=True)
print("Propagate once:")
sd.propagate_all_cells_once()
# sd.show(details=True)
new_singletons = set()
while True:
    new_s = sd.where_can_it_go()
    if len(new_s) == 0:
        break
    new_singletons |= new_s
print("After where can it go:")
sd.show(details=True)
sdd = Sudoku.from_string('[[[4], [3], [5], [2], [6], [9], [7], [8], [1]], [[6], [8], [2], [5], [7], [1], [4], [9], [3]], [[1], [9], [7], [8], [3], [4], [5], [6], [2]], [[8], [2], [6], [1], [9], [5], [3], [4], [7]], [[3], [7], [4], [6], [8], [2], [9], [1], [5]], [[9], [5], [1], [7], [4], [3], [6], [2], [8]], [[5], [1], [1, 2, 5, 6, 8, 9], [3], [2], [6], [1, 2, 8, 9], [7], [4]], [[2], [4], [1, 2, 8, 9], [9], [5], [7], [1, 2, 8, 9], [3], [6]], [[7], [6], [3], [4], [1], [8], [2], [5], [9]]]')
print("The above should be equal to:")
sdd.show(details=True)
assert_equal(sd, sdd)

sd = Sudoku(sd_partially_solved)
newly_singleton = sd.where_can_it_go()
print("Newly singleton:", newly_singleton)
print("Resulting Sudoku:")
sd.show(details=True)

import requests

r = requests.get("https://raw.githubusercontent.com/shadaj/sudoku/master/sudoku17.txt")
puzzles = r.text.split()

def convert_to_our_format(s):
    t = s.replace('0', '_')
    r = []
    for i in range(9):
        r.append(t[i * 9: (i + 1) * 9])
    return r
