# Electronics and embedded lab files

Desktop requirements: Python 3, no third-party packages. Download the Python files into one folder. Open a terminal in that folder. On systems where Python is named `python` rather than `python3`, substitute that command.

- `python3 circuit_lab.py`: ideal resistor calculations. Defaults report MID = 1.500 V unloaded and 1.000 V loaded, with source currents 150.0 µA and 200.0 µA. Checks enforce current and power accounting.
- `python3 signal_lab.py`: synthetic RC and sampling calculations; creates or overwrites `rc_step.csv` and `alias_samples.csv` in the current folder. Defaults report 10.000 ms, 2.086 V at 10 ms, 3.278 V at 50 ms, and an alias comparison difference smaller than 1e-12. This is ideal model data, not measurement data.
- `python3 embedded_lab.py`: requires `debounce.py` in the same folder. Expected event rows are `40,pressed`, `125,released`, `500,heartbeat`, `1000,heartbeat`, followed by a PASS line. The clock is simulated; execution does not wait for real elapsed time.

The desktop programs and checks were run during handbook preparation. The optional `pico_button_logger.py` is a full MicroPython example but was **not run on physical hardware**. Its syntax was checked on desktop; that cannot verify board pins, electrical behavior, USB operation, or real timing.

For that optional exercise, use an original non-wireless RP2040 Raspberry Pi Pico or Pico H, with the matching MicroPython v1.26.0 firmware. Follow the official board instructions for firmware installation and file transfer. With USB disconnected, connect a normally open momentary switch between the board's GP15 and a GND pin, using the official pinout. GP15 is a signal name, not physical pin 15. Verify the switch contacts with a continuity meter while unpowered. Reconnect USB, copy `debounce.py` and `pico_button_logger.py` to the board's filesystem, and run the latter from the connected MicroPython editor/REPL. Expected: onboard LED changes state about every half second, and each deliberate press/release prints one event pair with board-relative timestamps. Stop using Ctrl-C; the LED should turn off. No motor, external power supply, or external LED is involved.

These programs teach specific ideal models and behavior. They are not production motor-control firmware, calibrated instruments, or evidence that the pivot has been actuated or load-tested.
