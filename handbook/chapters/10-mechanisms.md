# Mechanisms and actuators: make the motion earn its motor

Imagine a small sensor on a tabletop arm. You want to turn it toward a target, hold it still while taking a reading, then return to a known position. A motor can provide rotation, but it does not decide how the arm is supported, how much it bends, or whether a command corresponds to the angle you actually obtain. Those questions belong to the whole mechanism.

This chapter turns a desired motion into a first transmission and actuator specification. You will calculate torque and speed, distinguish several causes of positioning error, and use a hand-operated experiment to test a load model. Bring the force, moment, and free-body-diagram ideas from the [mechanics chapter](../mechanics/). No electronics or motor purchase is needed for the core lab. The numbers here describe a separate teaching example; they do not establish an actuator rating for the untested [triangulated pivot](../../projects/triangulated-pivot/).

## Begin at the output

Describe what the load must do before choosing a motor. Our illustrative arm carries a 100 g sensor, with its center of mass 80 mm from a horizontal rotation axis. It must sweep through 90° in two seconds and stop. Write down the orientation: a vertical axis does not experience the same gravitational turning moment as a horizontal one. Also record travel limits, acceptable error, operating time, and what should happen when power disappears.

Mass is not force. A 0.100 kg sensor has weight approximately `0.100 × 9.81 = 0.981 N`. When the arm is horizontal, the perpendicular distance from the axis to the weight's line of action is 0.080 m. The gravitational torque is therefore:

`τ = F × r = 0.981 × 0.080 = 0.0785 N·m`

A newton metre, N·m, is force multiplied by perpendicular distance. If the arm turns upward, that perpendicular distance shrinks. The worst gravitational case is the horizontal position, not every position. The arm's own weight, cable drag, friction, and acceleration add demands that this first calculation omits. Add them as identifiable terms; a large unexplained multiplier hides what you still need to measure.

For example, a uniform 40 g arm extending 80 mm contributes another `0.040 × 9.81 × 0.040 = 0.0157 N·m` when horizontal. The combined static requirement becomes 0.0942 N·m. That is a holding requirement at one configuration. A mechanism intended to move quickly also needs torque to change its angular speed. Rotational inertia describes resistance to angular acceleration; mass farther from the axis contributes disproportionately. Moving the same sensor closer to the axis can reduce both gravity torque and acceleration demand.

## A transmission trades distance and speed for force

A reduction gear makes the motor turn several revolutions for one output revolution. Define the reduction ratio here as `G = motor speed / output speed`. With a 20:1 reduction, 600 rpm at the motor becomes 30 rpm at the output. In an ideal transmission, output torque is twenty times motor torque. Real transmissions dissipate energy, so use an efficiency estimate, η, between zero and one:

`output torque ≈ motor torque × G × η`

Suppose our preliminary moving-load target is 0.15 N·m, including explicitly provisional allowances for friction and acceleration. At `G = 20` and assumed `η = 0.70`, motor torque must be approximately `0.15 / (20 × 0.70) = 0.0107 N·m`. The efficiency is a design assumption to verify, not a property shared by every gearbox.

The sweep's average output speed is 45°/s, or 7.5 rpm. A smooth start and stop require a higher peak speed than that average. If we provisionally choose 15 rpm peak output speed, the motor must deliver its required torque at about 300 rpm. A listing that separately advertises enough torque and enough speed does not prove that both are available simultaneously.

Power makes the trade clearer. Mechanical power is `P = τω`, with angular speed ω in radians per second. One revolution is `2π` radians; 15 rpm is `15 × 2π / 60 = 1.571 rad/s`. Delivering 0.15 N·m at that speed takes approximately 0.236 W mechanically. Reduction changes torque and speed together; it does not create power. Losses increase the electrical input required.

Gears are one option. A toothed belt can move the motor away from the load and provide reduction with widely spaced pulleys. A lead screw converts rotation to translation: a 2 mm lead advances 2 mm per revolution, so 120 rpm gives 4 mm/s. A linkage can produce a useful path or mechanical advantage that changes through its motion. These choices also change packaging, friction, stiffness, maintenance, and failure behavior. Do not assume a screw or gearbox will hold a load without power; back-driving behavior depends on geometry, friction, wear, and operating conditions.

## Three errors that feel similar

Turn an output clockwise to a mark, then approach the same mark counterclockwise. If the input moves before the output responds, clearance between mating parts creates **backlash**. If the output moves under load and springs back when released, the mechanism has **compliance**, the inverse of stiffness. If it sticks and then jumps, static friction and changing contact forces are involved. A higher-resolution encoder does not remove any of these mechanical causes.

Accuracy describes closeness to a desired value. Repeatability describes how tightly repeated attempts cluster. A rig might repeatedly stop 2° short: repeatable, but inaccurate. It might average the correct angle while scattering widely: correct average, poor repeatability. Record the direction of approach and applied load when measuring either property.

Support the load through an intentional bearing or guide arrangement. A motor shaft may have limited allowable radial and axial loads; its ability to produce torque does not establish its ability to support an overhung arm. A flexible coupling accommodates specified misalignment between supported shafts. It is not a substitute for supporting a loose shaft. Revisit the free-body diagram with the transmission installed: gear and belt forces add loads of their own.

## What the motor can actually deliver

