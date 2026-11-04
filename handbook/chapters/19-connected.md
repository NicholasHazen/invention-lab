# 19. Connected devices: make communication failure an ordinary condition

A bench logger becomes more useful when its measurements reach a laptop. A positioning rig becomes more complicated when commands arrive over a network. Messages can be late, repeated, lost, malformed, or sent by the wrong device. Designing only for the successful exchange leaves the most consequential behavior unspecified.

This chapter connects the sensor/logger to a larger system while keeping the behavior understandable. You will distinguish board-level buses from network protocols, calculate a realistic serial data budget, and replay duplicate and stale commands through a small receiver. The lab requires the software/data chapter and Python 3; it opens no network connection and controls no hardware. Familiarity with digital voltage levels helps with the optional physical interfaces.

## “Serial” describes an arrangement, not one universal connector

Serial communication sends bits over time rather than placing every bit on a separate wire. UART, I²C, and SPI are all serial interfaces, but they differ in timing, addressing, wiring, and electrical assumptions. A USB connector does not imply that the signals on its pins are ordinary microcontroller UART signals. A USB-to-UART adapter translates between different interfaces.

| Interface | How devices coordinate | A useful first application | What to check first |
| --- | --- | --- | --- |
| UART | Sender and receiver agree on bit timing and frame format; no shared clock line | Text logs between a board and laptop adapter | Voltage compatibility, transmit/receive wiring, baud rate, data bits and parity |
| I²C | A controller supplies a clock; addressed devices share data and clock lines | Several low-rate sensors on a short local bus | Addresses, pull-ups, voltage limits, bus capacitance and device timing |
| SPI | A clock and device-select signal coordinate shifting data | A display, converter, or memory needing direct transfers | Clock polarity/phase, bit order, select timing and maximum clock rate |

