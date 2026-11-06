#!/usr/bin/env python3
"""Original numerical study. No hardware, network, or motor-control interfaces.

SI internally. A forward-efficiency sizing envelope is separate from the IDEAL
reversible-transmission cycle trace. Neither is a hardware rating.
"""
import argparse
import csv
from dataclasses import dataclass
import math


def positive(name, value, allow_zero=False):
    if not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero):
        raise ValueError(f"{name} must be finite and {'nonnegative' if allow_zero else 'positive'}")
    return value


@dataclass(frozen=True)
class Rotary:
    rotor_inertia: float  # Required input, kg m^2; not a hidden zero.
    payload_mass: float = 0.25
    payload_radius: float = 0.100
    arm_mass: float = 0.08
    arm_length: float = 0.100
    angle: float = math.pi / 2
    move_time: float = 1.0
    ratio: float = 3.0
    forward_efficiency: float = 0.90
    friction: float = 0.010
    gravity: float = 9.81

    def __post_init__(self):
        for name, value in self.__dict__.items():
            positive(name, value, name in ('rotor_inertia', 'payload_mass', 'arm_mass', 'friction'))
        if self.forward_efficiency > 1:
            raise ValueError('forward_efficiency must be <= 1')

    @property
    def load_inertia(self):
        return self.payload_mass * self.payload_radius**2 + self.arm_mass * self.arm_length**2 / 3

    @property
    def gravity_max(self):
        return self.gravity * (self.payload_mass * self.payload_radius + self.arm_mass * self.arm_length / 2)

    @property
    def acceleration(self):
        return 4 * self.angle / self.move_time**2

    def envelope(self):
        acceleration_torque = self.load_inertia * self.acceleration
        output = self.gravity_max + acceleration_torque + self.friction
        subtotal = output / (self.ratio * self.forward_efficiency)
        rotor_term = self.rotor_inertia * self.ratio * self.acceleration
        return dict(load_inertia_kg_m2=self.load_inertia,
                    gravity_max_Nm=self.gravity_max,
                    acceleration_rad_s2=self.acceleration,
                    acceleration_torque_Nm=acceleration_torque,
                    output_envelope_Nm=output,
                    motor_transmission_subtotal_Nm=subtotal,
                    motor_rotor_term_Nm=rotor_term,
                    motor_envelope_Nm=subtotal + rotor_term,
                    output_peak_rpm=2 * self.angle / self.move_time * 60 / (2 * math.pi),
                    motor_peak_rpm=self.ratio * 2 * self.angle / self.move_time * 60 / (2 * math.pi),
                    reflected_load_inertia_kg_m2=self.load_inertia / self.ratio**2)


def triangular(t, duration, displacement):
    """Displacement, speed, acceleration, including one-sided end acceleration.

    Acceleration jumps are mathematical idealizations, not commands for a drive.
    Integrators below use midpoint samples, avoiding jump ambiguities.
    """
    positive('duration', duration)
    if not math.isfinite(displacement) or not math.isfinite(t) or not 0 <= t <= duration:
        raise ValueError('finite displacement and 0 <= t <= duration required')
    a = 4 * displacement / duration**2
    if t < duration / 2:
        return 0.5 * a * t**2, a * t, a
    remaining = duration - t
    return displacement - 0.5 * a * remaining**2, a * remaining, -a


