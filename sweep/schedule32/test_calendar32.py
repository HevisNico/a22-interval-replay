"""Check the scientific input and shared clock of the shortened campaign."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'affine')]
import engine, run, temporal

class Calendar32(unittest.TestCase):
    def test_shared_source_and_exact_dates(self):
        trains = run.initial_trains('calendar-test', temporal)
        self.assertEqual(list(map(len, trains)), [32] + [0] * 11)
        first = trains[0][0]
        for k, pulse in enumerate(trains[0]):
            self.assertEqual((pulse.box().lo, pulse.box().hi), (8*k, 8*k))
            self.assertIs(pulse.terms, first.terms)
            self.assertEqual(pulse.minus(first).lo, 8*k)
            self.assertEqual(pulse.minus(first).hi, 8*k)
        self.assertEqual(trains[0][-1].token(), ('clock', '248'))

    def test_quiet_cell_runs_to_original_terminal_horizon(self):
        result = engine.compute_cell(1, 6, [()] * 12, 'calendar-test/quiet')
        self.assertEqual(result['outputs'], ())
        self.assertEqual(result['state']['terminal_affine']['t'].token(), ('clock', '1116'))

if __name__ == '__main__':
    unittest.main()
