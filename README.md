This is code designed to solve a game based on tuile that can rotate in place.

It implements a CSP to find solutions where all tuile are connected to others tuile.

Tuiles are encoded using integer between 0 and 16 reprensented in base 16.
The first bit encodes the presence of a connector on the top, the second bit on the left, the third on the bottom and the fourth on the right.
All tuiles are illustrated in the tuiles folder.

Options are for the grid:
* `-s` to read the grid from stdin
* `-g <h> <l>` for a randomly generated grid (`l` is optionnal, grid will be square by default)
