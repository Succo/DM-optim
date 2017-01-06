import copy


def rotate(val):
    """ rotate shift all bits by one, move the last bit first """
    return ((val << 1) & (~17)) | (val >> 3)


def getPossible(val):
    """ getPossible generates all rotations possible for a value """
    possible = [val]
    tmp = val
    while rotate(tmp) != val:
        tmp = rotate(tmp)
        possible += [tmp]
    return possible


class Tuile():
    """ tuile stores information about a tuile state
    and it's possible rotation"""
    def __init__(self, val, x, y):
        val = int(val, 16)
        self.possible = getPossible(val)
        self.assigned = None
        # positions
        self.x = x
        self.y = y

    def connectUp(self, conn):
        """ connectUp imposes or not a path Up based on conn value """
        self.possible = [val for val in self.possible if (val & 1) == conn]
        return len(self.possible) != 0

    def getUp(self):
        """ getUp returns 1 if the tuile is connected Up, 0 otherwise """
        return (self.assigned & 1)

    def connectLeft(self, conn):
        """ connectLeft imposes or not a path Left based on conn value """
        self.possible = [val for val in self.possible if (val & 2) >> 1 == conn]
        return len(self.possible) != 0

    def getLeft(self):
        """ getLeft returns 1 if the tuile is connected Left, 0 otherwise """
        return (self.assigned & 2) >> 1

    def connectDown(self, conn):
        """ connectDown imposes or not a path Down based on conn value """
        self.possible = [val for val in self.possible if (val & 4) >> 2 == conn]
        return len(self.possible) != 0

    def getDown(self):
        """ getDown returns 1 if the tuile is connected Down, 0 otherwise """
        return (self.assigned & 4) >> 2

    def connectRight(self, conn):
        """ connectRight imposes or not a path Right based on conn value """
        self.possible = [val for val in self.possible if (val & 8) >> 3 == conn]
        return len(self.possible) != 0

    def getRight(self):
        """ getRight returns 1 if the tuile is connected Right, 0 otherwise """
        return (self.assigned & 8) >> 3


class Grille():
    """ grille is the main class, has the array of tuile """
    def __init__(self, width, height, tuiles):
        # Dimension of the grid
        self.width = width
        self.height = height
        self.tuiles = tuiles
        # Number of nodes in the tree
        self.nodes = 0
        # Context, i.e. list of effectued modification
        self.context = []

    # utils
    def get(self, x, y):
        return self.tuiles[y*self.width+x]

    def prettyPrint(self):
        for i, t in enumerate(self.tuiles):
            print(t.possible)

    # Solver core function
    def constrain_border(self):
        """ constrain_border imposes no connection outside on all borders """
        for i in range(self.width):
            if not self.get(i, 0).connectUp(0):
                return False
            if not self.get(i, self.height-1).connectDown(0):
                return False
        for j in range(self.height):
            if not self.get(0, j).connectLeft(0):
                return False
            if not self.get(self.width-1, j).connectRight(0):
                return False
        return True

    def solve(self):
        """ iterator on all solutions """
        self.nodes += 1
        t = self.select_tuile()
        if t is None:
            yield [t.assigned for t in self.tuiles]
        else:
            for orient in t.possible:
                t.assigned = orient
                history = self.save_context()
                if not self.forward_check(t):
                    yield None
                else:
                    for sol in self.solve():
                        yield sol
                self.restore_context(history)
                t.assigned = None

    # context management
    def save_context(self):
        return len(self.context)

    def restore_context(self, history):
        """ restore tuile to their previous values """
        while len(self.context) > history:
            tuile = self.context.pop()
            index = tuile.y * self.width + tuile.x
            self.tuiles[index] = tuile

    def update_tuile(self, tuile):
        """ update a tuile storing it's previous value in context """
        index = tuile.y * self.width + tuile.x
        self.context.append(self.tuiles[index])
        self.tuiles[index] = tuile

    # exploration
    def select_tuile(self):
        """ returns the next tuile on which to iterate
        heuristic: the one with the smallest domain """
        choice = None
        for t in self.tuiles:
            if t.assigned is None and  \
                (choice is None or
                    len(t.possible) < len(choice.possible)):
                choice = t
        return choice

    def forward_check(self, t):
        # Constrain the tuile above
        if t.y > 0 and self.get(t.x, t.y-1).assigned is None:
            above = copy.deepcopy(self.get(t.x, t.y-1))
            if not above.connectDown(t.getUp()):
                return False
            if len(above.possible) != len(self.get(t.x, t.y-1).possible):
                self.update_tuile(above)
        # Constrain the tuile below
        if t.y < self.height-1 and self.get(t.x, t.y+1).assigned is None:
            below = copy.deepcopy(self.get(t.x, t.y+1))
            if not below.connectUp(t.getDown()):
                return False
            if len(below.possible) != len(self.get(t.x, t.y+1).possible):
                self.update_tuile(below)
        # Constrain the tuile left
        if t.x > 0 and self.get(t.x-1, t.y).assigned is None:
            left = copy.deepcopy(self.get(t.x-1, t.y))
            if not left.connectRight(t.getLeft()):
                return False
            if len(left.possible) != len(self.get().possible):
                self.update_tuile(left)
        # Constrain the tuile right
        if t.x < self.width-1 and self.get(t.x+1, t.y).assigned is None:
            right = copy.deepcopy(self.get(t.x+1, t.y))
            if not right.connectLeft(t.getRight()):
                return False
            if len(right.possible) != len(self.get(t.x+1, t.y).possible):
                self.update_tuile(right)
        return True
