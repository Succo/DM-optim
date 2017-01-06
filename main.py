#!/usr/bin/python3

import sys
from tuile import Grille, Tuile


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
        for i in range(width):
            tuiles += [Tuile(line[i], i, height)]
        height += 1
    g = Grille(width, height, tuiles)
    g.constrain_border()
    for sol in g.solve():
        print(sol)

if __name__ == "__main__":
    main()
