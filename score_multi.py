#!/usr/bin/env python
"""Computes bits per character entropy for strings."""

import argparse
from ast import arg
import math
from pyexpat import model
import multiprocessing as mp
import pynini
import re

M_LN2 = math.log(2)


class Error(Exception):
    pass


def _bits_per_char(string: pynini.Fst, lm: pynini.Fst) -> float:
    """Computes bits per char according to LM FST.

    Args:
      string: an FSA to be scored.
      lm: a WFSA language model.

    Returns:
      The score as bits per char.

    Raises:
      Error: Composition failure.
    """
    # Checks properties ahead of time, just to be sure.
    eprops = pynini.ACCEPTOR | pynini.STRING | pynini.UNWEIGHTED
    oprops = string.properties(eprops, True)
    assert eprops == oprops, f"{oprops} != {eprops}"
    # Scores the lattice.
    lattice = pynini.intersect(string, lm)
    # Detects composition failure.
    if lattice.start() == pynini.NO_STATE_ID:
        raise Error("Composition failure")
    # The shortest backwards distance from the start state to a final state
    # is the cost of a string w.r.t. the LM.
    cost = pynini.shortestdistance(lattice, reverse=True)[lattice.start()]
    # Converts this to base-2.
    bits = float(cost) / M_LN2
    # A n-char string FSA has n + 1 states. Draw it if you don't believe me.
    chars = string.num_states() - 1
    return bits / chars


def main(args: argparse.Namespace) -> None:
    # read model
    lm = pynini.Fst.read(args.lm)

    # open the input text.txt file
    with open(args.corpus, "r") as file:
      # set the output tsv file
      output = open('output.tsv', 'w')
      # iterate over each line of the file
      for text in file:
        # compile each string into an fst format, escaping especial characters
        line = pynini.accep(pynini.escape(text.rstrip()))

        try:
          # apply _bits_per_char to each fst line
          score =_bits_per_char(line, lm)
          # write the file
          output.write(f'{str(score)}"\t"{text}')
          # print(score, text)
        except Error:
          pass
      

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # TODO: Add arguments here, then delete this line and the ellipses.
    parser.add_argument("--corpus", help="path to corpus file")
    parser.add_argument("--lm", help="path to model fst file")
    process = mp.Process(target=main, args=(parser.parse_args(),))
    process.start()
    process.join()
