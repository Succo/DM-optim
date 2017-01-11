import random
import sys


class Grille_Generator():
    """  Grille_Generator generates valid grid by iterating in values"""
    def __init__(self, width, height):
        # Dimension of the grid
        self.width = width
        self.height = height
        # /!\ in generator tuiles only stores int as there is no need
        # for Tuile class
        self.tuiles = []

    # utils
    def get(self, x, y):
        return self.tuiles[y*self.width+x]

    def print_sol(self, sol, f=sys.stdout):
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += format(sol[i*self.width+j], 'x')
            print(line, file=f)

    # generator core function
    def generate(self):
        """ Iterate on tuiles """
        for j in range(self.height):
            for i in range(self.width):
                possible = [t for t in range(16)]
                if i == 0:
                    conn_left = 0
                else:
                    conn_left = ((self.get(i-1, j) >> 3) & 1)
                possible = [t for t in possible if (t >> 1) & 1 == conn_left]
                if j == 0:
                    conn_up = 0
                else:
                    conn_up = ((self.get(i, j-1) >> 2) & 1)
                possible = [t for t in possible if t & 1 == conn_up]
                if i == self.width-1:
                    possible = [t for t in possible if (t >> 3) & 1 == 0]
                if j == self.height-1:
                    possible = [t for t in possible if (t >> 2) & 1 == 0]
                self.tuiles += [random.choice(possible)]
