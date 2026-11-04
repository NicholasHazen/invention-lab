"""Run: python3 -m unittest -v test_labs.py from this folder."""
import math
import unittest
import sensor_log
import control_lab
import robot_arm
import vision_baseline
import message_lab


class LogTests(unittest.TestCase):
    def test_reference_points_and_midpoint(self):
        for raw, expected in [(100, 0), (500, 20), (900, 40)]:
            self.assertAlmostEqual(sensor_log.calibrate_mm(raw), expected)

    def test_bad_time_and_range(self):
        rows = [{"time_s": t, "raw_count": raw, "status": "ok"}
                for t, raw in [(0, 100), (0, 300), (1, 1024), (float("nan"), 100)]]
        accepted, rejected = sensor_log.clean_rows(rows)
        self.assertEqual((len(accepted), len(rejected)), (1, 3))


class ControlTests(unittest.TestCase):
    def test_p_offset_and_pi_rejection(self):
        self.assertAlmostEqual(control_lab.simulate()[-1]["output"], 0.4, places=3)
        self.assertAlmostEqual(control_lab.simulate(ki=1, disturbance=-0.1, duration=40)[-1]["output"], 0.6, places=3)

    def test_saturation_and_windup(self):
        reference = lambda t: 2.0 if t < 10 else 0.4
        plain = control_lab.simulate(ki=1, reference=reference, antiwindup=False)
        protected = control_lab.simulate(ki=1, reference=reference)
        self.assertTrue(all(0 <= s["applied"] <= 1 for s in plain + protected))
        self.assertGreater(plain[599]["output"], 0.99)
        self.assertLess(protected[599]["output"], 0.6)


class RobotTests(unittest.TestCase):
    def test_forward_and_frame(self):
        x, y = robot_arm.forward(math.pi / 6, -math.pi / 3)
        self.assertAlmostEqual(x, 90 * math.sqrt(3))
        self.assertAlmostEqual(y, 10)
        self.assertAlmostEqual(robot_arm.transform_point(20, 0, math.pi / 2, 50, 30)[1], 50)

    def test_inverse_roundtrip_and_rejection(self):
        for elbow in (-1, 1):
            q = robot_arm.inverse(120, 40, elbow=elbow)
            for actual, expected in zip(robot_arm.forward(*q), (120, 40)):
                self.assertAlmostEqual(actual, expected)
        with self.assertRaises(ValueError):
            robot_arm.inverse(190, 0)


class VisionTests(unittest.TestCase):
    def test_split_and_confusion_matrix(self):
        train, test = vision_baseline.records()
        self.assertFalse(set(r[0] for r in train) & set(r[0] for r in test))
        threshold = vision_baseline.choose_threshold(train)
        self.assertEqual(threshold, 3)
        result = vision_baseline.evaluate(test, threshold)
        self.assertEqual([result[k] for k in ("tp", "fp", "tn", "fn")], [3, 2, 2, 1])
        self.assertAlmostEqual(result["precision"], 0.6)


class MessageTests(unittest.TestCase):
    def test_duplicate_cannot_refresh_watchdog(self):
        receiver = message_lab.Receiver()
        self.assertEqual(receiver.receive(message_lab.command(1, 0), 0), "applied")
        self.assertEqual(receiver.receive(message_lab.command(1, 0), 0.8), "duplicate or old")
        self.assertEqual(receiver.tick(2.0), "off")

    def test_expired_invalid_and_out_of_order(self):
        receiver = message_lab.Receiver()
        self.assertEqual(receiver.receive(message_lab.command(3, 0), 2), "expired or future")
        self.assertEqual(receiver.receive(message_lab.command(True, 2), 2), "invalid schema")
        self.assertEqual(receiver.receive(message_lab.command(3, 2), 2), "applied")
        self.assertEqual(receiver.receive(message_lab.command(2, 2), 2), "duplicate or old")


if __name__ == "__main__":
    unittest.main()
