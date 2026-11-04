"""Optional original RP2040 Pico/Pico H exercise. NOT tested on hardware.

Requires MicroPython v1.26.0 for the original, non-wireless Raspberry Pi Pico.
Copy this file AND debounce.py onto the board. Run this file interactively.
Do not rename it main.py until the wiring and manual run have been checked.
USB power only. Momentary switch connects GP15 to a GND pin; no other supply.
Uses the original Pico's onboard LED on GP25; not a Pico W/other-board example.
"""

from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms
from debounce import Debouncer

button_pin = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin(25, Pin.OUT, value=0)
button = Debouncer(interval_ms=20, elapsed_ms=ticks_diff)
last_heartbeat = ticks_ms()

print("time_ms,event")
try:
    while True:
        now = ticks_ms()
        event = button.update(now, button_pin.value() == 0)
        if event is not None:
            print("{},{}".format(now, "pressed" if event else "released"))
        if ticks_diff(now, last_heartbeat) >= 500:
            led.toggle()
            last_heartbeat = now
        sleep_ms(1)
finally:
    led.off()
