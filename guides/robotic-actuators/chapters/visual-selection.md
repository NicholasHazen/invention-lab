# Choose by the constraint that matters

A hobby servo, a harmonic drive, and a brushless motor can all appear in a search for a robot joint. They describe different parts of the solution. A servo supplies controlled motion; a harmonic drive changes speed and torque; a brushless motor supplies electromagnetic torque. A single joint can combine all three. This map gives each familiar name its own place, then compares the benefits and constraints that matter when building with it.

Start with the motion you need. Follow the comparison to a mechanism lesson, then use the sizing chapters to evaluate a specific component. These are reasons to investigate an option, not universal performance rankings. Actual ratings, support bearings, drive, cooling, and duty determine whether a product can do your job.

## First separate the names

| The choice | What the name tells you | Examples |
| --- | --- | --- |
| Motor or physical effect | Where mechanical force originates | Brushed DC, stepper, brushless, linear motor, solenoid, pneumatic cylinder |
| Transmission | How motion and effort reach the load | Harmonic/strain-wave, cycloidal, planetary, belt, screw, tendon |
| Feedback and packaging | What is measured, controlled, and supplied together | Hobby servo, smart bus servo, industrial servo system, integrated robot joint |
| Mechanical arrangement | How the load is driven or made compliant | Direct drive, quasi-direct drive, series elastic, counterbalanced joint |

