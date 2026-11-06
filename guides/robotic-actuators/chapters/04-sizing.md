# Size the motion before choosing the motor

A motor can lift an arm once and still be unsuitable for holding it all afternoon. The lift asks for torque and speed together; the hold asks for torque without cooling time. This chapter turns the rotary study into a small requirements sheet with separate entries for motion, holding, current, and repeated operation.

You need the force and moment ideas from [the requirements chapter](#chapter-01), a calculator, and optionally Python 3.10 or newer. You will calculate the load demand, translate it through a reduction, and run a time history that exposes what a single “required torque” number leaves out. The numbers describe a design study, not a tested rating for the earlier pivot.

## Start where the load acts

Our output shaft has a horizontal axis. A 100 mm arm carries a 0.25 kg payload at its tip; the uniform arm itself weighs 0.08 kg. Measure angle θ upward from horizontal. The payload's weight acts at 100 mm and the arm's weight at its midpoint, 50 mm. At horizontal, both have their greatest moment arm about this shaft.

Convert millimeters to meters before multiplying. Using gravitational acceleration g = 9.81 m/s²:

```text
Maximum gravity torque = g × (payload mass × tip radius + arm mass × length/2)
                       = 9.81 × (0.25 × 0.100 + 0.08 × 0.050)
                       = 0.28449 N·m
Gravity torque at angle θ = 0.28449 × cos(θ) N·m
```

At vertical, gravity contributes zero torque in this ideal geometry. That does not make vertical a robust parking position: a disturbance, a shifted center of mass, or a loss of support can start a fall. Plan a mechanically supported rest position before adding power.

Mass also resists acceleration. Moment of inertia J records both how much mass there is and how far it is from the axis. A point payload contributes mr²; a uniform slender arm rotating about one end contributes mL²/3. Therefore J_load = 0.25 × 0.100² + 0.08 × 0.100²/3 = **0.002766667 kg·m²**. Inertia remains present when the arm is stationary; its acceleration torque happens to be zero then. Add real output pulleys, hubs, fasteners, and wiring masses when the layout becomes a specific assembly.

## Specify how the arm gets there

“Move 90° in one second” does not specify a speed profile. We choose equal acceleration and deceleration halves, with no cruise interval. The speed graph is a triangle: its area must equal the angular travel. A 90° move is π/2 radians, so peak speed is twice travel divided by time, or π rad/s = **30 rpm**. Constant acceleration during the first half is 2π rad/s² = **6.283185 rad/s²**.

The acceleration torque magnitude is J_load × α = **0.017383479 N·m**. Gravity dominates this particular slow move. Shorten the time to 0.5 seconds and speed doubles, but acceleration and its torque increase fourfold. The gravity term remains unchanged. This is why choosing a faster motor is not the whole answer to a faster move.

![Output torque components during the one-second upward move. Gravity falls as the arm rises; the acceleration term changes sign halfway.](assets/sizing-torque-trace.svg)

The discontinuity halfway through this ideal profile demands an instantaneous acceleration change. A real mechanism has finite stiffness and a real drive has finite bandwidth. Use this profile for a first sizing calculation; later choose a trajectory with bounded acceleration changes if the mechanism rings or the process requires smoother movement.

## An envelope and a time history answer different questions

Add a deliberately assumed **0.010 N·m moving friction allowance**. This is a placeholder to replace with measurement, and it does not describe breakaway friction. A positive-demand envelope adds the largest magnitudes:

```text
Output envelope = maximum gravity + acceleration magnitude + moving friction
                = 0.284490 + 0.017383479 + 0.010000
                = 0.311873479 N·m
```

An envelope is useful before the timing is known. It is not automatically the largest torque that actually occurs. In this specific upward move, maximum gravity and positive acceleration coincide in the limit just after starting, so the model approaches this value. In a different orientation or trajectory, the peaks need not coincide.

To find simultaneous demand, evaluate torque at the same θ, velocity, and acceleration at every instant. Just before the halfway point, θ approaches 45° and acceleration is positive. Just afterward, gravity is nearly unchanged but acceleration reverses. Near the vertical endpoint, deceleration can require negative actuator torque even though velocity remains positive. That interval can return mechanical energy toward the drive. Never apply a forward-efficiency formula indiscriminately to this reverse flow.

## Move the demand to the motor shaft

The 20-tooth driving pulley and 60-tooth output pulley give reduction G = 3. Define G as motor speed divided by output speed. Peak motor speed is **90 rpm**. With assumed forward efficiency η = 0.90, the motor's transmission torque subtotal is 0.311873479/(3 × 0.90) = **0.115508696 N·m**.

The rotor must accelerate too. Suppose a candidate's rotor inertia were **0.000010 kg·m²**. This is an illustrative input, not an identified motor. Motor acceleration is Gα, so its additional torque is J_motor × G × α = **0.000188496 N·m**. The combined illustrative envelope becomes **0.115697192 N·m**, before omitted motor friction and input-pulley inertia.

Increasing reduction lowers the load's contribution but increases the rotor acceleration term. The load inertia reflected to the motor is J_load/G² = **0.000307407 kg·m²**. The square comes from kinetic energy: substituting output speed = motor speed/G into ½Jω² produces the factor 1/G². This coordinate conversion does not remove bearing forces, belt tension, or structural bending. [Oriental Motor's sizing procedure](https://www.orientalmotor.com/technology/motor-sizing-calculations.html) likewise treats inertia, torque, and speed as separate selection inputs.

Do not choose a motor from stall torque alone. Compare the demanded torque at its accompanying speed against the selected motor-and-drive operating limits, then check pulse duration, repetition, supply voltage, and temperature conditions. A reduction is only acceptable if its own torque, speed, radial-load, and life limits also fit.

## Run the numerical experiment

Download [actuator_sizing.py](examples/actuator_sizing.py) and [test_actuator_sizing.py](examples/test_actuator_sizing.py) into one folder. Open a terminal there and run:

```sh
python3 actuator_sizing.py --rotor-inertia 0.00001 --csv cycle.csv
python3 -m unittest -v test_actuator_sizing
```

The program uses only Python's standard library and never connects to hardware. The first section prints the forward-efficiency envelope above. The second deliberately uses an **ideal reversible transmission**, η = 1, for a four-second cycle: raise for one second, hold vertical for one, lower for one, hold horizontal for one. It includes the specified rotor inertia and signed moving friction; holds receive no friction credit. It does not simulate a controller.

The executed reference run produced **0.068669031 N·m motor RMS torque** for that ideal cycle and **0.031415927 J net mechanical work**. These are calculated results, not measurements. The work equals friction torque multiplied by the round-trip angle; potential and kinetic energy return to their starting values. The 14 accompanying tests passed, including energy balance, reversed motion, time scaling, and invalid-input rejection.

RMS means square each torque, weight by its duration, average over the entire cycle, then take the square root. A hold belongs in that average. Dividing the peak by a convenient factor cannot reproduce an arbitrary cycle. RMS torque is useful for motor selection, but peak operation must also be checked separately. [maxon's Formulae Handbook, section 6.5](https://www.maxongroup.com/medias/sys_master/8802918268958.pdf?attachment=true) presents those distinct checks.

If torque-producing current were defined by K_t = 0.020 N·m/A, our illustrative positive envelope corresponds to **5.78486 A**, and the ideal cycle RMS corresponds to **3.43345 A**. Neither is the bench supply's current. The meaning of an ampere must match the motor constant: winding current, phase RMS, phase peak, and field-oriented q-axis current are not interchangeable labels. [Chapter 9 on feedback and drives](#chapter-09) develops this distinction.

Current RMS can estimate copper heating with an appropriate resistance and current convention. It does not predict winding temperature by itself: cooling, thermal time constants, changing resistance, and speed-dependent losses still matter. Our ideal-transmission RMS also omits transmission losses. Treat it as a comparison exercise, not permission for continuous operation.

## Cross-check the other two designs

The horizontal screw stage needs 10 N at 20 mm/s. A 2 mm/rev lead requires **600 rpm**. At assumed forward efficiency 0.35, torque is F × lead/(2πη) = **0.009094568 N·m**. Multiplying torque by angular speed gives **0.571429 W input mechanical power**; the stage receives Fv = **0.200 W**. Acceleration, screw inertia, preload, and guide friction beyond the stated resistance remain separate.

For the finger, 5 N at a 30 mm tip arm needs 0.15 N·m at the hinge. A constant 10 mm tendon moment arm requires **15 N tension**. An 8 mm spool needs **0.120 N·m**, and a 60° finger turn consumes **10.471976 mm of tendon**, or **75° of spool rotation**. These assume constant moment arms and a single effective spool radius; return springs and routing losses add demand.

Predict what happens if you double screw lead or spool radius. The answer in each case is twice the required shaft torque and half the shaft rotation for the same output travel. Energy still balances. If your calculation makes both torque and travel smaller, inspect the ratio direction and millimeter-to-meter conversion.

For an independent variation, run the rotary program with `--move-time 0.5`, then with `--ratio 6`. Record which quantities change and which do not. Use that comparison to nominate two candidate motor/reduction combinations, leaving their thermal and electrical entries blank until actual datasheets supply them.
