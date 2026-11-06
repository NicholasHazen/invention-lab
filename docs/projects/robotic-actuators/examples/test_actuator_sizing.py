"""Behavioral and conservation checks, runnable with Python's unittest."""
import math
import unittest
from actuator_sizing import Rotary, triangular, ideal_cycle, weighted_rms, screw, tendon


class SizingTests(unittest.TestCase):
    def setUp(self):
        self.p = Rotary(1e-5)

    def test_shared_reference_numbers(self):
        e = self.p.envelope()
        self.assertAlmostEqual(e['gravity_max_Nm'], .28449)
        self.assertAlmostEqual(e['load_inertia_kg_m2'], .002766666666666667)
        self.assertAlmostEqual(e['output_peak_rpm'], 30)
        self.assertAlmostEqual(e['motor_peak_rpm'], 90)

    def test_triangle_area_and_endpoints(self):
        n = 2000
        distance = sum(triangular((i+.5)/n, 1, math.pi/2)[1]/n for i in range(n))
        self.assertAlmostEqual(distance, math.pi/2, places=12)
        self.assertEqual(triangular(0, 1, 1)[0:2], (0, 0))
        self.assertEqual(triangular(1, 1, 1)[0:2], (1, 0))

    def test_move_time_scaling(self):
        fast = Rotary(1e-5, move_time=.5).envelope()
        slow = self.p.envelope()
        self.assertAlmostEqual(fast['acceleration_rad_s2'], 4*slow['acceleration_rad_s2'])
        self.assertAlmostEqual(fast['motor_peak_rpm'], 2*slow['motor_peak_rpm'])
        self.assertEqual(fast['gravity_max_Nm'], slow['gravity_max_Nm'])

    def test_signed_reverse_profile(self):
        for t in (.1, .3, .6, .9):
            self.assertEqual(triangular(t, 1, -2), tuple(-x for x in triangular(t, 1, 2)))

    def test_ratio_changes_rotor_and_load_oppositely(self):
        e1 = self.p.envelope()
        e2 = Rotary(1e-5, ratio=6).envelope()
        self.assertAlmostEqual(e2['motor_transmission_subtotal_Nm'], e1['motor_transmission_subtotal_Nm']/2)
        self.assertAlmostEqual(e2['motor_rotor_term_Nm'], 2*e1['motor_rotor_term_Nm'])
        self.assertAlmostEqual(e2['reflected_load_inertia_kg_m2'], e1['reflected_load_inertia_kg_m2']/4)

    def test_rotor_inertia_is_required(self):
        with self.assertRaises(TypeError):
            Rotary()

    def test_cycle_energy_conservation(self):
        rows = ideal_cycle(self.p)
        work = sum(r['motor_power_ideal_W']*r['dt_s'] for r in rows)
        # Round trip returns potential and kinetic energy; only friction remains.
        self.assertAlmostEqual(work, 2*self.p.angle*self.p.friction, places=10)

    def test_upward_energy_matches_potential_plus_friction(self):
        rows = [r for r in ideal_cycle(self.p) if r['segment'] == 'up']
        work = sum(r['motor_power_ideal_W']*r['dt_s'] for r in rows)
        self.assertAlmostEqual(work, self.p.gravity_max + self.p.angle*self.p.friction, places=6)

    def test_trace_does_not_silently_apply_forward_loss_to_regen(self):
        a = ideal_cycle(self.p, samples_per_segment=10)
        b = ideal_cycle(Rotary(1e-5, forward_efficiency=.5), samples_per_segment=10)
        self.assertEqual(a, b)
        self.assertTrue(any(r['motor_power_ideal_W'] < 0 for r in a))

    def test_rms_weights_duration_and_sign(self):
        rows = [{'dt_s': 1, 'x': 3}, {'dt_s': 3, 'x': -1}]
        self.assertAlmostEqual(weighted_rms(rows, 'x'), math.sqrt(3))

    def test_holds_include_gravity_without_friction_credit(self):
        rows = ideal_cycle(self.p, samples_per_segment=2)
        hold = [r for r in rows if r['segment'] == 'hold_horizontal'][0]
        self.assertAlmostEqual(hold['motor_torque_ideal_Nm'], .28449/3)
        self.assertEqual(hold['motor_power_ideal_W'], 0)

    def test_screw_power_balance_and_lead_tradeoff(self):
        a = screw()
        self.assertEqual(a['rpm'], 600)
        self.assertAlmostEqual(a['torque_Nm']*a['rpm']*2*math.pi/60, a['input_power_W'])
        b = screw(lead=.004)
        self.assertEqual(b['rpm'], a['rpm']/2)
        self.assertAlmostEqual(b['torque_Nm'], 2*a['torque_Nm'])

    def test_tendon_work_and_spool_tradeoff(self):
        a = tendon()
        self.assertAlmostEqual(a['tension_N'], 15)
        self.assertAlmostEqual(a['spool_torque_Nm'], .12)
        self.assertAlmostEqual(a['spool_angle_deg'], 75)
        self.assertAlmostEqual(a['spool_torque_Nm']*math.radians(a['spool_angle_deg']),
                               5*.030*math.pi/3)
        b = tendon(spool_radius=.016)
        self.assertAlmostEqual(b['spool_torque_Nm'], 2*a['spool_torque_Nm'])
        self.assertAlmostEqual(b['spool_angle_deg'], a['spool_angle_deg']/2)

    def test_invalid_inputs_are_rejected(self):
        for kwargs in ({'move_time': 0}, {'ratio': -1}, {'forward_efficiency': 1.1},
                       {'payload_mass': float('nan')}, {'friction': -1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Rotary(1e-5, **kwargs)
        for args in ((-1, 1, 1), (2, 1, 1), (0, 0, 1)):
            with self.assertRaises(ValueError):
                triangular(*args)
        with self.assertRaises(ValueError):
            screw(efficiency=0)
        with self.assertRaises(ValueError):
            tendon(spool_radius=0)


if __name__ == '__main__':
    unittest.main()
