import copy

import cv2
import numpy as np


def rotate(val):
    """ rotate shift all bits by one, move the last bit first """
    return ((val << 1) & (~17)) | (val >> 3)


def get_possible(val):
    """get_possible generates all rotations possible for a value """
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
        self.possible = get_possible(val)
        self.assigned = None
        # positions
        self.x = x
        self.y = y

    def connect(self, orientation, conn):
        """ connect imposes a connection along an orientation (0, 1, 2, 3) """
        self.possible = [val for val in self.possible if
                         (val >> orientation) & 1 == conn]
        return len(self.possible) != 0

    def get(self, orientation):
        return (self.assigned >> orientation) & 1


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

    def pretty_print(self):
        for i, t in enumerate(self.tuiles):
            print(t.possible)
            print(t.assigned)
        print()

    def print_sol(self, sol):
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += format(sol[i*self.width+j], 'x')
            print(line)

    def picture_from_sol(self, sol):
        tiles = [cv2.imread("tuile/{}.png".format(format(i, 'x')), -1)
                 for i in range(16)]
        lines = []
        for i in range(self.height):
            lines += [np.concatenate([tiles[sol[i*self.width + j]] for
                                      j in range(self.width)], axis=1)]
        vis = np.concatenate(lines, axis=0)
        cv2.imwrite("out/graph.png", vis)

    # Solver core function
    def constrain_border(self):
        """ constrain_border imposes no connection outside on all borders """
        for i in range(self.width):
            if not self.get(i, 0).connect(0, 0):
                return False
            if not self.get(i, self.height-1).connect(2, 0):
                return False
        for j in range(self.height):
            if not self.get(0, j).connect(1, 0):
                return False
            if not self.get(self.width-1, j).connect(3, 0):
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
                # self.pretty_print()
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
        for idx, (x, y) in enumerate([(0, -1), (-1, 0), (0, 1), (1, 0)]):
            new_x = t.x + x
            new_y = t.y + y
            if new_x < 0 or new_x > self.width-1 or\
               new_y < 0 or new_y > self.height-1:
                continue
            new_tuile = copy.deepcopy(self.get(new_x, new_y))
            if new_tuile.assigned is not None:
                continue
            new_tuile.connect((idx+2) % 4, t.get(idx))
            if len(new_tuile.possible) != len(self.get(new_x, new_y).possible):
                self.update_tuile(new_tuile)
        return True
