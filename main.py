#!/usr/bin/python3

import random
import sys
from tuile import Grille, Tuile, get_possible
from generate import Grille_Generator


def grid_from_stdin(args):
    """ Read a grid from stdin and treats its solutions """
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
    if "-a" in args:
        g.maintain_arc_consistency()
    g.constrain_border()
    sols = [sol for sol in g.solve()]
    process_sols(g, sols, args)


def random_grid(height, width):
    """ generates a grid of random tuiles """
    values = [format(i, 'x') for i in [0, 1, 3, 5, 7, 15]]
    side_values = [format(i, 'x') for i in [0, 1, 3, 5, 7]]
    corner_values = [format(i, 'x') for i in [0, 1, 3, 5]]
    tuiles = []
    for i in range(height):
        for j in range(width):
            if (i == 0 or i == height-1) and\
               (j == 0 or j == width-1):
                val = random.choice(corner_values)
            elif (i == 0 or i == height-1) or\
                 (j == 0 or j == width-1):
                val = random.choice(side_values)
            else:
                val = random.choice(values)
            tuiles += [Tuile(val, j, i)]
    return Grille(width, height, tuiles)


def generate_grid(args):
    """ Generates a random grid and treats it according to args
        Can be forced to find a grid with at least a solution """
    height = int(args[0])
    if len(args) > 1 and args[1].isdigit():
        width = int(args[1])
    else:
        width = height
    g = random_grid(height, width)
    g.constrain_border()
    if "-a" in args:
        g.maintain_arc_consistency()
    sols = [sol for sol in g.solve()]
    while "-f" in args and len(sols) == 0:
            g = random_grid(height, width)
            g.constrain_border()
            if "-a" in args:
                g.maintain_arc_consistency()
            sols = [sol for sol in g.solve()]
    process_sols(g, sols, args)


def random_sample(max_size):
    """ Generates random solvable grids and store them in their default state
        Useful to have grids for prototyping """
    max_size = int(max_size)
    for i in range(1, max_size):
        print(i)
        g = Grille_Generator(i, i)
        g.generate()
        with open("input/{}x{}".format(i, i), 'w') as f:
            inputs = [min(get_possible(val)) for val in g.tuiles]
            g.print_sol(inputs, f=f)


def process_sols(g, sols, args):
    """ Prints and output information related to a solution
        depanding on arguments """
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


def main():
    """ Main just get args and either use predefined grid
        or randomly generated grid """
    args = sys.argv
    if len(args) < 2 or args[1] not in ["-s", "-g", "-r"] or "-h" in args:
        print("Usage: ./main.py <main arg> <options>")
        print("main args:")
        print("  -s          read a grid from stdin")
        print("  -g <H> <W>  generate a grid of size HxW (W optionnal)")
        print("  -r <n>      populates 'input' with valid grid of 1x1 to nxn")
        print("  -h          print this message and exit")
        print("options:")
        print("  -a          maintain arc consistency in the solver")
        print("  -p          output all solutions to the grid")
        print("  -i          save pictures of all solutions in 'out'")
        print("  -f          with '-g' to force grid to have a solution")
        return
    if args[1] == "-s":
        grid_from_stdin(args[2:])
    elif args[1] == "-g":
        generate_grid(args[2:])
    else:
        random_sample(args[2])

if __name__ == "__main__":
    main()
