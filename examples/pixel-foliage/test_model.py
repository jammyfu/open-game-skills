import unittest
from model import viewport, leaf_offset, recovery, haze


class Contracts(unittest.TestCase):
    def test_odd_viewport(self):
        self.assertEqual(viewport((1365, 767)), (4, (42, 23)))

    def test_too_small_rejected(self):
        with self.assertRaises(ValueError):
            viewport((319, 180))

    def test_calm_and_inner_canopy(self):
        for n in range(400):
            self.assertEqual(leaf_offset(n / 100, 17, 0), (0, 0))
            self.assertEqual(leaf_offset(n / 100, 17, edge=.3), (0, 0))

    def test_world_wave_and_discrete_hold(self):
        for n in range(40):
            t = n / 10
            self.assertEqual(leaf_offset(t, 0), leaf_offset(t, 80))
            self.assertEqual(leaf_offset(t, 0), leaf_offset(t + .09, 0))
            self.assertTrue(all(isinstance(x, int) for x in leaf_offset(t, 0)))

    def test_rates_sample_same_time(self):
        for n in range(120):
            self.assertEqual(leaf_offset(n / 30, 11), leaf_offset(4*n / 120, 11))

    def test_recovery_overshoots_and_settles(self):
        self.assertTrue(any(recovery(n/100) < 0 for n in range(300)))
        self.assertLess(abs(recovery(10)), 1e-7)

    def test_haze_endpoints_alpha_foreground(self):
        color, sky = (24, 64, 32, 137), (120, 180, 240)
        self.assertEqual(haze(color, sky, 0), color)
        self.assertEqual(haze(color, sky, 1), sky + (137,))
        self.assertEqual(haze(color, sky, .5), (72, 122, 136, 137))
        self.assertEqual(haze(color, sky, 1, foreground=True), color)


if __name__ == '__main__':
    unittest.main()
