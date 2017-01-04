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
    def __init__(self, val):
        val = int(val, 16)
        self.possible = getPossible(val)
        self.assigned = None

    def connectUp(self, conn):
        """ connectUp imposes or not a path Up based on conn value """
        self.possible = [val for val in self.possible if (val & 1) == conn]
        return len(self.possible) != 0

    def connectLeft(self, conn):
        """ connectLeft imposes or not a path Left based on conn value """
        self.possible = [val for val in self.possible if (val & 2) >> 1 == conn]
        return len(self.possible) != 0

    def connectDown(self, conn):
        """ connectDown imposes or not a path Down based on conn value """
        self.possible = [val for val in self.possible if (val & 4) >> 2 == conn]
        return len(self.possible) != 0

    def connectRight(self, conn):
        """ connectRight imposes or not a path Right based on conn value """
        self.possible = [val for val in self.possible if (val & 8) >> 3 == conn]
        return len(self.possible) != 0


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

    def get(self, x, y):
        return self.tuiles[y*self.width+x]

    def constrainBorder(self):
        """ constrainBorder imposes no connection outside on all borders """
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

    def prettyPrint(self):
        for i, t in enumerate(self.tuiles):
            print(t.possible)

    def solve(self):
        """ iterator on all solutions """
        self.nodes += 1
        t = self.selectVar()
        if t is None:
            yield [t.assigned for t in self.tuiles]
        else:
            for orient in t.possible:
                t.assigned = orient
                history = self.save_context()
                self.restore_context(history)

    # context management
    def save_context(self):
        return len(self.context)

    def restore_context(self, history):
        """ restore tuile to their previous values """
        while len(self.context) > history:
            i, tuile = self.context.pop()
            self.tuiles[i] = tuile

    def update_tuile(self, i, tuile):
        """ update a tuile storing it's previous value in context """
        self.context.append(i, self.tuiles[i])
        self.tuiles[i] = tuile

    # exploration
    def selectVar(self):
        """ returns the next tuile on which to iterate
        heuristic: the one with the smallest domain """
        choice = None
        for t in self.tuiles:
            if t.assigned is None and  \
                (choice is None or
                    len(t.possible) < len(choice.possible)):
                choice = t
        return choice
