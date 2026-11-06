# Make the actuator report what the mechanism actually does

Imagine the motor encoder reports exactly the requested angle while the arm tip sits a millimeter low. The controller may be doing its job perfectly: it controls the measurement it receives. A loose hub, stretched belt, or bending bracket can move the load without producing the same motion at the motor. Before tuning gains, decide which physical quantity the system needs to regulate and where that quantity can be observed.

This chapter assumes you have worked through [sizing](#chapter-04) and can identify the motor, transmission, and output support in one of the three layouts. You need paper and a calculator; no powered mechanism is required. You will sketch feedback locations, trace a limited command through nested control loops, and define what happens when a sensor, command stream, or power source disappears.

## Put the measurement beside the question

A motor encoder measures motor rotation. Dividing that rotation by the 3:1 ratio estimates output rotation under an assumption: the transmission preserves the geometric relationship. A load encoder on the output shaft observes errors that break that assumption. Neither encoder directly measures the flexible arm's tip position. If the task is accurate contact with an object, the sensor boundary may need to extend farther still.

![A motor encoder measures before the compliant transmission; a load encoder measures after it. Position, velocity, and current loops have different measured quantities.](assets/sizing-feedback-path.svg)

Suppose an encoder provides **4096 decoded counts per motor revolution**. “Decoded” matters because vendors may quote pulses before or counts after quadrature decoding. One motor count corresponds ideally to 360/(4096 × 3) = **0.029296875° at the output**, or about **0.0511 mm of arc travel at a 100 mm tip radius**. Those are quantization steps. They are not a claim that the tip is accurate to 0.0511 mm.

Resolution describes distinguishable steps; accuracy concerns closeness to the true position; repeatability concerns returning to the same result. [Renishaw's encoder FAQ](https://www.renishaw.com/en/optical-encoders-frequently-asked-questions--34674) distinguishes these properties. An eccentric encoder magnet, a shifting bracket, and a stable calibration offset have different effects, even if the displayed number has many decimal places.

For the screw stage, a motor encoder cannot see axial coupling slip, nut backlash, or carriage compliance. A linear scale on the carriage can. For the tendon finger, spool angle does not uniquely determine fingertip force: tendon stretch, routing friction, return spring torque, and contact location intervene. A tension sensor measures one internal force, while a calibrated elastic element measures force through its deflection. Neither automatically determines every force at a multi-contact fingertip.

Motor and load sensors can serve different loops. A brushless drive may need rotor position for commutation while using output position for the task. Dual feedback introduces a dynamic problem: compliance separates the motion seen by the two sensors. ODrive's [dual-encoder documentation](https://docs.odriverobotics.com/v/latest/manual/hardware-config.html#dual-encoder) specifically warns that load-side velocity feedback across compliance or backlash can produce oscillation. Adding a sensor is not a substitute for checking the loop design.

## Follow a command inward

A common servo structure nests three loops. Position error asks for velocity; velocity error asks for torque; a current loop adjusts electrical drive to obtain the requested motor current. Inner loops must respond appropriately before the outer loops depend on them. Some drives combine or modify these stages, so inspect the actual product rather than assuming every “servo” has identical internals. ODrive documents one concrete [cascaded controller structure](https://docs.odriverobotics.com/v/latest/manual/control.html).

The important distinction is between a requested value and an achieved value. A position loop can request movement faster than the mechanism permits. A velocity loop can request torque above the current limit. A current loop can run out of available voltage at speed. Software should preserve those facts in telemetry rather than presenting a setpoint as a measurement.

A proportional correction increases effort with error. An integral term accumulates persistent error and can counter steady disturbances, but can also accumulate while the actuator is saturated. Anti-windup means handling that saturation so stored integral action does not keep demanding impossible effort. A feedforward term estimates predictable demand, such as gravity, before error develops. Feedback still corrects the imperfect estimate.

## Trace one limited command on paper

Use this deliberately simplified controller thought experiment. All position and velocity quantities below refer to the **output shaft**; the torque request refers to the **motor shaft**. This declaration avoids accidentally applying the ratio twice. The gains are teaching values, not tuning instructions for a real drive.

The arm is measured at 45°, its commanded position is 50°, and its measured output speed is +5°/s. Choose a position gain of 4/s. The 5° error requests +20°/s. Now apply an illustrative +10°/s velocity limit before calculating the velocity error: the error entering the next stage is +5°/s, or 0.0872665 rad/s.

Choose a velocity proportional gain of 0.1 N·m per rad/s, expressed as motor torque per output angular speed. Its correction is **0.00872665 N·m**. With an ideal transmission, gravity feedforward at 45° is 0.28449 × cos(45°)/3 = **0.06705494 N·m**. Their sum is about **0.0757816 N·m**. This paper trace omits integration, acceleration feedforward, friction, and transmission loss so the command path stays visible.

With the hypothetical matched torque constant K_t = 0.020 N·m/A, that request needs **3.78908 A** of torque-producing current. If the illustrative current limit is 3 A, the motor can request at most **0.060 N·m** under this model. Position will lag because even the ideal gravity feedforward exceeds the available torque. Raising the position gain does not create the missing current.

Predict which of three changes can remove this particular saturation: increasing encoder resolution, reducing payload, or increasing position gain. Reducing payload lowers gravity demand. More encoder counts do not supply torque, and higher gain can increase the saturated demand. A different reduction might help, but must be checked against speed, rotor inertia, and transmission limits using the sizing chapter.

## An ampere needs a definition

The relation torque = K_t × current is useful only when both quantities use the same convention. A brushed motor's armature current, a sinusoidal phase's RMS current, its peak current, and a field-oriented controller's q-axis current can have different numerical values. Do not insert an unexplained square-root-of-two conversion: waveform, motor connection, and transform normalization matter.

For example, ODrive's [API reference](https://docs.odriverobotics.com/v/latest/fibre_types/com_odriverobotics_ODrive.html) defines a motor torque constant and exposes q-axis current information. That is a reason to read the selected drive's definitions, not a universal calibration rule. Record the motor datasheet's convention beside the drive's current-limit convention before translating a torque requirement.

The DC supply current belongs to another measurement boundary. PWM switching, motor voltage, losses, and stored energy separate it from winding current. At a stationary hold the mechanical power τω is zero while the windings can still dissipate heat. At speed, voltage headroom also matters because back EMF and resistive/inductive voltage demands must fit the drive and supply. A current-capable driver therefore does not guarantee the required torque at every speed.

## Give returning energy somewhere to go

Lowering the arm can send energy back through the motor. If all of the study's 0.28449 J gravitational potential change reached an illustrative 1000 µF DC bus capacitor initially at 12 V, its voltage would rise to √(12² + 2 × 0.28449/0.001) = **26.7017 V**. This intentionally lossless energy calculation is not a component design, but it shows why a small load can matter to an electrical bus.

A current-limited bench supply is not necessarily able to absorb reverse current. The actual drive may require a compatible regenerative supply, a manufacturer-supported braking resistor arrangement, or a rated clamp. Inspect voltage, peak energy, repetitive power, thermal mounting, and fault behavior together. The [ODrive Regen Clamp datasheet](https://docs.odriverobotics.com/v/latest/hardware/regen-clamp-datasheet.html) is a concrete example of a device that routes regenerated energy to an external resistor; its specifications apply to that product, not every controller.

## Define the states before enabling the drive

Draw five boxes: **disabled**, **ready**, **moving**, **controlled stop**, and **fault**. Disabled means no commanded motor torque; ready means the reference, limits, and sensors are valid. Moving requires an explicit bounded command. A controlled stop uses a validated deceleration path while enough power and feedback remain available. A fault prevents automatic restart until the cause is reviewed.

Next write the physical outcome beside each transition. If command communication expires, can the drive decelerate within the remaining travel? If encoder feedback becomes invalid, closed-loop deceleration may no longer be trustworthy. If power disappears, active holding torque disappears too. A gravity-loaded arm therefore needs a planned catch, rest, counterbalance, or appropriately rated holding arrangement. A holding brake must not be assumed suitable for repeated dynamic stops.

These boxes are a design exercise, not a safety-certified architecture. Before powered testing, use the selected drive's documented disable and fault behavior and provide a physical arrangement that contains motion when electronics cannot. Do not test a fault by unplugging motor or encoder connectors under power. [The bench chapter](#chapter-10) develops controlled, supported checks.

For an independent exercise, redraw the feedback diagram for the screw stage with both a motor encoder and a carriage scale. Mark the sensor that detects each of three faults: loose coupling, nut backlash, and bending guide mount. If none measures the actual error that matters to your task, change the measurement location before changing gains.
