import tempfile
import unittest
from pathlib import Path
from generator import build, validate

class GeneratorTests(unittest.TestCase):
    def test_small_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            tables = build(Path(directory), 0.02, 20261022)
            self.assertEqual(len(tables["employees"]), 20)
            self.assertEqual(len(tables["tasks"]), 160)
            self.assertEqual(len(tables["ground_truth"]), 5)
            self.assertTrue(validate(tables)["passed"])

if __name__ == "__main__":
    unittest.main()
