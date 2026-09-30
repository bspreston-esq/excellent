"""Tests for excellent.py — most triumphant, dude!"""

import subprocess
import sys
import unittest

import excellent


def run_excellent(*args):
    return subprocess.run(
        [sys.executable, "excellent.py", *args],
        capture_output=True,
        text=True,
        cwd=".",
    )


class ExcellentTest(unittest.TestCase):
    def test_regular_quote_from_regular_set(self):
        proc = run_excellent()
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), excellent.REGULAR_QUOTES)

    def test_careful_quote_from_careful_set(self):
        proc = run_excellent("--careful")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), excellent.CAREFUL_QUOTES)

    def test_bogus_quote_from_bogus_set(self):
        proc = run_excellent("--bogus")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(proc.stdout.strip(), excellent.BOGUS_QUOTES)

    def test_help_exits_zero_and_shows_usage(self):
        proc = run_excellent("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stdout)
        self.assertIn("--careful", proc.stdout)
        self.assertIn("--bogus", proc.stdout)

    def test_invalid_argument_exits_nonzero_with_usage(self):
        proc = run_excellent("--totally-bogus-flag")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stderr)

    def test_conflicting_modes_rejected(self):
        proc = run_excellent("--careful", "--bogus")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usage:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
