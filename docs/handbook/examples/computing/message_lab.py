"""Replay an application command policy in memory. No sockets or physical outputs."""
import math


class Receiver:
    def __init__(self, timeout_s=2.0):
        self.last_sequence = -1
        self.last_received = None
        self.state = "off"
        self.timeout_s = timeout_s

    def receive(self, message, now):
        try:
            seq, sent, state = message["sequence"], message["sent_s"], message["state"]
            if type(message["version"]) is not int or message["version"] != 1:
                return "invalid schema"
            if type(seq) is not int or seq < 0:
                return "invalid schema"
            if type(sent) not in (int, float) or not math.isfinite(sent):
                return "invalid time"
            if state not in ("on", "off"):
                return "invalid state"
        except (KeyError, TypeError):
            return "invalid schema"
        # This lab shares a simulated clock. Real clocks require an explicit synchronization policy.
        if not 0 <= now - sent <= 1.0:
            return "expired or future"
        if seq <= self.last_sequence:
            return "duplicate or old"
        self.last_sequence = seq
        self.last_received = now
        self.state = state
        return "applied"

    def tick(self, now):
        if self.last_received is None or now - self.last_received >= self.timeout_s:
            self.state = "off"
        return self.state


def command(sequence, sent_s, state="on"):
    return {"version": 1, "sequence": sequence, "sent_s": sent_s, "state": state}


def main():
    receiver = Receiver()
    events = [(0.0, command(1, 0.0)), (0.1, command(1, 0.0)),
              (0.2, command(0, 0.0)), (3.0, command(2, 0.0)),
              (3.1, command(3, 3.1, "off"))]
    for now, message in events:
        receiver.tick(now)
        verdict = receiver.receive(message, now)
        print(f"t={now:.1f} seq={message['sequence']} {verdict}; state={receiver.state}")
    print(f"t=6.0 timeout state={receiver.tick(6.0)}")


if __name__ == "__main__":
    main()
