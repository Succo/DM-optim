import sys


class tuile():
    """ tuile stores information about a tuile state
    and it's possible rotation"""
    def __init__(self, val):
        self.val = int(val, 16)

    def hasConnectorUp(self):
        return (self.val & 1) != 0

    def hasConnectorLeft(self):
        return (self.val & 2) != 0

    def hasConnectorDown(self):
        return (self.val & 4) != 0

    def hasConnectorRight(self):
        return (self.val & 8) != 0


class grille():
    """ grille is the main class, has the array of tuile """
    def __init__(self, width, height, tuiles):
        self.width = width
        self.height = height
        self.tuiles = tuiles

    def get(self, x, y):
        return self.tuiles[y*self.width+x]


def main():
    args = sys.argv
    print(args)
    if len(args) != 2 or args[1] != "-s":
        print("Run the program with -s and input from stdin")
        return
    height = 0
    width = 0
    tuiles = []
    for line in sys.stdin:
        if height == 0:
            width = len(line)-1  # -1 for the \n
        height += 1
        for i in range(width):
            tuiles += [tuile(line[i])]
    g = grille(width, height, tuiles)
    print(g.get(0, 1))

if __name__ == "__main__":
    main()
