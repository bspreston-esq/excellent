"""Tests for triumphant.py — most triumphant, dude!"""

import subprocess
import sys
import unittest

import triumphant


def run_triumphant(*args):
    return subprocess.run(
        [sys.executable, "triumphant.py", *args],
        capture_output=True,
        text=True,
        cwd=".",
    )


class TriumphantTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
