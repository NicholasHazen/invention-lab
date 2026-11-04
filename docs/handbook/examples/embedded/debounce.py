"""Time-based button debouncer, usable in CPython or MicroPython.

An event is True for a newly accepted press, False for a newly accepted release,
or None when the accepted state has not changed. All times are milliseconds.
"""


class Debouncer:
    def __init__(self, interval_ms=20, elapsed_ms=None):
        if interval_ms <= 0:
            raise ValueError("Debounce interval must be positive")
        self.interval_ms = interval_ms
        self.elapsed_ms = elapsed_ms or (lambda now, then: now - then)
        self.stable = False
        self.candidate = False
        self.since_ms = 0

    def update(self, now_ms, pressed):
        pressed = bool(pressed)
        if pressed != self.candidate:
            self.candidate = pressed
            self.since_ms = now_ms
        elif self.candidate != self.stable:
            if self.elapsed_ms(now_ms, self.since_ms) >= self.interval_ms:
                self.stable = self.candidate
                return self.stable
        return None