For example, “brushless servo with a strain-wave reducer” describes the motor, control, and transmission. “Frameless” means a motor is supplied for integration into your structure; it does not mean bearings, encoder, controller, or cooling arrive with it. “Servo” does not promise a particular gear type, torque, or accuracy. [Chapter 2](#chapter-02) separates these choices with a labeled system diagram.

## Servo systems and integrated joints

These are often useful first candidates for a maker concentrating on a mechanism. Read **what the command means** before comparing torque: a connector or the word “digital” does not establish which variables the device controls.

| Type | What it does / why choose it | Drawbacks and constraints | Learn more |
| --- | --- | --- | --- |
| **Hobby positional servo** | Motor, gears, output sensor, and controller in one package; a pulse command usually requests an angle | Specified travel; gearbox play; sustained torque may be poorly documented; supply current and output bearing loads matter | [Position control](#c02-hobby-positional-servos) |
| **Continuous-rotation hobby servo** | Convenient drive for a wheel or winch; command commonly sets direction and effort around a neutral point | Usually cannot command an absolute angle; neutral drift and load-dependent speed; verify actual speed feedback | [Command differences](#c02-continuous-rotation-servos) |
| **Smart bus servo** | Addressable actuators with reported position and model-dependent telemetry or current/velocity modes | Protocol, bus wiring, update rate, faults, thermal limits, and supported modes; greater cost than simple hobby packages | [What the bus adds](#c02-smart-bus-servos) |
| **Industrial servo motor + drive** | Matched feedback motor and drive offer configurable position, velocity, or torque control and detailed sizing data | Motor, drive, feedback, supply, commissioning, and mechanics form a system; a bare servo motor needs its drive | [A controlled axis](#c02-industrial-servo-motor-and-drive) |
| **Integrated robot joint actuator** | Packages motor, reduction, sensing, and drive; some include output support and a hollow bore | Verify bearings, brake, encoder location, protocol, cooling path, and power-loss behavior; “integrated” does not establish what is included | [Joint packages](#c02-integrated-robot-joints-and-quasi-direct-drive) |
| **Direct drive / quasi-direct drive (QDD)** | No reducer, or a modest reduction, can improve mechanical transparency when interacting with a load | Motor must supply more torque; diameter, current, cooling, cogging, friction, and tuning matter; QDD has no fixed universal ratio | [Reducing the reduction](#c02-integrated-robot-joints-and-quasi-direct-drive) |

A hobby servo helps you learn mounting, commands, and joint motion. A smart servo makes reported state and faults easier to inspect. A custom motor-and-drive system gives architectural freedom while asking you to solve more integration problems. None is selected for our arm until its operating evidence and output support pass the requirement. The [ROBOTIS operating-mode manual](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/) illustrates the detail to seek.

## Rotary motor technologies

![Functional sketches compare a brushed motor with rotating windings and mechanical commutation, a permanent-magnet stepper with two phase groups, and a brushless motor with stationary phase windings and a magnet rotor.](assets/compare-motor-physics.svg)

*Look for what turns and what switches the magnetic field. These sketches simplify pole counts and winding paths.*

| Type | Benefit | Constraint that can rule it out |
| --- | --- | --- |
| Brushed DC motor / gearmotor | Approachable reversible drive for wheels, spools, and custom mechanisms | Brushes wear; startup current can be large; encoder and feedback control are additional choices; gearbox torque has its own limit |
| Open-loop stepper | Useful low-speed positioning with step-and-direction commands | Counted steps do not prove motion; moving torque, resonance, acceleration, and energized heating constrain operation |
| Closed-loop stepper | Feedback can detect or correct position error within the system's capability | Feedback cannot create missing torque; assess motor, drive, error response, and torque–speed curve together |
| Brushless permanent-magnet motor, including BLDC/PMSM designs | Electronic commutation avoids brush wear; compatible drives enable current, velocity, and position control | Drive/feedback compatibility, low-speed sensing, torque/current conventions, voltage headroom, and cooling |
| Frameless torque motor | Rotor and stator can fit directly around your joint geometry | You supply alignment, air gap, bearings, retention, sensing, heat path, and control integration |

Coreless, slotless, outrunner, and inrunner describe further construction choices. They affect quantities such as inertia, diameter, heat flow, and cogging; they do not replace the operating-envelope comparison. [Chapter 2](#chapter-02) develops motor selection; [chapter 9](#chapter-09) connects drives and feedback. Oriental Motor's [stepper explanation](https://www.orientalmotor.com/stepper-motors/technology/stepper-motor-basics.html) helps interpret the stepper rows.

## Rotary transmissions and reducers

**Harmonic drives and cycloidal drives deserve separate comparisons.** Both can make compact high-reduction joints, using different mechanisms and manufacturing methods. Harmonic Drive® is a brand associated with **strain-wave gearing**; “strain-wave” is the useful generic search term.

| Type | How it works / principal benefit | Cost, limitation, or design constraint |
| --- | --- | --- |
| **Harmonic / strain-wave reducer** | A rotating wave generator deforms a toothed flexspline inside a circular spline; a small tooth-count difference creates large reduction | Flexspline fatigue, wave-generator bearing, precision teeth, lubrication, torque/speed limits, and elastic twist; low backlash does not mean zero deformation |
| **Cycloidal reducer** | An eccentric drives a lobed disc against ring pins or an internal ring; an output mechanism extracts slow rotation | Eccentric bearings, pin contact, clearance/preload, disc profiles, balancing, and lubrication; printed demonstrators cannot inherit metal reducer ratings |
| **RV-style reducer** | A particular two-stage arrangement combines an initial gear stage with a cycloidal stage | More bearings and closely fitted components; mass, housing stiffness, assembly tolerances, and product-specific load ratings |
| **Planetary gearbox** | Planets share contact around a sun gear; holding one member creates a compact, often coaxial reduction | Load sharing depends on precision; backlash, carrier stiffness, bearings, number of stages, and efficiency |
| **Spur / helical gear train** | Parallel shafts with visible ratios; spur gears are approachable demonstrators; helical engagement can be smoother | Tooth profiles, centre distance, lubrication, housing stiffness, and backlash; helical teeth produce axial thrust |
| **Bevel gearing** | Changes shaft direction, commonly through 90° | Alignment, mounting distance, tooth contact, and bearing reactions; right-angle packaging alone does not imply large reduction |
| **Worm gearing** | Compact right-angle speed reduction | Sliding losses and heating; self-locking depends on geometry and friction and is not a general power-loss holding guarantee |
| **Timing belt** | Separates axes and places motor mass away from the joint | Tension adds shaft load; alignment, elastic stretch, tooth engagement, installation travel, and tooth jump limits |
| **Chain and sprockets** | Positive drive over separated axes where a chain's load and environmental characteristics fit | Lubrication, slack, wear, noise, speed ripple, support, and guarding |
| **Cable capstan / tendon** | Remote motor placement and low moving mass; a capstan transfers force through friction | Tension-only cable action, preload, routing friction, slip/stretch, termination, and effective spool radius |

Read the dedicated [strain-wave lesson](#c03-harmonic-drives-strain-wave-gearing) and [cycloidal/RV lesson](#c03-cycloidal-reducers-and-rv-drives) for component diagrams, reduction examples, and printability. [Chapter 3](#chapter-03) covers the wider comparison. The [Harmonic Drive video lesson](#watch-video-strain-wave-gearing) shows traveling engagement zones alongside the written explanation.

![Kinematic schematics compare a same-direction open belt, opposite-direction external spur gears, a fixed-ring planetary stage, and a guided screw stage. Each labels its ratio or travel and its support constraint.](assets/compare-transmissions.svg)

*Trace input and output. The 20T:60T belt and external gears both reduce speed by three, but the external gears reverse direction. With the ring fixed, the illustrated sun-input, carrier-output planetary gives 1 + 60/20 = 4:1. Identify fixed, input, and output members before using a ratio.*

## Linear motion options

“Linear actuator” describes the resulting motion. Inside there might be a screw, belt, electromagnetic motor, or fluid cylinder. A screw also needs a way to prevent unwanted rotation and to carry side loads.

| Type | Why choose it | What to check |
| --- | --- | --- |
| **Lead screw** | Simple sliding screw/nut pair for a compact guided axis | Friction, wear, efficiency, lead accuracy, backlash, speed, buckling, and thrust support; establish self-locking for the actual system |
| **Ball screw** | Rolling balls reduce sliding friction; preload can reduce lost motion | Cost, lubrication, contamination, nut packaging, preload drag, critical speed, support bearings, and backdriving |
| **Roller screw** | Threaded rollers provide many loaded contacts for demanding axial force and duty | Precision manufacture, cost, lubrication, alignment, and model-specific load/life data; not an easy printed substitute |
| **Packaged electric linear actuator** | Motor, transmission, screw, and housing arrive assembled; limits or feedback may be included | Stroke, retracted length, loaded speed, duty, feedback, end limits, allowable side loads, and power-off holding |
| **Belt axis / rack and pinion** | Can suit longer travel without a long rotating screw | Belt compliance/tension, or rack alignment/tooth backlash; separate guides and position reference |
| **Direct linear motor** | Magnetic force moves a carriage without rotary-to-linear transmission | Magnet track, guidance, encoder/commutation, cooling, cables, and continuous holding force; iron-core attraction can add bearing load |
| **Voice coil** | Bidirectional force approximately proportional to current over a specified working region | Travel, guidance, continuous heating, and feedback; peak force is not a sustained holding rating |

Use [chapter 3](#chapter-03) for screw construction and [chapter 6](#chapter-06) to model a guided stage. [Chapter 8](#chapter-08) compares packaged actuators, linear motors, and voice coils. Kollmorgen's [linear motor selection explanation](https://www.kollmorgen.com/en-us/blogs/how-to-select-direct-drive-linear-actuators) connects motor, guide, feedback, and cooling.

## Fluid, compliant, and specialized options

![Qualitative plots show a DC motor's torque-speed trade, a pull solenoid's changing force with air gap, a voice coil's approximately constant-force working region, and a cylinder's unequal piston areas.](assets/compare-operating-constraints.svg)

*Read each horizontal axis. Speed, open gap, and stroke position are different variables. These are qualitative relationships, not product ratings. A solenoid's strong seated pull may say little about whether it can start your load moving.*

| Type | A plausible use / advantage | Deciding constraint |
| --- | --- | --- |
| Pneumatic cylinder | Repetitive clamp or end-to-end stroke where air is available | Compressor/valves, compressibility, flow, friction, position control, and pressure loss |
| Hydraulic cylinder | High axial force with suitable infrastructure | Pump, valves, hoses, filtration, seals, heat, leakage, and load holding |
| Fluid rotary actuator | Pressure-driven limited-angle rotation, using a vane or rack and pinion | Angular range, seals, stops/cushioning, shaft loads, valves, and supply; distinguish from continuous fluid motors |
| Pneumatic artificial muscle | Pressurized tensile element contracts for compliant pulling | Force changes with contraction/pressure; return or opposing actuator, hysteresis, supply, and control |
| Soft chamber / bending actuator | Compliant chambers turn inflation into bending or gripping | Material, geometry, fabrication consistency, pressure, sensing, and fatigue; softness alone does not establish contact force |
| Solenoid, including latching types | Brief pull or latch; latching can retain a state without continuous coil power | Force throughout stroke, return/release method, impact, and permitted duty |
| Shape-memory alloy wire | Compact active element for occasional contraction | Installed length, heating/cooling time, bias force, temperature, and cycle life |
| Piezo stack / amplified piezo | Small, stiff motion for fine adjustment or vibration control | Stroke–force trade, driver requirements, hysteresis, creep, and loaded dynamics |
| Piezo walking / ultrasonic motor | Repeated microscopic motions create larger accumulated travel | Frictional contact, wear, load/speed behavior, specialized drive and control; evaluate separately from a bare stack |
| Series elastic actuator (SEA) | Measured spring deflection can estimate transmitted force | Extra travel, stored energy, stiffness, sensing, and control bandwidth; an arrangement around an actuator |

[Chapter 8](#chapter-08) explains these effects and their supporting equipment. Brakes, clutches, return springs, and counterbalances can change an actuator's job. Each has its own function and ratings: a holding brake retains a load, a clutch couples or disconnects a transmission, and a spring stores energy. Torque-limiting clutches have separately specified limits. They are not additional sources of continuous motor power.

## What to explore for our printed pivot

Keep the pivot's metal shaft and two bearing stations responsible for the neighboring module's bending loads. Then compare ways to **apply torque** to that supported joint. A servo horn or reducer flange does not automatically replace the support design; an integrated unit can do so only if its documented bearing and moment ratings cover the job.

| Candidate architecture | What the next experiment teaches | What would decide against it |
| --- | --- | --- |
| Positional or smart servo driving a supported shaft, directly or through a belt | Joint commands, mounting, supply behavior, and measured motion | Inadequate continuous torque, travel, duty, modes, or mounting space |
| Motor + encoder + timing belt | Separates motor, reduction, feedback, and support so each can be inspected | Belt tension, packaging, compliance, or control integration effort |
| Purchased strain-wave, cycloidal, or planetary reducer with motor/drive | Compact torque multiplication and reducer integration | Cost, speed loss, friction, output stiffness, mass, or unsupported loads |
| Direct-drive or QDD joint | Backdriving, current-based effort control, and contact behavior | Motor size, current/cooling, sensing, or power-loss holding requirements |

These are candidate experiments, not selected parts. The guide's worked arm reaches a brief moving torque envelope near 0.312 N·m and 30 rpm output, and may need to hold a horizontal gravity moment of 0.28449 N·m. Our real modular robot needs its own mass, lever arm, acceleration, duty, and cable-travel requirements. Passing a moving point does not establish an all-afternoon hold.

Pick two candidates and write **one benefit, one drawback, and one condition that rules each out**. Then change a requirement: let the arm rest on a support between moves, or require it to yield when pushed. Revisit continuous heating, transmission friction, sensing, and holding. The useful result is a shortlist that changes for an explainable reason when the job changes.
