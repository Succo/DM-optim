class Tuile():
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


class Grille():
    """ grille is the main class, has the array of tuile """
    def __init__(self, width, height, tuiles):
        self.width = width
        self.height = height
        self.tuiles = tuiles

    def get(self, x, y):
        return self.tuiles[y*self.width+x]
