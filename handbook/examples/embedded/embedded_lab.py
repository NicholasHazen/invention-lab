"""Deterministic button/timing lab. Run beside debounce.py with Python 3."""

from debounce import Debouncer

BOUNCE_TRACE = [(10, True), (12, False), (15, True), (17, False),
                (20, True), (100, False), (103, True), (105, False)]


def simulate(trace, duration_ms=1100):
    button = Debouncer(interval_ms=20)
    raw = False
    transition_index = 0
    events = []
    last_heartbeat = 0
    for now in range(duration_ms + 1):
        while transition_index < len(trace) and trace[transition_index][0] <= now:
            raw = trace[transition_index][1]
            transition_index += 1
        event = button.update(now, raw)
        if event is not None:
            events.append((now, "pressed" if event else "released"))
        if now - last_heartbeat >= 500:
            events.append((now, "heartbeat"))
            last_heartbeat = now
    return events


def self_check():
    assert simulate(BOUNCE_TRACE) == [(40, "pressed"), (125, "released"),
                                      (500, "heartbeat"), (1000, "heartbeat")]
    assert simulate([(10, True), (29, False)], 100) == []  # A short glitch.
    assert simulate([(0, True)], 100) == [(20, "pressed")]  # Held at boot.
    assert simulate([(10, True), (50, False)], 100) == [(30, "pressed"), (70, "released")]
    # Exercise rollover using a deliberately tiny 256-tick clock.
    modular_difference = lambda now, then: ((now - then + 128) % 256) - 128
    button = Debouncer(20, modular_difference)
    assert button.update(250, True) is None
    assert button.update(13, True) is None  # 19 ms after 250.
    assert button.update(14, True) is True  # 20 ms after 250.


def main():
    self_check()
    print("time_ms,event")
    for now, event in simulate(BOUNCE_TRACE):
        print(f"{now},{event}")
    print("PASS: bounce, short glitch, held-at-boot, ordinary edges, rollover")


if __name__ == "__main__":
    main()
