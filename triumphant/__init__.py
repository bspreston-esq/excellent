#!/usr/bin/env python3
"""triumphant - a totally excellent quote machine, dude!

Serves up righteous quotes from Bill and Ted's Excellent Adventure and
other collections (yeah, baby!). Party on!
"""

import argparse
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_COLLECTION = "default"

_SEPARATOR = re.compile(r"^-{2,}$")


def _collection_roots():
    """Candidate roots containing collection directories, in precedence order."""
    return [Path("/var/lib/triumphant"), Path(__file__).resolve().parent / "collections"]


def parse_quotes(text):
    """Parse quote file text into a list of quotes.

    Quotes are separated by a line of two or more hyphens. Blank lines and
    lines starting with ``#`` are ignored. Quotes may span multiple lines;
    surrounding whitespace is trimmed.
    """
    quotes = []
    current = []
    for line in text.splitlines():
        stripped = line.strip()
        if _SEPARATOR.match(stripped):
            quote = "\n".join(current).strip()
            if quote:
                quotes.append(quote)
            current = []
        elif not stripped or stripped.startswith("#"):
            continue
        else:
            current.append(stripped)
    quote = "\n".join(current).strip()
    if quote:
        quotes.append(quote)
    return quotes


@dataclass(frozen=True)
class Collection:
    name: str
    description: str
    standard: tuple
    careful: tuple
    bogus: tuple


def find_collection_dir(name, roots=None):
    """Return the directory of collection ``name`` or None."""
    roots = _collection_roots() if roots is None else [Path(root) for root in roots]
    for root in roots:
        candidate = root / name
        if candidate.is_dir():
            return candidate
    return None


def _read_quotes(path):
    return tuple(parse_quotes(path.read_text(encoding="utf-8")))


def _description(collection_dir, name):
    desc_file = collection_dir / "description"
    if desc_file.is_file():
        desc = desc_file.read_text(encoding="utf-8").strip()
        if desc:
            return desc
    return name


def list_collections(roots=None):
    """Return ``[(name, description)]``; ``default`` is listed first."""
    found = {}
    roots = _collection_roots() if roots is None else [Path(root) for root in roots]
    for root in roots:
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if entry.is_dir() and (entry / "standard").is_file():
                found.setdefault(entry.name, _description(entry, entry.name))
    names = sorted(found)
    if DEFAULT_COLLECTION in names:
        names.remove(DEFAULT_COLLECTION)
        names.insert(0, DEFAULT_COLLECTION)
    return [(name, found[name]) for name in names]


def load_collection(name, roots=None):
    """Load a collection; raises LookupError/FileNotFoundError/ValueError."""
    collection_dir = find_collection_dir(name, roots=roots)
    if collection_dir is None:
        available = ", ".join(n for n, _ in list_collections(roots=roots))
        raise LookupError(f"unknown collection {name!r}; available: {available}")
    standard = _read_quotes(collection_dir / "standard")
    careful = _read_quotes(collection_dir / "careful")
    bogus = _read_quotes(collection_dir / "bogus")
    if not standard or not careful or not bogus:
        raise ValueError(
            f"collection {name!r} must have non-empty standard, careful and bogus quote files"
        )
    return Collection(
        name=name,
        description=_description(collection_dir, name),
        standard=standard,
        careful=careful,
        bogus=bogus,
    )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="triumphant",
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
    parser.add_argument(
        "-L",
        "--list-collections",
        action="store_true",
        help="list the available quote collections and exit",
    )
    parser.add_argument(
        "-C",
        "--collection",
        default=DEFAULT_COLLECTION,
        metavar="NAME",
        help=f"collection to draw quotes from (default: {DEFAULT_COLLECTION})",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_collections:
        for name, description in list_collections():
            print(f"{name} ({description})")
        return 0

    try:
        collection = load_collection(args.collection)
    except (LookupError, FileNotFoundError, ValueError) as exc:
        print(f"triumphant: error: {exc}", file=sys.stderr)
        return 2

    if args.careful:
        quotes = collection.careful
    elif args.bogus:
        quotes = collection.bogus
    else:
        quotes = collection.standard

    print(random.choice(quotes))
    return 0


# The default collection's quote sets, for convenience.
_DEFAULT = load_collection(DEFAULT_COLLECTION)
REGULAR_QUOTES = _DEFAULT.standard
CAREFUL_QUOTES = _DEFAULT.careful
BOGUS_QUOTES = _DEFAULT.bogus
