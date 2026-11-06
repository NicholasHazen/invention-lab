# Other actuator families: choose the physical effect that fits

Our tendon finger needs about 15 N of cable tension and 10.47 mm of cable travel in its idealized geometry. A geared rotary motor can provide that through a spool. Could a solenoid pull the cable directly? Could a shape-memory wire replace the motor? Those questions become useful when we keep force, travel, response time, holding behavior, and the entire energy supply in the same comparison.

Bring the force and moment ideas from [chapter 7](#chapter-07). This chapter teaches you to screen unfamiliar actuator technologies and to distinguish intentional compliance from accidental looseness. You need paper and a calculator. The exercises are numerical design reviews; they do not ask you to assemble pressure systems, heat actuator wire, or energize piezo hardware.

## A short stroke is a different job from a joint rotation

A simple pull solenoid attracts an iron plunger into a magnetic circuit. Its force depends strongly on plunger position and current; the force quoted near the seated position may be unavailable at the beginning of travel. That can be useful for a latch that needs a brief pull and then rests against a stop. It is a poor assumption for a finger that needs controlled tension throughout its travel.

A return spring, gravity, or another mechanism usually provides the opposite motion in a simple one-direction solenoid. The return force subtracts from useful pull and the stop must absorb the final motion. Other designs provide latching, proportional, or bidirectional behavior; TLX's [solenoid design guide](https://static.tlxtech.com/files/Leveraging-Custom-Linear-Solenoids.pdf) describes these variations. Check the force–stroke curve and continuous versus pulse duty at the stated voltage and temperature. A coil that survives a short pulse may overheat during a long hold.

A **voice coil** instead places a current-carrying conductor in a permanent magnetic field. Within its specified working region, force is approximately proportional to current, and reversing current reverses force. This suits small controlled displacements, vibration excitation, or compliant contact. The actuator still needs guidance, travel limits, and position feedback when position matters. H2W's [voice-coil and solenoid comparison](https://cdn.h2wtech.com/blog/voice-coil-actuators-vs-solenoids) explains their different force-versus-stroke behavior; consult a specific product curve for actual range.

The absence of gears does not remove heating. Suppose a hypothetical voice coil has force constant `5 N/A` and resistance `2 Ω`. Producing our ideal 15 N requires `15/5 = 3 A`, and copper loss at that resistance is `I²R = 18 W`. At a stationary hold, useful mechanical power is zero. The device might still be suitable with the right continuous thermal rating, but a peak-force headline cannot establish that. Increasing current to 6 A would double ideal force and quadruple copper heating to 72 W. These numbers demonstrate a relationship, not a candidate or a drive setting.

## Fluid actuators move the supply outside the joint

A pneumatic cylinder turns pressure into linear force. That makes a compact cylinder attractive for repetitive opening, closing, or clamping when a suitable air supply already exists. A portable robot must also carry or connect to the compressor, valves, regulator, tubing, and energy storage. Compare that complete system with the electric alternative, including noise, leaks, and the energy spent producing compressed air.

For a cylinder with one rod, extension and retraction have different effective piston areas. The ideal extension force is cap-side pressure times full piston area minus rod-side pressure times annular area. Subtract seal friction and external resistance to predict acceleration. The common shortcut `F = pressure × area` assumes the opposite side contributes negligible gauge-pressure force. SMC's [cylinder-output explanation](https://www.smcworld.com/support/faq/en/s.do?ca_id=701&id=1654&lang=en) labels this result theoretical for a reason.

Air compresses, so a blocked cylinder and its tubing behave partly like a spring. Valve flow limits, chamber volume, pressure changes, friction, and feedback determine the motion response. A faster valve does not by itself make a stiff, accurate position axis. Festo distinguishes [servo-pneumatic positioning](https://www.festo.com/ca/en/c/products/actuators-and-drives-id_pim5) from simple cylinder actuation and identifies air compressibility as a design consideration.

Hydraulic cylinders use a liquid working fluid and can deliver large forces from compact actuators. They still require pump capacity, valves, hoses, filtration, seals, cooling, and load-holding provisions. Fluid, hose, and frame compliance remain; “liquid” does not mean an infinitely rigid mechanism. Leakage and throttling losses can turn input energy into heat. Parker's [cylinder application guide](https://www.parker.com/content/dam/Parker-com/Literature/Industrial-Cylinder/cylinder/cat/english/Parker_Mobile_Cylinder_Products_Catalog_HY18-1000.pdf) is useful for seeing the supporting hardware and force/flow calculations together.

For both families, consider what happens when pressure is lost, a hose fails, or a valve sticks. Isolate and verify stored-energy release using the selected equipment's documented procedure before servicing it. Our learning path stops at drawings and calculations here. Printed pressure vessels and improvised pressure plumbing would introduce a separate engineering problem that this guide does not establish how to solve.

## A paper cylinder exposes the trade

Consider a hypothetical 16 mm bore, 6 mm rod cylinder with 0.10 MPa gauge pressure at the driving chamber, zero gauge pressure in the opposing chamber, and ignored friction. Full piston area is `π × 16²/4 = 201.06 mm²`. Rod-side area is `201.06 − π × 6²/4 = 172.79 mm²`. Since `1 MPa = 1 N/mm²`, theoretical forces are 20.11 N extending and 17.28 N retracting.

Both exceed the finger's ideal 15 N tension, but that arithmetic does not select the cylinder. A return spring, seal friction, pressure drops, speed requirement, and force-control tolerance could consume the apparent margin. At 20 mm/s extension, cylinder-side volume flow is `area × speed = 4,021 mm³/s`, or 0.241 L/min. For compressed air, this chamber-volume flow is not the same as a compressor's free-air flow rating; density and reference conditions matter.

Predict what happens if bore diameter doubles while rod diameter remains 6 mm. Extension area and theoretical extension force quadruple. Required chamber flow at the same speed also quadruples. Greater force arrives with a supply and packaging cost rather than appearing for free.

## Compliance can be an intentional measuring element

A soft fingertip cushions contact. A return spring opens a finger. A flexible belt twists under load. These are forms of mechanical compliance, but they do not all provide a measured force signal. A **series elastic actuator** deliberately places an elastic element in the actuator's force path. Measuring its deformation and knowing its calibrated stiffness allows an estimate of transmitted force, which can be used in feedback.

![A spring in series transmits tendon force and can be measured. A separate return spring helps open the finger and adds to the required actuator force.](assets/families-compliance.svg)

For a linear spring, the first model is `F = kx`. The actuator moves one end; the load moves the other; their relative displacement is x. A spring in parallel with the load has a different role: it can counterbalance weight or provide return force. Draw which bodies each spring connects before naming the architecture. Williamson's [MIT series-elastic-actuator report](https://dspace.mit.edu/entities/publication/7ca5684c-f297-40cc-b145-532eb634fae4) examines the trade between force behavior, shock response, and achievable bandwidth.

Take an illustrative series spring of `1.5 N/mm`. Transmitting 15 N stretches it 10 mm and stores `½kx² = 0.075 J`. In the constant-moment-arm finger model, winding the finger closed requires 10.47 mm of tendon travel. Building 15 N after contact adds another 10 mm at the spring. From an initially unstrained state, the actuator must accommodate approximately 20.47 mm total cable take-up, about 146.6° on the 8 mm spool. A mechanism sized for only the original 75° spool motion would run out of travel.

A 0.1 mm spring-deflection measurement increment corresponds ideally to 0.15 N tension increments at this stiffness. This is resolution, not calibrated force accuracy: spring hysteresis, friction, preload, sensor error, and tendon routing all matter. Making the spring stiffer reduces travel but also reduces the deformation available to measure a given force. Making it softer introduces more deflection and changes the mechanical dynamics. A natural frequency from a spring–mass calculation is not the closed-loop force bandwidth; the motor, transmission, sensor, and controller also constrain response.

The stored energy remains when drive power disappears. Design spring retention and travel stops so release cannot fling parts. Begin a physical compliance study with a small commercial spring, passive displacement measurement, and restrained loads, after selecting its allowable travel; the numbers above are not a spring purchase specification.

## Shape-memory wire and piezoelectric motion

Shape-memory alloy wire contracts when heating changes its material state; cooling and a bias load allow recovery. That can make a quiet compact latch or occasional motion attractive. For repetitive movement, heat must leave the wire between cycles. More heating current can accelerate the heating phase but cannot remove the cooling requirement. Ambient temperature, diameter, stress, and strain affect response and life.

Dynalloy's [Flexinol technical data](https://dynalloy.com/technical-data-wires/) gives operating guidance and condition-specific cooling times. For example, its 0.10 mm, 70°C wire entry lists an approximate 1.1 s cooling time in room-temperature static air with a vertical wire. That is not a universal cycle rate. At an assumed 4% working contraction, our 10.47 mm tendon travel would require roughly `10.47/0.04 = 262 mm` active wire before adding routing, bias motion, or series compliance. A compact-looking strand can require considerable installed length, and its force capability must be checked separately.

Piezoelectric actuators change dimension in an electric field. Stack actuators suit small, stiff displacements; flexure amplification can enlarge motion while trading away force and stiffness. They are useful for fine optical adjustment and vibration control, but a bare stack is not a direct replacement for a long-travel finger actuator. Piezo walking and ultrasonic motors combine repeated small motions to obtain longer travel; assess their complete mechanism separately.

Voltage does not map to one exact displacement in an open-loop piezo: hysteresis makes the path matter and creep changes displacement over time. PI's [displacement tutorial](https://www.physikinstrumente.com/en/expertise/technology/piezo-technology/properties-piezo-actuators/displacement-behavior/) explains why feedback is valuable. A piezo also has different free-displacement and blocking-force endpoints; it cannot deliver both simultaneously. Its electrical capacitance requires charging current during motion, while dielectric losses and driver limits constrain repetition. [PI's dynamic-operation guide](https://www.physikinstrumente.com/en/expertise/technology/piezo-technology/properties-piezo-actuators/dynamic-operation/) relates useful response to the loaded mechanics. Use packaged, documented equipment for a future piezo experiment; this chapter provides no high-voltage driver recipe.

## Screen by the required motion

Make four cards: a latch that moves once per minute, our 15 N tendon finger, a fine-focus adjustment, and a repetitive industrial clamp with an existing air supply. For each, list travel, force through the entire stroke, duty, required feedback, and response after power loss. Then assign two plausible actuator families and one reason each might fail.

Recalculate the series-spring example with `k = 3 N/mm`. Predict the change before calculating. The spring stretches 5 mm at 15 N, stores 0.0375 J, and requires about 15.47 mm total take-up under the same assumptions. A 0.1 mm measurement increment now represents 0.30 N, so the reduced travel comes with coarser force resolution. If your energy increases when stiffness doubles at fixed force, check whether you accidentally held displacement fixed instead.

For an independent challenge, design the finger's behavior after an object blocks it halfway closed. Compare motor-current limiting, measured series-spring deformation, and a simple solenoid pull. Specify what each approach can actually observe. That comparison turns actuator choice into a prediction about contact behavior, which is much more useful than selecting whichever technology has the largest force headline.
