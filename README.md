This is code designed to solve a game based on tuile that can rotate in place.

It implements a CSP to find solutions where all tuile are connected to others tuile.

When called with the `-s` it will consume a grid from stdin where all tuile are encoded in base 16 ints.
The first bit encodes the presence of a connector on the top, the second bit on the left, the third on the bottom and the fourth on the right.
All tuiles are illustrated in the tuiles folder.
