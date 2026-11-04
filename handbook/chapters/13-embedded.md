# Embedded systems: make time and state explicit

A sensor logger seems simple: read a sensor, save a number, and respond to a button. The difficulty appears when those actions overlap. A button changes while a reading is in progress. A sensor fails to reply. A file write takes longer than usual. The device restarts with its button already held down. Embedded engineering is largely the work of deciding what those situations mean.

This chapter builds a small, testable behavior model before putting it on a board. You will separate raw inputs from accepted events, schedule work without long pauses, and describe recovery states. You need the circuit and sampling chapters plus basic variables, functions, and conditionals from [software and data](../software-data/). The main lab uses ordinary Python on a laptop; an optional complete MicroPython adaptation targets one specific board.

## What a microcontroller contains

A microcontroller combines a processor with memory and peripherals on one chip. The processor executes instructions. Flash memory commonly holds the program after power is removed; RAM holds temporary working data. Peripherals perform specialized jobs such as timing, analog conversion, counting pulses, and moving bytes across communication interfaces.

A development board adds practical support: a power regulator, USB connection, accessible pins, and sometimes an indicator or radio. Board names and chip names are not interchangeable. Raspberry Pi's Pico documentation, for example, distinguishes the Pico microcontroller boards from Linux-running Raspberry Pi computers and identifies several board variants. A pin assumption valid for one variant may be wrong for another. [Official Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) is the starting point for board identification and pinouts.

A general-purpose input/output pin, GPIO, is configured as an input or output. As an input it observes voltage according to specified logic thresholds. As an output it can source or sink only limited current. It cannot directly power a motor. An unconnected input can float, meaning its voltage has no well-defined logic state. A pull-up resistor gives it a weak connection to a positive logic supply; a switch to ground can then deliberately pull it low.

With that wiring, an open button reads high and a pressed button reads low. Convert this electrical fact into a meaningful variable such as `pressed = raw_value == 0` near the input boundary. The rest of the program should reason about a press rather than repeatedly remembering whether zero means active.

## One press can contain many electrical transitions

Mechanical contacts can bounce: on closing or opening, they make and break contact several times before settling. Counting every raw edge can turn one deliberate press into several commands. A common solution accepts a changed state only after it has remained unchanged for a chosen interval.

Our example keeps three pieces of information: the accepted state, the candidate state most recently observed, and the time that candidate began. Whenever the raw input changes, it replaces the candidate and restarts the timer. When the candidate has persisted for 20 ms and differs from the accepted state, the program accepts it and emits exactly one event. Twenty milliseconds is a teaching choice to evaluate for a real switch and interaction, not a universal debounce requirement.

Consider a synthetic trace that becomes pressed at 10 ms, released at 12, pressed at 15, released at 17, then pressed continuously from 20 ms onward. The candidate timer restarts at every transition. At 40 ms it has seen twenty uninterrupted milliseconds of the pressed state, so it reports one press. On release, transitions at 100, 103, and 105 ms settle in the released state. The accepted release occurs at 125 ms.

This rule rejects a 19 ms glitch, but it also intentionally ignores a real tap shorter than the required stable duration. Every filter encodes a tradeoff. Before reducing a debounce interval to make an interface feel faster, decide how many extra events you can tolerate and measure the actual switch behavior.

## A loop should keep several promises

The simplest firmware repeatedly reads inputs, updates its model, performs any work that is due, and repeats. A half-second sleep inside that loop prevents ordinary polling during the sleep. The display may blink correctly while the program misses a brief input entirely.

Instead, store when each task last ran and compare it with the current clock. Our heartbeat changes the indicator state when at least 500 ms has elapsed, while button processing runs on every pass. A full indicator on/off cycle then takes approximately one second. The short sleep at the end of the board example yields between polls; it does not promise exact one-millisecond scheduling. USB printing, interpreter overhead, and other work can add delay.