def ideal_cycle(p, hold_seconds=1.0, samples_per_segment=2000):
    """Up, hold upper, down, hold horizontal; IDEAL transmission, signed friction.

    Gravity depends on angle from horizontal. Rotor inertia is included. Holds
    receive no friction credit. Pulley inertia, losses, stiction and control
    transients are absent. Returns midpoint samples with duration for RMS.
    """
    positive('hold_seconds', hold_seconds, True)
    if not isinstance(samples_per_segment, int) or samples_per_segment < 2:
        raise ValueError('samples_per_segment must be an integer >= 2')
    rows = []
    elapsed = 0.0
    segments = [('up', p.move_time, 0.0, p.angle),
                ('hold_upper', hold_seconds, p.angle, 0.0),
                ('down', p.move_time, p.angle, -p.angle),
                ('hold_horizontal', hold_seconds, 0.0, 0.0)]
    for name, duration, start, displacement in segments:
        if duration == 0:
            continue
        dt = duration / samples_per_segment
        for i in range(samples_per_segment):
            t = (i + 0.5) * dt
            if displacement:
                dtheta, omega, alpha = triangular(t, duration, displacement)
                moving_friction = math.copysign(p.friction, omega)
            else:
                dtheta = omega = alpha = moving_friction = 0.0
            theta = start + dtheta
            torque = p.gravity_max * math.cos(theta) + p.load_inertia * alpha + moving_friction
            motor = torque / p.ratio + p.rotor_inertia * p.ratio * alpha
            rows.append(dict(segment=name, time_s=elapsed+t, dt_s=dt,
                             angle_rad=theta, output_speed_rad_s=omega,
                             output_accel_rad_s2=alpha, output_torque_Nm=torque,
                             motor_torque_ideal_Nm=motor,
                             motor_power_ideal_W=motor*p.ratio*omega))
        elapsed += duration
    return rows


def weighted_rms(rows, field):
    if not rows:
        raise ValueError('at least one sample required')
    durations = [positive('dt_s', row['dt_s']) for row in rows]
    values = [row[field] for row in rows]
    if any(not math.isfinite(x) for x in values):
        raise ValueError('sample values must be finite')
    return math.sqrt(math.fsum(dt*x*x for dt, x in zip(durations, values))/math.fsum(durations))


def screw(force=10.0, lead=0.002, speed=0.020, efficiency=0.35):
    for name, value in locals().copy().items():
        positive(name, value)
    if efficiency > 1:
        raise ValueError('efficiency must be <= 1')
    return dict(rpm=speed/lead*60, torque_Nm=force*lead/(2*math.pi*efficiency),
                output_power_W=force*speed, input_power_W=force*speed/efficiency)


def tendon(tip_force=5.0, tip_arm=0.030, tendon_arm=0.010,
           spool_radius=0.008, finger_angle=math.pi/3):
    for name, value in locals().copy().items():
        positive(name, value)
    tension = tip_force * tip_arm / tendon_arm
    travel = tendon_arm * finger_angle
    return dict(tension_N=tension, spool_torque_Nm=tension*spool_radius,
                tendon_travel_m=travel, spool_angle_deg=math.degrees(travel/spool_radius))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rotor-inertia', type=float, required=True, help='specified motor rotor inertia in kg m^2')
    parser.add_argument('--move-time', type=float, default=1.0)
    parser.add_argument('--ratio', type=float, default=3.0)
    parser.add_argument('--csv', help='optional ideal cycle trace output path')
    args = parser.parse_args()
    try:
        p = Rotary(args.rotor_inertia, move_time=args.move_time, ratio=args.ratio)
    except ValueError as exc:
        parser.error(str(exc))
    print('POSITIVE MOTORING ENVELOPE (assumed forward efficiency 0.90)')
    for k, v in p.envelope().items():
        print(f'{k}: {v:.9f}')
    rows = ideal_cycle(p)
    print('\nIDEAL TRANSMISSION CYCLE: up, hold upper 1 s, down, hold horizontal 1 s')
    print(f'motor_RMS_ideal_Nm: {weighted_rms(rows, "motor_torque_ideal_Nm"):.9f}')
    print(f'cycle_mechanical_work_ideal_J: {math.fsum(r["motor_power_ideal_W"]*r["dt_s"] for r in rows):.9f}')
    for name, values in [('SCREW', screw()), ('TENDON', tendon())]:
        print('\n'+name)
        for k, v in values.items():
            print(f'{k}: {v:.9f}')
    if args.csv:
        with open(args.csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f'Wrote {len(rows)} midpoint samples to {args.csv}')


if __name__ == '__main__':
    main()
