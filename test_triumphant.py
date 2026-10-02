"""Tests for triumphant - most triumphant, dude!"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import triumphant
from triumphant import parse_quotes


def run_triumphant(*args):
    return subprocess.run(
        [sys.executable, "-m", "triumphant", *args],
        capture_output=True,
        text=True,
        cwd=".",
    )


class ParserTest(unittest.TestCase):
    def test_single_line_quotes(self):
        self.assertEqual(parse_quotes("One\n--\nTwo\n"), ["One", "Two"])

    def test_multi_line_quotes(self):
        text = "Line one\nline two\n--\nAfter\n"
        self.assertEqual(parse_quotes(text), ["Line one\nline two", "After"])

    def test_comments_and_blank_lines_ignored(self):
        text = "# header\n\nOne\n\n--\n# between\nTwo\n"
        self.assertEqual(parse_quotes(text), ["One", "Two"])

    def test_separator_variants(self):
        text = "One\n---\nTwo\n-----\nThree\n"
        self.assertEqual(parse_quotes(text), ["One", "Two", "Three"])

    def test_single_hyphen_is_not_separator(self):
        self.assertEqual(parse_quotes("One\n-\nTwo\n"), ["One\n-\nTwo"])

    def test_whitespace_trimmed(self):
        self.assertEqual(parse_quotes("  One  \n--\n Two\n"), ["One", "Two"])

    def test_leading_trailing_separators_ignored(self):
        self.assertEqual(parse_quotes("--\nOne\n--\n--\n"), ["One"])


class DefaultCollectionTest(unittest.TestCase):
    def test_default_lists_nonempty(self):
        self.assertTrue(triumphant.REGULAR_QUOTES)
        self.assertTrue(triumphant.CAREFUL_QUOTES)
        self.assertTrue(triumphant.BOGUS_QUOTES)

    def test_original_quotes_preserved(self):
        self.assertIn("Be excellent to each other.", triumphant.REGULAR_QUOTES)
        self.assertIn("69, dudes!", triumphant.REGULAR_QUOTES)
        self.assertIn("So-crates. 'The only true wisdom consists in knowing that you know nothing.'", triumphant.CAREFUL_QUOTES)
        self.assertIn("Most non-triumphant", triumphant.BOGUS_QUOTES)

    def test_new_quotes_added(self):
        self.assertIn("Station!", triumphant.REGULAR_QUOTES)
        self.assertIn("Wyld Stallyns!", triumphant.REGULAR_QUOTES)
        self.assertIn("Dude, late!", triumphant.CAREFUL_QUOTES)
        self.assertIn("So bogus!", triumphant.BOGUS_QUOTES)

    def test_no_duplicates(self):
        for quotes in (triumphant.REGULAR_QUOTES, triumphant.CAREFUL_QUOTES, triumphant.BOGUS_QUOTES):
            self.assertEqual(len(quotes), len(set(quotes)))


class CollectionsTest(unittest.TestCase):
    def test_load_default(self):
        collection = triumphant.load_collection("default")
        self.assertEqual(collection.description, "Bill and Ted's Excellent Adventure")

    def test_load_austin_powers(self):
        collection = triumphant.load_collection("austin-powers")
        self.assertIn("Yeah, baby!", collection.standard)
        self.assertIn("Danger, danger, danger!", collection.careful)
        self.assertIn("Oh no, baby, no!", collection.bogus)

    def test_unknown_collection_raises(self):
        with self.assertRaises(LookupError):
            triumphant.load_collection("no-such-collection")

    def test_list_collections(self):
        collections = triumphant.list_collections()
        names = [name for name, _ in collections]
        self.assertEqual(names[0], "default")
        self.assertIn("austin-powers", names)
        descriptions = dict(collections)
        self.assertEqual(descriptions["default"], "Bill and Ted's Excellent Adventure")
        self.assertIn("austin-powers", descriptions)

    def test_precedence_system_root_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = Path(tmp) / "system"
            packaged = Path(tmp) / "packaged"
            (system / "custom").mkdir(parents=True)
            (packaged / "custom").mkdir(parents=True)
            (system / "custom" / "standard").write_text("System standard\n")
            (system / "custom" / "careful").write_text("System careful\n")
            (system / "custom" / "bogus").write_text("System bogus\n")
            (packaged / "custom" / "standard").write_text("Packaged standard\n")
            (packaged / "custom" / "careful").write_text("Packaged careful\n")
            (packaged / "custom" / "bogus").write_text("Packaged bogus\n")
            roots = [system, packaged]
            collection = triumphant.load_collection("custom", roots=roots)
            self.assertEqual(collection.standard, ("System standard",))

    def test_description_falls_back_to_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            (root / "mystery").mkdir(parents=True)
            for name in ("standard", "careful", "bogus"):
                (root / "mystery" / name).write_text("Q\n")
            collection = triumphant.load_collection("mystery", roots=[root])
            self.assertEqual(collection.description, "mystery")

    def test_missing_quote_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            (root / "partial").mkdir(parents=True)
            (root / "partial" / "standard").write_text("Q\n")
            with self.assertRaises(FileNotFoundError):
                triumphant.load_collection("partial", roots=[root])

    def test_empty_quote_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            (root / "empty").mkdir(parents=True)
            for name in ("standard", "careful", "bogus"):
                (root / "empty" / name).write_text("# nothing here\n")
            with self.assertRaises(ValueError):
                triumphant.load_collection("empty", roots=[root])


class CliTest(unittest.TestCase):
    def test_regular_quote_from_regular_set(self):
        proc = run_triumphant()
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), triumphant.REGULAR_QUOTES)

    def test_careful_quote_from_careful_set(self):
        proc = run_triumphant("--careful")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), triumphant.CAREFUL_QUOTES)

    def test_bogus_quote_from_bogus_set(self):
        proc = run_triumphant("--bogus")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), triumphant.BOGUS_QUOTES)

    def test_help_exits_zero_and_shows_usage(self):
        proc = run_triumphant("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stdout)
        self.assertIn("--careful", proc.stdout)
        self.assertIn("--bogus", proc.stdout)

    def test_invalid_argument_exits_nonzero_with_usage(self):
        proc = run_triumphant("--totally-bogus-flag")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stderr)

    def test_conflicting_modes_rejected(self):
        proc = run_triumphant("--careful", "--bogus")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stderr)

    def test_list_collections_flag(self):
        proc = run_triumphant("-L")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("default (Bill and Ted's Excellent Adventure)", proc.stdout)
        self.assertIn("austin-powers (", proc.stdout)

    def test_list_collections_long_flag(self):
        proc = run_triumphant("--list-collections")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("default", proc.stdout)

    def test_collection_selection(self):
        collection = triumphant.load_collection("austin-powers")
        for flag in ("-C", "--collection"):
            proc = run_triumphant(flag, "austin-powers", "--bogus")
            self.assertEqual(proc.returncode, 0)
            self.assertIn(proc.stdout.strip(), collection.bogus)

    def test_unknown_collection_errors(self):
        proc = run_triumphant("-C", "no-such-collection")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unknown collection", proc.stderr)


if __name__ == "__main__":
    unittest.main()
