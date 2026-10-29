"""Check the scientific input and shared clock of the shortened campaign.

Runs from the tests/ folder of the C7 package with calendar28_T230.patch applied, as in the
v4.6 archives and in CI (.github/workflows/checks.yml, package v4.6-calendar28):
  unzip sweep/v33_c7/A22_fresh_launch_v3_3_C7.zip; patch -p1 -d <pkg> < calendar28_T230.patch
  cp test_calendar28.py <pkg>/tests/; cd <pkg>; python -B -m unittest discover -s tests
"""
import sys
import unittest
from decimal import Decimal
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'affine')]
import engine, run, temporal

class Calendar28(unittest.TestCase):
    def test_shared_source_and_exact_dates(self):
        trains = run.initial_trains('calendar-test', temporal)
        self.assertEqual(list(map(len, trains)), [28] + [0] * 11)
        first = trains[0][0]
        for k, pulse in enumerate(trains[0]):
            self.assertEqual((pulse.box().lo, pulse.box().hi), (8*k, 8*k))
            self.assertIs(pulse.terms, first.terms)
            self.assertEqual(pulse.minus(first).lo, 8*k)
            self.assertEqual(pulse.minus(first).hi, 8*k)
        self.assertEqual(trains[0][-1].token(), ('clock', '216'))

    def test_quiet_cell_runs_to_early_terminal_horizon(self):
        result = engine.compute_cell(1, 6, [()] * 12, 'calendar-test/quiet')
        self.assertEqual(result['outputs'], ())
        self.assertEqual(result['state']['terminal_affine']['t'].token(), ('clock', '2.3E+2'))

    def test_silent_auxiliary_relaxation_uses_230(self):
        result = engine.compute_cell(1, 6, [()] * 12, 'calendar-test/relaxation')
        for lo, hi in result['state']['m']:
            width = Decimal(hi) - Decimal(lo)
            self.assertGreater(width, Decimal('1e-56'))
            self.assertLess(width, Decimal('1e-53'))

    def test_input_whose_cycle_extends_past_terminal_is_refused(self):
        trains = [()] * 12
        temporal.begin_producer('late-input')
        from affine_iv import I
        trains[0] = (temporal.Time('late', I('229.5')),)
        with self.assertRaises(AssertionError):
            engine.compute_cell(1, 0, trains, 'calendar-test/unfinished')

if __name__ == '__main__':
    unittest.main()
