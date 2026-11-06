import math
import unittest
from bench_analysis import analyze


class BenchTests(unittest.TestCase):
    def setUp(self):
        self.points = [(.1, .6), (.2, 1), (-.1, -.6), (-.2, -1)]

    def test_separates_linear_compliance_from_gap(self):
        result = analyze(self.points)
        self.assertAlmostEqual(result['branch_gap_mm'], .4)
        self.assertAlmostEqual(result['positive_stiffness_Nm_rad'], 2.5)
        self.assertAlmostEqual(result['apparent_lost_motion_deg'], math.degrees(.004))

    def test_pure_elasticity_has_no_gap(self):
        result = analyze([(f, 4*f) for f, _ in self.points])
        self.assertAlmostEqual(result['branch_gap_mm'], 0)

    def test_zero_offset_does_not_change_gap_or_stiffness(self):
        a = analyze(self.points)
        b = analyze([(f, d+12) for f, d in self.points])
        for key in ('branch_gap_mm', 'positive_stiffness_Nm_rad'):
            self.assertAlmostEqual(a[key], b[key])

    def test_radius_changes_converted_metrics(self):
        a, b = analyze(self.points, 100), analyze(self.points, 200)
        self.assertAlmostEqual(b['positive_stiffness_Nm_rad'], 4*a['positive_stiffness_Nm_rad'])
        self.assertAlmostEqual(b['apparent_lost_motion_deg'], a['apparent_lost_motion_deg']/2)

    def test_invalid_or_insufficient_data(self):
        for points in ([], [(1, 1), (1, 2), (-1, -1), (-2, -2)],
                       [(1, -1), (2, -2), (-1, 1), (-2, 2)], [(float('nan'), 1)]):
            with self.subTest(points=points), self.assertRaises(ValueError):
                analyze(points)
        with self.assertRaises(ValueError):
            analyze(self.points, 0)


if __name__ == '__main__':
    unittest.main()
