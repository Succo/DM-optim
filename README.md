This is code designed to solve a game based on tuile that can rotate in place.

It implements a CSP to find solutions where all tuile are connected to others tuile.

Tuiles are encoded using integer between 0 and 16 reprensented in base 16.
The first bit encodes the presence of a connector on the top, the second bit on the left, the third on the bottom and the fourth on the right.
All tuiles are illustrated in the tuiles folder.

```
Usage: ./main.py <main arg> <options>
main args:
  -s          read a grid from stdin
  -g <H> <W>  generate a grid of size HxW (W optionnal)
  -r <n>      populates 'input' with valid grid of 1x1 to nxn
  -h          print this message and exit
options:
  -a          maintain arc consistency in the solver
  -p          output all solutions to the grid
  -i          save pictures of all solutions in 'out'
  -f          with '-g' to force grid to have a solution
```
