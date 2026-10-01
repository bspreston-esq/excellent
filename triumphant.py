#!/usr/bin/env python3
"""triumphant.py — a totally excellent quote machine, dude!

Serves up righteous quotes from Bill and Ted's Excellent Adventure.
Party on!
"""

import argparse
import random

REGULAR_QUOTES = [
    "Be excellent to each other.",
    "Party on, dudes!",
    "69, dudes!",
    "Iron Maiden? Excellent!",
    "Most triumphant!",
    "Bodacious!",
    "Most outstanding!",
    "Excellent!",
]

CAREFUL_QUOTES = [
    "Strange things are afoot at the Circle-K.",
    "All we are is dust in the wind, dude.",
    "So-crates. 'The only true wisdom consists in knowing that you know nothing.'",
]

BOGUS_QUOTES = [
    "Most non-triumphant",
    "Heinous",
    "Bogus",
    "Things are most heinously failing",
]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="triumphant.py",
        description="Prints a most excellent quote. Be excellent to each other!",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--careful",
        action="store_true",
        help="print a quote from the careful set (strange things are afoot)",
    )
    mode.add_argument(
        "--bogus",
        action="store_true",
        help="print a quote from the bogus set (things are most heinously failing)",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.careful:
        quotes = CAREFUL_QUOTES
    elif args.bogus:
        quotes = BOGUS_QUOTES
    else:
        quotes = REGULAR_QUOTES

    print(random.choice(quotes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
