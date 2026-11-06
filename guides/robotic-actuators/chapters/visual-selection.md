# Choose by the constraint that matters

A motor that works well in a printer can be a poor choice for a robot elbow. The printer may care about repeatable positioning along a guide. The elbow may need to hold weight, survive pushes, and move gently in contact with a person or object. We can understand the difference by comparing the complete job: motion, load, duty, feedback, support, and available power.

Use this visual map to make a shortlist, then follow the linked chapters for the calculations. The advantages below are reasons to investigate a family. The constraints are questions its actual datasheet and your prototype must answer; they are not universal rankings of every product in that family.

## First separate the names

**Brushed, stepper, and brushless** describe motor technologies. **Servo** describes a feedback-controlled system, and an integrated servo packages several parts of that system. **Belt, gearbox, screw, and tendon** describe ways to transmit motion. **Series elastic** describes where a compliant element sits in the force path. Those categories overlap: a brushless servo can drive a belt, a geared servo can pull a tendon, and either can include measured series compliance.

![Functional sketches compare a brushed motor with rotating windings and mechanical commutation, a permanent-magnet stepper with two phase groups, and a brushless motor with stationary phase windings and a magnet rotor.](assets/compare-motor-physics.svg)

*Look for what turns and what switches the magnetic field. The drawings simplify pole counts and winding paths; they are explanations of operating principles, not winding instructions or sectioned product models.*

| Electric option | Why it can be useful | Main cost or limitation | Check before choosing |
| --- | --- | --- | --- |
| Brushed DC gearmotor | Straightforward reversible drive; many sizes and ratios; useful for wheels and simple mechanisms | Brushes wear; gears add clearance and losses; a bare motor does not report angle | Continuous torque at speed, startup current, gearbox limits, encoder location |
| Integrated positional servo | Motor, reduction, sensing, and control arrive together; convenient for a first joint or gripper | Package geometry, modes, thermal behavior, and output support constrain your mechanism | Usable travel, sustained load data, bearing loads, command-loss behavior, telemetry |
| Stepper with driver | Predictable command increments and useful low-speed positioning; common in guided stages | Moving torque falls within a speed-dependent envelope; heat and resonance matter; open loop can miss motion | Actual motor/driver torque–speed curve, acceleration, duty, homing, and feedback needs |
| Brushless motor with servo drive | Electronic commutation; flexible torque/velocity/position control when properly integrated | Rotor sensing or estimation, compatible electronics, commissioning, and tuning add work | Torque/current convention, voltage headroom, low-speed control, peak and continuous limits |
| Direct or modest-reduction drive | Removes or reduces transmission effects; attractive for a joint you want to push or control in contact | Motor must provide more joint torque; mass, current, and cooling can grow | Whole-system torque density, cogging/friction, thermal conditions, power-off behavior |

