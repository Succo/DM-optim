#!/usr/bin/python3

import random
import sys
from tuile import Grille, Tuile


def grid_from_stdin():
    height = 0
    width = 0
    tuiles = []
    for line in sys.stdin:
        if height == 0:
            width = len(line)-1  # -1 for the \n
        for i in range(width):
            tuiles += [Tuile(line[i], i, height)]
        height += 1
    return Grille(width, height, tuiles)


def generate_grid(args):
    """ generates a grid of random tuiles """
    values = [format(i, 'x') for i in range(16)]
    side_values = [format(i, 'x') for i in range(15)]
    corner_values = [format(i, 'x') for i in range(12)]
    height = int(args[0])
    if len(args) > 1 and args[1].isdigit():
        width = int(args[1])
    else:
        width = height
    tuiles = []
    for i in range(height):
        for j in range(width):
            if (i == 0 or i == height-1) and\
               (j == 0 or j == width-1):
                tuiles += [Tuile(random.choice(corner_values), j, i)]
            elif (i == 0 or i == height-1) or\
                 (j == 0 or j == width-1):
                tuiles += [Tuile(random.choice(side_values), j, i)]
            else:
                tuiles += [Tuile(random.choice(values), j, i)]
    return Grille(width, height, tuiles)


def main():
    args = sys.argv
    if len(args) < 2 or args[1] not in ["-s", "-g", "-h"]:
        print("Run the program with -s to read from stdin or -g and size")
        return
    if args[1] == "-s":
        g = grid_from_stdin()
    else:
        g = generate_grid(args[2:])
    g.constrain_border()
    g.maintain_arc_consistency()
    for sol in g.solve():
        g.print_sol(sol)
        g.picture_from_sol(sol)

if __name__ == "__main__":
    main()