A brushed DC motor develops torque through current in its windings. As it turns, it generates a voltage opposing the supply, called back electromotive force, or back EMF. At rest that opposing voltage is absent, so starting current can be large. A blocked motor also remains in that condition. Manufacturer guidance distinguishes free-running current, stall current, and controller limits for this reason. [Pololu's motor and supply selection guide](https://www.pololu.com/docs/0J73/4.1) is a useful practical treatment.

For an illustrative motor at one fixed supply voltage, suppose no-load speed is 1,000 rpm and stall torque is 0.050 N·m. A simple straight-line approximation predicts 800 rpm at 0.010 N·m and 400 rpm at 0.030 N·m. This is a teaching model, not a purchased motor specification. Obtain a real torque–speed curve, winding limits, gearbox limits, and operating-duty information before selecting hardware.

At stall, speed is zero, so useful mechanical power `τω` is zero even though electrical power is entering and heating the motor. Stall torque is consequently a poor continuous-duty target. A motor that survives a brief startup may overheat if held against a stop. Gear teeth or a coupling may fail before the motor does. Never perform an unrestricted stall test to discover the rating of an unknown motor.

A **servo** is a feedback-controlled actuator system: a controller compares measured motion with the requested motion and changes the drive. A hobby servo commonly packages motor, gears, position sensing, and controller, but its advertised torque still needs supply, thermal, and duty-cycle context. A **stepper motor** advances through commanded magnetic states. Counting steps can predict position only while the rotor follows those commands; excessive load or acceleration can cause missed steps. Holding torque at zero speed does not describe torque at operating speed. [Adafruit's stepper guide](https://learn.adafruit.com/all-about-stepper-motors/what-is-a-stepper-motor) provides an accessible introduction and a separate driver-matching discussion.

## The driver belongs in the specification

A microcontroller output is a signal, not a motor power source. A motor driver switches current from a suitable supply. A reversible DC motor typically uses an H-bridge; a stepper needs appropriate phase control and, commonly, regulated winding current. Select the driver using motor voltage, startup and stall behavior, current limiting, heat dissipation, and fault response. A brief peak-current number is not the same as a continuous rating on your actual board.

Pulse-width modulation, PWM, switches power on and off quickly; duty cycle is the fraction of each period spent on. It controls average behavior but does not make every electrical or thermal quantity equal to its duty-scaled value. Inductance, switching frequency, recirculation paths, and load matter. Use the driver's documented wiring and supply range rather than treating PWM as permission to exceed a motor's rating.

Plan a limit switch or position reference, a maximum permitted motion time, and a physical way to remove drive power. Arrange the mechanism so a software crash cannot unexpectedly drop a load onto a person. For a first powered trial, use a restrained, low-energy mechanism and an accessible power disconnect, keep fingers outside pinch points, and limit current according to the chosen hardware. These are part of designing the experiment, not features to add after it moves.

## Lab: measure the lever before selecting its actuator

Use a light ruler or stiff cardboard strip, pencil, tape, two equal small objects, and a tabletop. Coins or identical washers work; use only small masses and keep everything just above a tray or table so nothing can fall far. A scale is optional. This is a balance experiment, not a strength test of a printed joint.

1. Mark the strip's center. Balance the empty strip on the pencil at that mark. Adjust the pivot until the strip's own weight produces approximately no turning moment.
2. Tape one object 40 mm to the left of the pivot. Place an equal object on the right and find its balance distance. Predict 40 mm before adjusting it.
3. Replace the right-hand object with two equal objects. Predict a 20 mm balance distance, then test. Record actual distances from the pivot to the objects' approximate centers of mass.
4. Keep the two objects on the right but move them outward by 5 mm. Describe which side falls and explain the change with a torque equation.
5. Draw the load path through strip, pivot, and tabletop. Identify a force that the torque balance alone did not tell you: the pivot's upward support reaction.

**Expected observations:** equal weights approximately balance at equal distances; twice the weight approximately balances at half the distance. A thick pencil contact, tape mass, nonuniform ruler, and uncertain object centers can shift the result. If balancing depends strongly on which side you approach from, suspect pivot friction before changing the torque law. These are predicted observations; this handbook does not claim that this physical lab has been performed.

Now write the arm example's actuator requirement on paper: travel, peak speed assumption, gravity torque, acceleration allowance, duty cycle, support arrangement, and response to power loss. Mark each entry as calculated, assumed, specified, or measured. A usable specification makes uncertainty visible.

## Check your model

**Predict:** What happens to gravity torque if the sensor moves from 80 mm to 40 mm? What if reduction doubles while motor speed stays fixed? Does a stationary powered motor necessarily consume zero electricity?

**Answers:** sensor gravity torque halves; output speed halves and ideal output torque doubles, with actual changes affected by losses and limits; stationary mechanical power is zero but winding current can still produce substantial heat. Notice which quantities the equations describe before transferring an answer from mechanics to electricity.

For an independent challenge, design a hand-operated sensor tilt mount with a pointer and angle scale. Set a repeatability target, then approach five marks from both directions under the same small load. Record error and reversal behavior separately. Only after that experiment, compare a belt, gear, and lead-screw arrangement for motorizing it. Choose using measured needs, not a favorite actuator.

For a longer build-oriented path, Dustyn Roberts's [*Making Things Move*](https://www.mheducation.com/highered/mhp/product/making-things-move-diy-mechanisms-inventors-hobbyists-artists.html) connects mechanisms to approachable projects. The publisher's contents suit this transition from static parts to motion; it is a paid book, and older component examples need current datasheet checks. Start by redrawing one mechanism with your own load, support, and failure assumptions.
