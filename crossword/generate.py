import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # loop through items 
        for var, words in self.domains.items():
            # for each word in possible words, check the length
            # if length does not match the variable length, remove it
            for w in list(words):
                if var.length != len(w):
                    self.domains[var].remove(w)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        # check for overlaps
        if self.crossword.overlaps[x,y] is None:
            return revision
            
        else:
            i, j = self.crossword.overlaps[x,y]

            # loop through each word in x
            for word_x in list(self.domains[x]):
                # if there are no matches with any word_y, remove word_x
                if all(word_x[i] != word_y[j] for word_y in self.domains[y]):
                    self.domains[x].remove(word_x)
                    revision = True
            return revision
                        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # create list of arcs if it's not provided
        if arcs is None:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((y,x))
        else: 
            queue = arcs
        
        # loop until queue is empty
        while len(queue) > 0:
            x,y = queue.pop(0)
            print(x,y)
            if self.revise(x,y):
                # if domain is empty, the problem cannot be solved
                if len(self.domains[x]) == 0:
                    return False
                # add neighbouring arcs to queue because change in domain of x could result in neighbouring arcs no longer being arc consistent with x
                for z in self.crossword.neighbors(x) - {y}:
                    if z != y:
                        queue.append((z,x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # create a list to check which words have been used
        words_used = []
        for var, word in assignment.items():
            # check that word is of correct length
            if var.length != len(word):
                return False
            # check that word is distinct
            if word in words_used:
                return False
            words_used.append(word)

        # check that overlapped characters match (i.e. arc consistent)
        for var_x, word_x in assignment.items():
            for var_y, word_y in assignment.items():
                # if overlap exist and var_x is not var_y
                if var_x != var_y and self.crossword.overlaps[var_x,var_y] is not None:
                    i,j = self.crossword.overlaps[var_x,var_y] 
                    if word_x[i] != word_y[j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # set of unassigned variables
        # unassigned_vars = self.crossword.variables - set(assignment.keys())

        # set of neighboring vars (w/o assigned vars)
        neighboring_vars = self.crossword.neighbors(var) - set(assignment.keys())

        # dict for keep track of how many values are ruled out
        choices_eliminated = {v: 0 for v in self.domains[var]}

        # loop through values in the var
        for word_x in self.domains[var]:
            # loop through vars in neighboring vars
            for var_y in neighboring_vars:
                # find overlaps
                i,j = self.crossword.overlaps[var,var_y] 
                # loop through words in neighboring var
                for word_y in self.domains[var_y]:
                    # if word is idenfical or overlap char does not match, it is ruled out
                    if word_x == word_y or word_x[i] != word_y[j]:
                        choices_eliminated[word_x] += 1

        # sort dictionary items based on values and store in list
        result = [key for key, val in sorted(choices_eliminated.items(), key = lambda x: x[1])]

        return result


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # set of unassigned variables
        unassigned_vars = self.crossword.variables - set(assignment.keys())

        # dictionary with values = len of domain
        unassigned_vars_dict = {v: len(self.domains[v]) for v in unassigned_vars}

        # find min domain size from the dictionary 
        min_value = min(unassigned_vars_dict.values())

        # find vars with the min domain size
        vars_min_value = [v for v in unassigned_vars_dict if unassigned_vars_dict[v] == min_value]

        if len(vars_min_value) == 1:
            return vars_min_value[0]
        else:
            # dictionary with vars w min domain size
            vars_min_value_dict = {k: len(self.crossword.neighbors(k)) for k in vars_min_value}

            # find min degrees from the dictionary 
            min_degrees = min(vars_min_value_dict.values())

            # find vars with min degrees
            vars_min_degrees = [v for v in vars_min_value_dict if vars_min_value_dict[v] == min_degrees]

            # just return the first in list since ties are acceptable
            return vars_min_degrees[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        while not assignment_complete:
            var = self.select_unassigned_variable(assignment)
            self.order_domain_values(var)



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