For UART, both ends must agree closely enough on timing for the selected devices and frame length. A peripheral data sheet specifies the tolerances; a label such as “serial” does not. [Microchip's UART overview](https://www.microchip.com/en-us/products/microcontrollers/8-bit-mcus/peripherals/communication-connectivity/uart) is an entry point to device-specific documentation.

Typical I²C lines are pulled high and devices actively pull them low, allowing a shared bus. Pull-up resistance and capacitance affect how quickly a released line rises. Adding boards and long wires can therefore break timing even when the addresses are correct. [NXP's I²C specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) documents the electrical and protocol requirements. SPI uses different signaling and selection conventions; its device data sheet remains decisive for the supported mode and timing. See the [Microchip SPI overview](https://www.microchip.com/en-us/products/microcontrollers/8-bit-mcus/peripherals/communication-connectivity/spi) for the basic signal roles.

Before connecting boards, verify their logic voltage limits and reference arrangement with power removed. A 5 V output may damage a 3.3 V-only input. Do not infer compatibility from a connector fitting. Bare logic-level buses also are not automatically suitable for long external cables; interfaces such as RS-485 use additional electrical transceivers for different wiring conditions.

## Work out whether the bytes can fit

Suppose a UART link runs at 115,200 bits per second using eight data bits, no parity, and one stop bit, often written 8N1. A usual frame also has one start bit, so each data byte occupies ten transmitted bits. The theoretical data capacity is therefore `115,200 / 10 = 11,520 bytes/s`, before application pauses and other overhead.

If each logger record is 80 bytes including its line ending and the logger produces 50 records per second, the stream needs `80 × 50 = 4,000 bytes/s`, about 35% of that capacity. If an expanded JSON record reaches 180 bytes at 100 records per second, it needs 18,000 bytes/s and cannot fit. A growing output buffer may initially hide the mismatch, then create long delays or lost data.

Measure complete encoded records, including timestamps, field names, separators, and line endings. Leave room for bursts, diagnostic messages, and device processing. If logging blocks a time-sensitive control loop, separate acquisition from transmission with a bounded buffer and a documented overflow policy. Dropping an old telemetry sample with a gap counter can be preferable to silently delaying the controller; the correct policy depends on the experiment.

## Separate the transport from the meaning

A transport delivers bytes. An application protocol defines what those bytes mean. A useful telemetry record includes a schema version, device identifier, boot/session identifier, sequence number, measurement time, unit, value, and quality status. Not every project needs every field in every packet, but every ambiguity needs a resolution somewhere in the interface contract.

For example, `distance_mm: 20` is clearer than `value: 20`, while `raw_count: 500` preserves information needed for future calibration. A sequence number reveals gaps and duplicates within a session. A boot identifier distinguishes a legitimate sequence restart from an old packet arriving late. A timestamp supports age checks only when the receiver understands the clock and its uncertainty.

Frame the stream so that a receiver can recover after a damaged record. Newline-delimited JSON is convenient for small human-readable logs: read a bounded line, parse one record, validate its schema and ranges, then accept or reject it. Limit message size and parsing work. A syntactically valid document can still contain an impossible value, unsupported version, or unauthorized request.

Distinguish a received command from an applied command. A transport acknowledgment confirms a protocol event, not that a mechanism reached its target. The device should separately report accepted, rejected, executing, and completed states as appropriate, with the command identifier attached. This prevents a user interface from displaying success merely because a packet was sent.

## HTTP and MQTT organize communication differently

HTTP is a request-and-response application protocol. It suits reading a device status resource, downloading a log, or submitting a bounded configuration change. Use method semantics intentionally: reading a status should not secretly start motion. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines the common HTTP semantics, including safe and idempotent methods; an endpoint's implementation still has to honor those meanings.

MQTT uses a broker to route published messages to interested subscribers. A logger can publish measurements while a dashboard and archive subscribe independently. Topics provide routing, not a complete data schema or authorization policy. The [OASIS MQTT 5 specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) defines delivery levels: QoS 0 can lose messages, QoS 1 permits duplicates, and QoS 2 provides an exactly-once protocol delivery mechanism. None alone proves that a physical action completed exactly once across application crashes and restarts.

A repeated “toggle” command reverses the result again. A repeated “set indicator off” command has the same intended state, making it idempotent. Desired-state commands are often easier to recover than incremental instructions, although motion still needs explicit limits, identity, and state checks. Retained messages require particular care: a new subscriber may receive an old stored value. That is useful for a configuration snapshot and potentially inappropriate for an unqualified motion command.

Keep the first network extension local and observable. [Eclipse Mosquitto's documentation](https://mosquitto.org/documentation/) provides broker, client, authentication, and configuration references. Before allowing access beyond the development machine, configure authentication and permissions deliberately; do not assume a working demonstration has appropriate network exposure.

## Replay failure cases without a network

Download [message_lab.py](../examples/computing/message_lab.py) and run:

```sh
python3 message_lab.py
```

The receiver begins in an off state. A fresh command with sequence 1 turns the simulated state on. Repeating sequence 1 is rejected as duplicate; sequence 0 is rejected as old. A command sent at time 0 but delivered at time 3 is rejected as expired. By then the two-second timeout has already put the state off. A fresh explicit off command is accepted, and the final timeout leaves it off.

The lab's rule accepts only supported schema version 1, nonnegative integer sequences, states `on` or `off`, and timestamps no more than one second old. Accepted commands refresh a local watchdog time; rejected duplicates do not. This prevents a repeated old packet from making the receiver believe that the sender is still providing fresh instructions.

Read `tick()` separately from `receive()`. A timeout must run even when no messages arrive. A design that checks for silence only inside a message handler cannot notice total silence. In a real device, use an appropriate monotonic local clock for elapsed watchdog time. The lab uses one simulated clock for sender and receiver; it does not solve clock synchronization or authentication.

Run the [shared test suite](../examples/computing/test_labs.py) using the [example instructions](../examples/computing/README.md). Its checks include duplicate handling, expiry, out-of-order delivery, and the fact that a duplicate cannot refresh the watchdog. These are verified software policies for an in-memory example. The selected timeout is a teaching value, not a derived safe stopping interval for a mechanism.

Change the timeout to 0.5 seconds and trace the same events on paper before running them. Then add an event with a new sequence but an old timestamp. A sequence number alone does not establish freshness. Finally, consider a reboot: the in-memory sequence history disappears. A deployable policy must address sessions, persistence, and whether old commands can be replayed after a restart.

## Security is part of the device's behavior

Authentication answers which identity is connecting; authorization answers what that identity may do. A dashboard that can read temperature does not necessarily need permission to change calibration or command an actuator. Give devices distinct credentials, limit topic or endpoint permissions, and keep secrets out of public repositories and logs. Encrypt network traffic where required and verify the server identity; encryption without identity checking can protect a conversation with the wrong endpoint.

Plan how a device receives trusted software updates, reports its version, and recovers from an interrupted update. A checksum detects accidental corruption but does not establish who authorized an image. A signed update needs a protected trust decision and a recovery design. Keep a known working recovery route and test it on the development device before relying on remote maintenance.

[NISTIR 8259A](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8259A.pdf) is a useful requirements lens: device identification, configuration, data protection, interface access, software updates, and awareness of security state. Reading it does not certify a hobby build. Use it to turn vague intentions into questions you can answer about your specific device and its expected environment.

Security and functional limits complement each other. An authenticated command can still be mistaken or unsafe. Keep physical operating limits, stale-data handling, and stop behavior inside the local deterministic system. Loss of a cloud dashboard should not remove the device's ability to enforce its own constraints.

## Keep the experiment useful when disconnected

A local-first logger records essential data locally and treats upload as a separate task. Use a bounded queue and decide what happens when storage fills. Preserve sequence gaps and status flags rather than making a continuous-looking graph from incomplete data. When connectivity returns, upload with record identities so the server can recognize duplicates.

Separate “device online” from “measurement fresh.” A connected device may be publishing an old cached value. Show the measurement age, quality, and device state alongside the number. Logs should explain rejected commands, restarts, configuration changes, and dropped records without revealing credentials. A bounded, rotating log prevents diagnosis itself from exhausting the device's storage.

When a link fails, diagnose in layers: power and voltage, signal wiring and timing, byte framing, message schema, authentication, then application state. Garbled UART text suggests different causes from well-formed messages rejected for an expired timestamp. A known small message and a loopback or vendor-supported interface test often isolate the layer faster than rewriting the application.

## Check, then design the next connection

**Predict:** Why might QoS 1 break a toggle command? **Answer:** Duplicate delivery can toggle twice. A command identifier and idempotent desired-state behavior make retries easier to handle.

**Predict:** Does a successful network reply prove the mechanism reached its destination? **Answer:** No. Receipt, acceptance, execution, and verified completion are separate events.

**Predict:** Why does the receiver need a timeout routine independent of incoming messages? **Answer:** Total silence produces no message callback, so only a separately scheduled check can detect it.

For an independent project, extend the simulated logger with a bounded offline queue and an upload function that deliberately fails on selected attempts. Give each record a device/session/sequence identity. Demonstrate recovery without duplicate archive entries, document which records are dropped if the queue fills, and show the user how old the newest measurement is. Complete that behavior before adding a real broker or remote actuator; the network then becomes a transport for a policy you can already explain and test.