Microcontroller tick counters eventually wrap back to zero. Subtracting two raw tick values can then produce an incorrect interval. The supplied hardware program uses MicroPython's `ticks_diff` for elapsed time, with checks occurring often enough to satisfy its documented half-counter-period limit. It uses the same decision logic as the laptop example while changing how elapsed time is calculated. [MicroPython's time API](https://docs.micropython.org/en/v1.26.0/library/time.html) explains this contract.

Periodic sampling introduces another choice. Scheduling the next read relative to the planned deadline preserves a regular intended cadence, but a late program must decide whether to skip missed samples or catch up. Scheduling relative to the actual completion avoids immediate catch-up bursts but drifts. Record actual timestamps rather than pretending every sample occurred exactly on schedule. The right policy depends on whether you are recording slow temperature changes, controlling motion, or capturing a waveform.

## States make recovery a design decision

A state machine names the situations a device can occupy and defines the events that move it between them. For our eventual logger, a useful first design is:

| Current state | Event | Next state and action |
| --- | --- | --- |
| IDLE | Accepted press | Enter RECORDING; start a new session identifier. |
| RECORDING | Sample due | Attempt one bounded read; log its timestamp and result. |
| RECORDING | Accepted press | Finish the session and return to IDLE. |
| RECORDING | Read timeout or storage failure | Enter FAULT; preserve the error and stop claiming valid samples. |
| FAULT | Restart after the cause is addressed | Return to IDLE; require a new start command. |

The table is a design exercise, not behavior already implemented by the button-only example. It exposes questions that scattered conditions tend to hide. Should a button held during startup begin recording? Does a missing sensor produce a blank value, an old value marked stale, or an error? Should recovery automatically resume the previous activity? Decide these deliberately and test them separately.

For an actuated machine, state transitions must also define outputs. A FAULT state that changes only a screen message while leaving drive enabled is incomplete. Software recovery does not replace current limiting, mechanical limits, or a physical disconnect. This handbook's example drives only an onboard indicator; it is not motor-control firmware.

## Interrupts and watchdogs solve specific problems

Polling observes a pin whenever the program reaches the read operation. An interrupt asks the processor to respond to a hardware event without waiting for that point in the ordinary loop. Interrupts are useful for events that polling might miss, but they introduce concurrency: ordinary code and interrupt code can touch the same information at different moments.

Keep an interrupt handler short. Often it records a timestamp, increments a counter, or places an event in a bounded buffer for ordinary code to process. Printing, waiting, or doing a long sensor transaction inside it can disrupt other deadlines. Shared counters and buffers need deliberate handling so one context cannot observe a half-completed update. A slowly operated button usually does not justify starting with interrupts.

A watchdog is a timer that resets a system if the program fails to report healthy progress within its deadline. Feeding it on every loop regardless of sensor or task health can conceal failures. Feed it only when the checks representing useful progress have succeeded. Record reset causes when available, and make startup outputs safe. Rebooting repeatedly into the same bad command is not recovery. Test watchdog behavior deliberately on a low-energy setup; do not infer it from a blinking indicator.

## Interfaces have both electrical and message rules

UART, I²C, and SPI move digital information between devices, but their names do not define a connector or guarantee voltage compatibility.

| Interface | Basic idea | Common beginner fault |
| --- | --- | --- |
| UART | Separate transmit and receive signals, with agreed data rate and framing. | TX wired to TX instead of the other device's RX, or mismatched logic voltage. |
| I²C | Shared clock and data with addressed devices and pull-up resistors. | Address collision, missing pull-ups, or pull-ups tied to the wrong supply. |
| SPI | Clocked data exchange, typically with a selection signal for each peripheral. | Wrong clock mode, swapped data direction, or incorrect chip selection. |

Non-isolated connections also need a common electrical reference. I²C breakout boards may each carry pull-ups; parallel resistors change the total pull-up resistance. SPI devices differ in when data is sampled relative to clock edges. UART bytes become useful only when both sides agree about message boundaries and meaning. A USB serial console is a convenient computer connection, but it is not the same wiring as a board's UART pins.

Use the sensor's datasheet and the board's peripheral documentation together. Add a timeout to every interaction that could otherwise wait forever. Log enough context—address, operation, elapsed time, and error—to distinguish an absent device from a value outside the expected physical range. The [MicroPython RP2 reference](https://docs.micropython.org/en/v1.26.0/rp2/quickref.html) documents GPIO and peripheral APIs for the version used by the optional exercise.

## Lab: prove the behavior before attaching a button

Download [debounce.py](../examples/embedded/debounce.py) and [embedded_lab.py](../examples/embedded/embedded_lab.py) into one folder. Run `python3 embedded_lab.py`. The program advances a synthetic clock; it does not depend on how fast your computer runs. Its expected output is:

```text
time_ms,event
40,pressed
125,released
500,heartbeat
1000,heartbeat
PASS: bounce, short glitch, held-at-boot, ordinary edges, rollover
```

1. Trace the candidate state from 10 to 40 ms on paper. Explain why the first event is not at 30 ms.
2. Read the `update` function in `debounce.py`. Match each stored variable to your paper trace. Notice that `None`, `True`, and `False` mean three different outcomes: no event, accepted press, and accepted release. Testing merely `if event` would discard release events.
3. In the simulation's `BOUNCE_TRACE`, move the final press transition from 20 to 25 ms. Predict a 45 ms accepted press. Update the corresponding expected assertion only after explaining the changed input, then rerun.
4. Restore the original file. Read the short-glitch, held-at-boot, and counter-rollover checks. Add a second clean press after the release and predict both new events before executing it.

These desktop checks were run during handbook preparation. They demonstrate behavior under specified inputs; they do not establish electrical performance or real-time deadlines on a board.

For the optional hardware adaptation, use an **original non-wireless RP2040 Pico or Pico H**, a normally open button, and USB power. Follow the official pinout. With USB unplugged, connect the switch between **GP15 and GND**; GP15 is a signal name, not physical pin 15. Verify which switch contacts connect when pressed. Copy `debounce.py` and [pico_button_logger.py](../examples/embedded/pico_button_logger.py) to the board using matching MicroPython v1.26.0 firmware, then run the latter interactively. The [example README](../examples/embedded/README.md) gives the complete procedure.

Expected behavior is one printed press/release pair per deliberate operation while the onboard indicator continues blinking. This hardware adaptation has **not been run on a physical board**. An import error usually means the companion file is absent or the wrong Python environment is selected. A permanently pressed input suggests a wiring short or the wrong switch contacts. A floating or erratic input suggests a missing pull-up configuration or wrong pin. The example intentionally excludes motors and external supplies.

## Build the next behavior yourself

**Predict:** Why can a heartbeat blink while the sensor task is broken? Why does “no event” need a different representation from “released”? What does a timeout add to a communication function?

**Answers:** the heartbeat proves only that its own path is running; release is a meaningful transition whereas no event means retain the accepted state; a timeout bounds how long other useful work can be delayed and gives the state machine a failure event.

Extend the desktop model into the IDLE/RECORDING/FAULT logger from the table. Feed it synthetic sensor values and deliberately missing replies. Require a new start command after recovery. Keep inputs separate from decisions so the same tests remain useful when hardware arrives. For a deeper architecture and debugging path, Elecia White's paid [*Making Embedded Systems*, second edition](https://www.oreilly.com/library/view/making-embedded-systems/9781098151539/) is appropriate after you can explain this program; it expects more programming experience than a first blinking-light tutorial.
