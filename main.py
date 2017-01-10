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
    if len(args) < 2 or args[1] not in ["-s", "-g"] or "-h" in args:
        print("Run the program with -s to read from stdin or -g and size")
        print("Use -a to maintain arc consistency in the solver")
        print("Use -p to output all solutions to the grid")
        print("Use -i to save pictures of the grid in 'out'")
        print("Default it only shows one solutions and whether it's unique")
        print("-h for this message and exit")
        return
    if args[1] == "-s":
        g = grid_from_stdin()
    else:
        g = generate_grid(args[2:])
    g.constrain_border()
    if "-a" in args:
        g.maintain_arc_consistency()
    sols = [sol for sol in g.solve()]
    if "-p" in args or "-i" in args:
        # treating all solutions
        for i, sol in enumerate(sols):
            if "-p" in args:
                g.print_sol(sol)
            if "-i" in args:
                g.picture_from_sol(sol, "grid_{}".format(i))
    else:
        if len(sols) == 0:
            print("# pas de solutions")
        elif len(sols) == 1:
            g.print_sol(sols[0])
            print("# la solution est unique")
        else:
            g.print_sol(sols[0])
            print("# la solution n'est pas unique")

if __name__ == "__main__":
    main()
