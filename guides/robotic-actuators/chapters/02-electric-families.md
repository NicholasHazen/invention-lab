# Electric actuators: choose what the whole system can do

A servo listing promises a large torque. A stepper promises thousands of positions per revolution. A brushless motor promises an impressive power rating. Which one can lift our 250 g payload, pause with the arm horizontal, and move again without overheating? None of those headline numbers answers the question. We need to know where the number was measured, under which conditions, and how the device responds when its load changes.

Bring the output requirements from [chapter 1](#chapter-01) and a calculator. By the end, you will be able to separate motor technology from feedback and gearing, reject an unsuitable specification, and identify the missing evidence needed before buying a candidate. This chapter uses paper calculations and datasheets; it does not require powering a motor.

## Three decisions hiding inside one product name

A **motor** converts electrical energy into mechanical motion. A **transmission** changes the relationship between motor motion and load motion. A **servo system** measures something, compares it with a command, and adjusts drive effort to reduce the difference. A brushed motor with an encoder and controller can form a servo. So can a brushless motor or a stepper. A gearmotor includes a transmission, but it need not include position feedback.

![Three independent actuator choices: motor technology, transmission, and control. A servo can combine several different motor and transmission types.](assets/families-system.svg)

The sensor's location matters. A motor encoder can report that the motor reached its target while a loose hub, flexible belt, or gearbox clearance lets the output differ. An output encoder observes those downstream effects, although observing them does not make the structure infinitely stiff. Keep the power path, measurement path, and support structure separate in your sketch. That habit will make later control problems much easier to diagnose.

Our arm needs approximately 0.284 N·m to remain horizontal. Its planned 90° move in one second reaches 30 rpm at the output. These are different requirements: a brief move and a sustained hold can stress the same actuator differently. [Chapter 4](#chapter-04) develops their complete sizing calculation.

## Brushed DC: current produces torque, speed changes current

In a brushed DC motor, mechanical contacts switch winding connections as the rotor turns. For a first model, torque increases with winding current. Rotation also generates a voltage opposing the supply, called **back EMF**. At a fixed applied voltage, faster rotation leaves less voltage available to push current through winding resistance. That connection explains the familiar falling torque–speed line. Maxon's [motor-data explanation](https://support.maxongroup.com/hc/en-us/articles/360013761160-Motor-data-and-simulation) shows both the useful approximation and cases where a straight line becomes inaccurate.

A gearmotor combines this motor with reduction. You gain output torque and lose output speed, while adding gearbox losses, clearance, and limits. Check whether a specification describes the bare motor or the gearbox output. Then check gearbox maximum torque separately: increasing motor current cannot strengthen gear teeth.

At zero speed, back EMF disappears. Applying full voltage can therefore draw a large current even though useful mechanical power, `torque × speed`, is zero. That electrical input becomes heat and other losses. Startup, sudden reversal, and a blocked output all deserve attention in driver selection. [Pololu's motor and supply guide](https://www.pololu.com/docs/0J73/4.1) distinguishes starting/stall current from free-running current and explains why prolonged stall can damage a motor.

This family is approachable for a first custom mechanism because motor, driver, encoder, and transmission remain visible design choices. The price of that flexibility is integration work: a two-wire motor does not know its angle. A reversible driver supplies power; a controller and suitable feedback create controlled positioning.

## Servo systems: compare the package and the feedback

“Buy a servo” leaves several choices unresolved. A small RC servo, a networked robot servo, and an industrial motor-and-drive pair can all use feedback, yet they expose very different capabilities to you. Start with the action you need: reach an angle, maintain a speed, or regulate effort. Then ask which parts of that job the purchased package actually performs.

![A functional position-servo loop separates command information, electrical power, mechanical motion, and measured output position. Four package examples compare hobby, smart bus, industrial, and integrated robot-joint servos.](assets/servo-system-options.svg)

*Trace the return arrow from the measured angle. The controller can correct an error only if its measurement exposes that error. Then compare the package boundaries below: putting the loop inside a box reduces your integration work, but does not guarantee that the box reports its measurements to your computer.*

| Servo option | Where it helps | Main compromise | Decisive checks |
| --- | --- | --- | --- |
| Hobby positional servo | A small joint, pointer, or linkage that needs bounded angle motion | Convenient package; often little telemetry or published continuous-load data | Angle range, sustained holding, supply current, gear play, horn and bearing loads |
| Continuous-rotation RC servo | Simple wheel or roller drive using an RC-style command | Common versions command direction and speed without measuring output angle | Presence of feedback, speed variation with load, neutral calibration |
| Smart bus servo | Several robot joints with addressed commands and status reporting | More observability; protocol, modes, and power distribution need setup | Sensor location, supported modes, bus timing, watchdog, temperature limits |
| Industrial servo motor + drive | Repeated precise motion with documented drive integration | Greater commissioning, cabling, tuning, and mounting work | Matched motor/drive/feedback, continuous torque–speed envelope, inertia, regeneration |
| Integrated robot joint | Compact rotary joint with motor, reducer, sensing, and drive packaged together | Convenient interfaces constrain ratio, geometry, cooling, and repair | Exactly what is integrated, output-load ratings, usable control modes, peak duration |

These are overlapping product arrangements. A smart servo may contain a brushless motor; an industrial servo may use a harmonic reducer; an integrated robot joint may use a modest-ratio planetary stage. The word **servo** tells us to look for a control loop, not a particular gear or motor shape.

### Hobby positional servos

A conventional positional hobby servo packages a small motor, reduction gears, an output-position sensor, and control electronics. It compares the commanded angle with its local measurement and drives the motor to reduce the difference. That makes it useful for a first linkage: the basic feedback loop arrives assembled. The usual tradeoffs are limited travel, gear clearance, and restricted access to measurements and tuning.

The signal wire carries a **pulse-width command**; the power wires supply the energy that moves the load. This command is different from the high-frequency motor-power PWM used inside a drive. Many RC interfaces use a neutral pulse near 1.5 ms, but allowable widths, update rate, angle range, and direction must come from the actual servo. A three-wire non-isolated interface uses its ground as the signal reference; a separate power supply still needs the documented common reference. This is not a wiring rule for isolated industrial drives or every serial bus. [Pololu explains the power and signal roles](https://www.pololu.com/blog/16/electrical-characteristics-of-servos-and-introduction-to-the-servo-control-interface).

A “digital” hobby servo can still use that same pulse interface: digital describes its internal control implementation, not a promise of serial commands or returned position. Likewise, a controller reporting the pulse it sent is not measuring the servo shaft. Calibration matters because a library's requested “90°” is only as good as its pulse-to-angle mapping. [Pololu's detailed interface discussion](https://www.pololu.com/blog/17/servo-control-interface-in-detail) shows why there is no universal mapping.

A servo horn transmits torque. It does not establish that the output bearing can support a long cantilever. For our pivot, retain the separate bearing-supported shaft and connect the actuator through a torque-transmitting interface. Also separate the short-duration stall number from the sustained horizontal holding requirement; a compact package can overheat while it appears to be doing nothing.

### Continuous-rotation servos

Many continuous-rotation RC servos replace angle positioning with a command for direction and speed. A neutral command asks for a stop; commanding for one second does not establish a repeatable angle because voltage, friction, and load affect travel. This is useful for a wheel, but insufficient by itself for a joint that must return to a specified angle.

The name has exceptions. Some products provide a separate feedback signal, and some smart servos support both multi-turn positioning and velocity modes. Check what is measured and what the host must implement. [Pololu's continuous-rotation comparison](https://www.pololu.com/category/143/continuous-rotation-servos) distinguishes ordinary open-loop versions from feedback-equipped examples. “360°” on a listing is therefore a prompt to read the control description, not proof of arbitrary-angle positioning.

### Smart bus servos

A smart bus servo accepts addressed messages and can return status. That can simplify a robot with several joints: the host can request motion and inspect the measured response. Depending on the model, available data may include position, current, supply voltage, temperature, and faults. The [ROBOTIS XM430 manual](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/) provides a concrete example with position, velocity, current, and current-based position modes, plus a configurable communication watchdog.

Those features make experiments more informative, but each needs interpretation. Motor current is an effort-related measurement, not a direct measurement of contact force after gears, friction, and linkage geometry. Read whether position is motor-side or output-side, and what happens to multi-turn counts after power loss. Verify the electrical bus variant, adapter, identifiers, and supported update rates; a familiar connector does not establish compatibility. The servo supply must still carry the combined load current of the joints.

For an early actuated pivot, this package is worth investigating when logging position and temperature matters more than minimizing purchase cost. Its continuous load capacity and output support still need to pass the same mechanical checks as any other option.

### Industrial servo motor and drive

Here the “servo motor” is commonly a motor with a feedback device; the compatible servo drive is another component. The drive regulates motor current and can participate in velocity and position loops. A higher-level controller provides motion commands. This arrangement offers flexibility for repeated machine motion, but you must integrate the drive, feedback interface, power, cables, mounting, and tuning. [Kollmorgen's system overview](https://webhelp.kollmorgen.com/s300_S700/EN/overview_servo_drives.htm) shows those separate roles.

Motor-side feedback can confirm motor angle while a transmission twists or takes up clearance. An output encoder measures farther along the mechanism; some drives support both sensors. Adding that measurement changes the control problem, because the flexible transmission remains between motor and load. Rockwell's [motor, auxiliary, and dual-feedback diagrams](https://www.rockwellautomation.com/en-us/docs/studio-5000-logix-designer/37-00/contents-ditamap/instruction-set/axis_servo_drive-diagrams.html) make the different loops explicit.

Choose this arrangement when its flexibility and documented integration are useful enough to justify the setup. Read continuous and peak ratings at the required speed and cooling condition. Check how braking energy is handled, whether a holding brake is supplied, and how the supported axis behaves when the drive is disabled. These are system design questions; a position-control mode alone does not answer them.

## Stepper: count commands, then check whether motion followed

A stepper's magnetic geometry creates a sequence of preferred rotor angles. The driver advances the magnetic field, and the rotor follows if available torque can overcome load and acceleration. In an open-loop system, counting commands estimates position; it does not measure missed motion. A closed-loop stepper adds feedback, but still has finite torque and speed.

Holding torque describes a stationary energized condition. Moving torque depends on the motor, driver, supply, winding current, and speed. Inductance limits how rapidly winding current changes; at higher stepping rates the current may not reach the intended value. A **current-regulated driver** switches its supply to regulate phase current. Set that current according to both motor and driver documentation; supply voltage and winding current are separate specifications.

Use the actual motor-and-driver **pullout curve**, the boundary beyond which synchronous motion cannot be maintained under the stated test conditions. Being below it is necessary, but startup, acceleration, resonance, and thermal limits still require margin. Oriental Motor's [curve-reading guide](https://www.orientalmotor.com/stepper-motors/technology/speed-torque-curves-for-stepper-motors.html) identifies the driver, voltage, test load, holding torque, and pullout information you should look for. A curve for a different driver or voltage is not proof of your system's performance.

**Microstepping** uses intermediate phase-current combinations to make motion smoother. A 1.8° motor at 16 microsteps per full step has a commanded increment of `1.8 / 16 = 0.1125°`. Through our 3:1 belt, that corresponds to `0.0375°` at the output. This is command resolution, not a measured accuracy claim. Friction, load, current errors, and motor geometry affect where the rotor actually settles. TI's [microstepping application note](https://www.ti.com/lit/an/sloa293a/sloa293a.pdf) explains why the incremental torque from one small command can be too small to cause immediate motion. This does not mean the motor's entire torque capacity falls by the microstep divisor.

Steppers suit many positioning stages when the required torque remains available over the complete speed profile. For a mobile robot joint, also consider the energy spent holding position, motor mass carried by other joints, and what happens if synchronization is lost.

## Brushless motors and field-oriented control

Permanent-magnet brushless motors move commutation into electronics. Product language often distinguishes BLDC motors associated with trapezoidal commutation from PMSMs associated with sinusoidal excitation; examine the winding, back-EMF shape, sensor, and supported drive rather than assuming the label determines everything. **Field-oriented control**, or FOC, regulates current components relative to the rotor's magnetic orientation, giving a useful way to command torque. It requires a sufficiently accurate rotor-angle measurement or estimate. [Microchip's motor-control resources](https://www.microchip.com/en-us/solutions/technologies/motor-control-and-drive/motor-control-algorithms) distinguish these control approaches and their implementations.

A sensorless fan controller and a robot-joint drive have different jobs. The joint may need controlled torque at rest, slow reversal, and recovery after an external push. Some sensorless methods need a startup alignment and acceleration sequence; others use specialized low-speed estimation. TI's [sensorless startup documentation](https://software-dl.ti.com/mcu-sdk/esd/AM13E2X-SDK/26_01_00_03/exports/docs/docs/am13e230x/user_guide/chapters/solutions/am13e230x/motor_control/control_start_sequence.html) makes that sequence explicit. Verify the selected controller's zero-speed behavior rather than assuming “FOC” guarantees it.

## Integrated robot joints and quasi-direct drive

An integrated robot joint packages some combination of a brushless motor, reduction, encoder, driver, bearings, and sometimes a brake. Integration describes the package; it does not identify the transmission. The [CubeMars AK80-9 example](https://www.cubemars.com/product/ak80-9-v3-0-robotic-actuator.html) combines a brushless motor, planetary reducer, encoder, and drive. Other joint modules use strain-wave or cycloidal reducers. Compare the complete assembly drawing and specification rather than assuming every module includes an output bearing or sensor with the same capabilities.

A **direct-drive** joint connects the motor to the load without reduction. A **quasi-direct-drive (QDD)** joint uses modest reduction and a motor that supplies substantial torque. Lower reduction can improve backdrivability and reduce the motor's reflected inertia for a given rotor, which is attractive when a joint should yield to a push. The cost is that the motor must supply more torque, and sustained holding still produces heat. “QDD” does not guarantee low friction, effortless backdriving, or safe contact. Motor size, cogging, gearing, control, and the complete mechanism determine the behavior. The [Berkeley Blue paper](https://arxiv.org/abs/1904.03815) explores this trade in a research robot; its measured results do not rate our printed pivot.

A **frameless torque motor** is another packaging choice: a rotor and stator supplied for integration into your mechanism. This can create a compact coaxial joint, but transfers bearing support, air-gap alignment, housing, thermal paths, and feedback integration to the designer. [Kollmorgen's frameless explanation](https://www.kollmorgen.com/en-us/products/motors/technologies-explained/what-is-a-frameless-motor) distinguishes the motor kit from a complete housed assembly. A printed housing is a useful geometry experiment; it does not inherit the performance of a thermally conductive, accurately aligned metal installation.

For our first powered pivot, compare two complete candidates: a supported output driven by a positional or smart servo, and a supported output driven through our visible belt study. Keep a compact integrated joint as a third option if packaging becomes decisive. A raw frameless motor is a later integration project unless its extra mechanical and control work is the subject you want to learn.

## A candidate that passes one check and fails another

Consider an invented DC gearmotor whose gearbox-output data at one supply voltage are 500 rpm no-load speed, 0.200 N·m stall torque, and a 0.060 N·m continuous limit under stated cooling conditions. Treat its output as the input to our additional 3:1 belt. These are teaching values, not a purchasable specification.

At 90 rpm, a linear torque–speed model predicts available torque of `0.200 × (1 − 90/500) = 0.164 N·m`. Our conservative moving-load bound of 0.312 N·m requires about `0.312 / (3 × 0.90) = 0.116 N·m` at this shaft, before its own acceleration and additional losses. The candidate clears that preliminary curve check.

For a conservative holding screen, give no credit to unmeasured static friction supporting the arm. The ideal torque balance then requires `0.28449 / 3 = 0.0948 N·m`, exceeding the invented 0.060 N·m continuous limit. The candidate fails this screen. Real static friction could reduce the motor torque needed, but that needs evidence rather than a favorable assumption. Applying a moving efficiency at zero speed cannot resolve the static balance. Rotor/gear inertia and duty-cycle information also remain necessary for final selection.

## Make a specification card before shopping

Predict first: will doubling microstep subdivision double usable positioning accuracy? Will a curve that passes at peak speed guarantee a cool horizontal hold?

1. Open the Oriental Motor curve guide and choose one displayed curve. Record its motor, driver, supply, current if given, and axis units. Mark missing information explicitly.
2. Read three speed–torque points. Record approximate values with reading uncertainty rather than inventing precision from a small graph.
3. Write a separate specification card for the invented gearmotor above. Keep curve capability, continuous torque, gearbox limits, sensor location, and power-loss behavior in separate fields.
4. Recalculate its curve torque at 180 rpm, then explain whether that change repairs its holding problem.

**Check:** the illustrative available torque becomes 0.128 N·m. Its continuous holding limit stays 0.060 N·m, so the hold still fails. Finer microsteps reduce command spacing; accuracy needs measurement. If your curve reading differs by a factor of 60 or `2π`, inspect rpm versus revolutions per second versus radians per second before changing the mechanical design.

For an independent variation, change the task to a vertical-axis turntable with the same inertia. Explain which gravity term disappears and which acceleration, friction, bearing, and thermal questions remain. That exercise should lead to a different candidate shortlist even though the payload mass is unchanged.
