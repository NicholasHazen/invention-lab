"""Two-link planar geometry in millimetres and radians; no motors or ROS needed."""
import math


def forward(q1, q2, l1=100.0, l2=80.0):
    return (l1 * math.cos(q1) + l2 * math.cos(q1 + q2),
            l1 * math.sin(q1) + l2 * math.sin(q1 + q2))


def inverse(x, y, l1=100.0, l2=80.0, elbow=1):
    if l1 <= 0 or l2 <= 0 or elbow not in (-1, 1):
        raise ValueError("positive link lengths and elbow +/-1 required")
    c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    if not -1.0 - 1e-12 <= c2 <= 1.0 + 1e-12:
        raise ValueError("target outside geometric workspace")
    q2 = elbow * math.acos(max(-1.0, min(1.0, c2)))
    q1 = math.atan2(y, x) - math.atan2(l2 * math.sin(q2), l1 + l2 * math.cos(q2))
    return q1, q2


def transform_point(x, y, angle_rad, offset_x, offset_y):
    return (math.cos(angle_rad) * x - math.sin(angle_rad) * y + offset_x,
            math.sin(angle_rad) * x + math.cos(angle_rad) * y + offset_y)


def main():
    point = forward(math.radians(30), math.radians(-60))
    print(f"q1=30 deg q2=-60 deg -> x={point[0]:.3f} mm y={point[1]:.3f} mm")
    for elbow in [-1, 1]:
        angles = inverse(*point, elbow=elbow)
        print(f"elbow={elbow:+d}: q1={math.degrees(angles[0]):.3f} deg q2={math.degrees(angles[1]):.3f} deg")
    transformed = transform_point(20, 0, math.pi / 2, 50, 30)
    print(f"camera point (20, 0) -> base ({transformed[0]:.1f}, {transformed[1]:.1f}) mm")
    try:
        inverse(190, 0)
    except ValueError as error:
        print(f"(190, 0) rejected: {error}")


if __name__ == "__main__":
    main()
