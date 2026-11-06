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

## Hobby and smart servos package the integration

A conventional positional hobby servo usually packages a small motor, reduction gears, an output-position sensor, and control electronics. Your command requests a position within its supported range. A continuous-rotation variant may interpret a similar command as speed or direction instead; the connector alone does not identify the behavior. Read the actual product's operating modes before designing a joint around it.

A smart servo adds a communication interface and may expose measured position, current, temperature, faults, and several control modes. For example, the [ROBOTIS XM430 manual](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/) documents current, velocity, position, and current-based position modes. It also distinguishes momentary stall torque from real operating performance. That makes the manual useful for learning what a complete actuator specification should contain; it is not a selection of that servo for our arm.

An integrated package can accelerate learning about mechanisms because you spend less time assembling a control system. However, inspect its output bearing capacity, mounting pattern, electrical interface, and behavior after communication loss. A servo horn transmits torque; its existence does not establish that the shaft can carry an arbitrarily long cantilever. A current limit can limit motor effort, but friction and gear losses prevent treating it as a perfectly calibrated contact-force limit.

## Stepper: count commands, then check whether motion followed

A stepper's magnetic geometry creates a sequence of preferred rotor angles. The driver advances the magnetic field, and the rotor follows if available torque can overcome load and acceleration. In an open-loop system, counting commands estimates position; it does not measure missed motion. A closed-loop stepper adds feedback, but still has finite torque and speed.

Holding torque describes a stationary energized condition. Moving torque depends on the motor, driver, supply, winding current, and speed. Inductance limits how rapidly winding current changes; at higher stepping rates the current may not reach the intended value. A **current-regulated driver** switches its supply to regulate phase current. Set that current according to both motor and driver documentation; supply voltage and winding current are separate specifications.

Use the actual motor-and-driver **pullout curve**, the boundary beyond which synchronous motion cannot be maintained under the stated test conditions. Being below it is necessary, but startup, acceleration, resonance, and thermal limits still require margin. Oriental Motor's [curve-reading guide](https://www.orientalmotor.com/stepper-motors/technology/speed-torque-curves-for-stepper-motors.html) identifies the driver, voltage, test load, holding torque, and pullout information you should look for. A curve for a different driver or voltage is not proof of your system's performance.

**Microstepping** uses intermediate phase-current combinations to make motion smoother. A 1.8° motor at 16 microsteps per full step has a commanded increment of `1.8 / 16 = 0.1125°`. Through our 3:1 belt, that corresponds to `0.0375°` at the output. This is command resolution, not a measured accuracy claim. Friction, load, current errors, and motor geometry affect where the rotor actually settles. TI's [microstepping application note](https://www.ti.com/lit/an/sloa293a/sloa293a.pdf) explains why the incremental torque from one small command can be too small to cause immediate motion. This does not mean the motor's entire torque capacity falls by the microstep divisor.

Steppers suit many positioning stages when the required torque remains available over the complete speed profile. For a mobile robot joint, also consider the energy spent holding position, motor mass carried by other joints, and what happens if synchronization is lost.

## Brushless motors and field-oriented control

Permanent-magnet brushless motors move commutation into electronics. Product language often distinguishes BLDC motors associated with trapezoidal commutation from PMSMs associated with sinusoidal excitation; examine the winding, back-EMF shape, sensor, and supported drive rather than assuming the label determines everything. **Field-oriented control**, or FOC, regulates current components relative to the rotor's magnetic orientation, giving a useful way to command torque. It requires a sufficiently accurate rotor-angle measurement or estimate. [Microchip's motor-control resources](https://www.microchip.com/en-us/solutions/technologies/motor-control-and-drive/motor-control-algorithms) distinguish these control approaches and their implementations.

A sensorless fan controller and a robot-joint drive have different jobs. The joint may need controlled torque at rest, slow reversal, and recovery after an external push. Some sensorless methods need a startup alignment and acceleration sequence; others use specialized low-speed estimation. TI's [sensorless startup documentation](https://software-dl.ti.com/mcu-sdk/esd/AM13E2X-SDK/26_01_00_03/exports/docs/docs/am13e230x/user_guide/chapters/solutions/am13e230x/motor_control/control_start_sequence.html) makes that sequence explicit. Verify the selected controller's zero-speed behavior rather than assuming “FOC” guarantees it.

A direct-drive joint connects the motor to the load without reduction. A quasi-direct-drive joint uses a relatively small reduction with a motor capable of substantial torque. Both can reduce transmission friction and reflected rotor inertia compared with high reduction, but they demand enough motor torque and heat rejection. The [Berkeley Blue research paper](https://arxiv.org/abs/1904.03815) shows this design trade in an actual research robot. Its results belong to that robot; they do not certify a smaller printed version.

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