Microchip's [motor-control overview](https://www.microchip.com/en-us/solutions/technologies/motor-control-and-drive/motor-control-algorithms) separates the commutation and drive approaches. Oriental Motor's [stepper explanation](https://www.orientalmotor.com/stepper-motors/technology/stepper-motor-basics.html) shows the phase-and-rotor relationship. Read [chapter 2](#chapter-02) for the qualifications that product headlines often leave out.

## Then choose the mechanical exchange

![Kinematic schematics compare a same-direction open belt, opposite-direction external spur gears, a fixed-ring planetary stage, and a guided screw stage. Each labels its ratio or travel and its support constraint.](assets/compare-transmissions.svg)

*Trace the input and output arrows. The familiar 20T:60T examples both reduce speed by three, but place the shafts and reverse direction differently. The planetary example has another moving member—the carrier—so its ratio is 1 + 60/20 = 4, not 60/20.*

| Transmission | What it buys | What it adds to the design |
| --- | --- | --- |
| Timing belt | Separates axes; lets you move motor mass away from the joint | Belt width and tension, shaft loads, alignment, elastic stretch, and installation travel |
| Spur or planetary gears | Compact torque multiplication; a planetary stage can keep input and output coaxial | Tooth and bearing loads, backlash, lubrication, housing stiffness, and ratio-dependent inertia |
| Cycloidal or strain-wave reducer | Large reduction in a compact arrangement | Eccentric or flexing components, precision interfaces, compliance, fatigue, and assembly complexity |
| Worm drive | Right-angle packaging and substantial reduction | Sliding losses and heating; difficult backdriving does not establish a reliable power-loss restraint |
| Screw | Converts many motor turns into small linear travel and axial force | A separate guide, defined thrust support, lead accuracy, backlash, critical speed, and end margins |
| Tendon and spool | Remote motor placement and a light moving finger | Tension-only action, routing friction, stretch, slack, termination, and changing spool radius |

Reduction trades speed for torque; it also changes reflected inertia. Backlash is motion through clearance; compliance is deformation under load. A transmission can have little backlash yet still twist appreciably. [Chapter 3](#chapter-03) develops those distinctions. The [planetary derivation](https://mechanics.ju.se/MachineElements/planetary-gears.html) explains why identifying the fixed member is essential.

For the first printed joint, a belt layout makes shaft support and alignment easy to see. That is a teaching advantage, not a claim that belts always outperform gearboxes. A compact enclosed joint may justify the integration effort of a purchased reducer; a long stage may favor a screw or belt for entirely different reasons.

## Some constraints live in the physical effect

![Qualitative plots show a DC motor's torque-speed trade, a pull solenoid's changing force with air gap, a voice coil's approximately constant-force working region, and a cylinder's unequal piston areas.](assets/compare-operating-constraints.svg)

*Read each horizontal axis before comparing curves. Speed, open gap, and stroke position are different variables. None of these drawings is a product rating. In particular, a solenoid's strong seated pull may say little about whether it can begin moving your load. The straight motor line is a first model; [maxon's explanation](https://support.maxongroup.com/hc/en-us/articles/360013761160-Motor-data-and-simulation) describes its limits.*

| Other option | A plausible job | Advantage | Constraint that often decides |
| --- | --- | --- | --- |
| Pull solenoid | Latch or brief end-to-end action | Compact, simple pull mechanism | Force across the entire stroke, return mechanism, impact, and permitted energized duty |
| Voice coil | Small controlled displacement or oscillation | Bidirectional force from current, without a rotary transmission | Stroke, guidance, continuous heating, and feedback; verify the stated force region |
| Pneumatic cylinder | Repetitive clamp where air already exists | Compact cylinder and simple end-to-end motion | Air supply, valves/flow, compressibility, friction, and behavior after pressure loss |
| Hydraulic cylinder | High-force machine with suitable hydraulic infrastructure | High force from a compact cylinder | Pump, valves, hoses, seals, heat, leakage, and load holding belong in the system comparison |
| Shape-memory wire | Occasional compact latch or shape change | Small active element and quiet motion | Required wire length, heating/cooling time, bias force, operating temperature, and cycle life |
| Piezo actuator | Fine focus, alignment, or vibration control | Small, stiff motion with suitable electronics | Stroke–force trade, driver voltage/current, hysteresis, creep, and loaded dynamics |
| Series elastic arrangement | A mechanism that needs measured compliant contact | Spring deformation can estimate transmitted force after calibration | Extra travel, stored energy, stiffness choice, sensing, and achievable control bandwidth |

H2W's [voice-coil/solenoid comparison](https://cdn.h2wtech.com/blog/voice-coil-actuators-vs-solenoids) explains why those two magnetic devices serve different motion needs. SMC labels cylinder output [theoretical](https://www.smcworld.com/support/faq/en/s.do?ca_id=701&id=1654&lang=en): pressure times area precedes friction and the rest of the mechanism. [Chapter 8](#chapter-08) works through the less familiar options and their complete energy supplies.

## Turn the map into a decision

Our arm needs a brief moving torque envelope near 0.312 N·m, reaches 30 rpm at the output, and may need to hold horizontally at a gravity moment of 0.28449 N·m. A candidate that passes the moving point can still fail sustained holding. For that job, start by screening continuous thermal capability and the power-loss arrangement. For a light, fast indexing stage, the decisive screen might instead be moving torque at speed and settling. For the tendon finger, it may be travel and force observability after contact.

Pick two plausible families and write **one advantage, one cost, and one disqualifying condition** for each. Then change one requirement. For example, replace “hold the arm all afternoon” with “move once, then rest on a mechanical support.” The load calculation remains useful, but the duty and holding requirements change. If your shortlist never changes when the requirements do, revisit which constraint you used to choose it.
