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
        self.width = width
        self.height = height
        self.tuiles = tuiles

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
