# Design for people and purpose

A sensor bracket can hold a sensor securely and still be unpleasant to use. Perhaps the cable cannot be unplugged, the adjustment screw needs three hands, or reinstalling the sensor changes its aim. Mechanical performance is one part of the product. The complete job includes the person who sets it up, the surrounding equipment and the moments when something needs repair.

You will turn an observed task into requirements, compare distinct concepts and run a small usability experiment. Bring the project brief from [Chapter 1](../start/) and the measurement habits from [Chapter 3](../measurement/). The prototype can be cardboard. Its purpose is to reveal an interaction before you invest in detailed CAD.

## Observe a task before asking for a feature

“Would you like an adjustable bracket?” encourages agreement with your idea. “Show me how you position this sensor now” exposes the current process. Watch where the person pauses, changes grip, searches for a tool or repeats an alignment. Ask what happened during a specific recent attempt. Separate what you saw from your interpretation.

For example, you might observe that someone disconnects a cable before removing a sensor. Your first interpretation is that the cable is in the way. A follow-up may reveal that disconnecting it prevents the software from recording unwanted data. A larger cable opening would not solve that problem. The observation is real; the cause still needs investigation.

Keep three columns: observation, possible need and question to test. “The user held the sensor with one hand while tightening two screws” is an observation. “The user needs temporary support during adjustment” is a candidate need. “Would a locating ledge allow adjustment without holding the sensor?” is a testable question. This chain makes the reasoning available for revision.

The [Stanford d.school Bootleg](https://dschool.stanford.edu/tools/design-thinking-bootleg) offers methods for observing, defining, generating ideas, prototyping and testing. Use a method to answer a real project question; the names of the stages are not evidence that a concept works.

## Requirements describe outcomes and constraints

A useful requirement names a condition and a way to check it. “Easy to assemble” is a direction. “A new user can install the dummy sensor using the supplied instructions and one hex key, without dropping a loose nut” is closer to an observable test. You still need to decide how many users and attempts provide enough confidence for your purpose.

Separate essential constraints from preferences. A maximum envelope may be essential because the assembly must clear another part. A particular color may be a preference. A mounting-hole pattern may be an interface constraint inherited from a purchased sensor. If a requirement fixes a solution too early, record why that restriction exists.

| Need or constraint | Provisional requirement | Evidence to collect |
|---|---|---|
| Reinstall without realigning everything | Return the reference edge within the project's chosen tolerance | Repeated removal/replacement measurements |
| Keep connectors accessible | Plug and unplug the actual connector with the bracket installed | Task observation using the real plug envelope |
| Allow maintenance | Replace the sensor without dismantling the main support | Assembly sequence and tool-access trial |
| Avoid accidental reversal | Make intended orientation apparent before fastening | Unprompted first-use trial |
| Fit available fabrication | Stay within the chosen process and stock limits | CAD envelope and manufacturing review |

Do not copy a threshold from a tutorial and assume it matches your job. Derive it from the consequence of error. If a sensor's field of view is broad, a millimetre of mounting variation may be irrelevant. If two gears must maintain centre distance, the same variation can prevent operation. Requirements should connect to behavior.

## Generate concepts that differ in principle

Three sketches with different corner radii are usually one concept. To explore alternatives, change how the task is achieved. A sensor could rest against locating stops and use one retaining screw; slide into a rail and latch; or sit in an adjustable cradle with a separate lock. Each arrangement makes different promises about repeatability, access and adjustment.

Break the task into functions: locate, retain, adjust, connect and release. Sketch alternative ways to perform each function. Then combine compatible choices. This prevents the first attractive silhouette from dictating every subsequent decision.

A functional decomposition is not an instruction to make every piece modular. The pivot's integrated triangulated housing may combine stiffness, access and appearance in one printed part. The question is whether combining functions helps the particular requirements. Separate components introduce fasteners and tolerances; integrated components can complicate printing and repair. Count both effects.

## A weighted comparison is a conversation with your assumptions

Suppose three concepts pass the essential envelope and access constraints. You score each from 1 to 5, where 5 is better, on repeatability, ease of assembly and ease of fabrication. Assign weights of 0.5, 0.3 and 0.2 respectively:

| Concept | Repeatability | Assembly | Fabrication | Weighted score |
|---|---:|---:|---:|---:|
| Locating stops + screw | 4 | 3 | 5 | 3.9 |
| Slide rail + latch | 4 | 5 | 2 | 3.9 |
| Adjustable cradle | 2 | 4 | 4 | 3.0 |

The first score is `0.5×4 + 0.3×3 + 0.2×5 = 3.9`. The tie is useful. It tells you the table does not resolve the choice under these assumptions. The rail's assembly advantage and fabrication disadvantage offset each other. A small rail coupon or a first-use mockup can supply evidence where the scores were guesses.

Changing weights changes the answer. If assembly becomes dominant, the rail may lead. If fabrication time dominates, the stops may lead. Do a sensitivity check before treating the highest score as an objective fact. Do not average an essential failure into a respectable total: a concept that blocks the connector is disqualified until that constraint is addressed.

Record whether each score came from observation, calculation, supplier information or intuition. The table's precision should not hide the uncertainty of its inputs.

## Prototype the question, not the entire product

A cardboard model can test hand clearance and the order of assembly. It cannot establish the strength of a printed latch. A small printed coupon can test a sliding fit. It cannot establish the usability of a complete installation. Choose the prototype's fidelity according to the uncertainty you want to reduce.

For the bracket, three focused prototypes may be more useful than one polished assembly:

1. A full-size paper or card envelope to test placement and connector access.
2. A small mating-feature coupon to test manufacturing clearance.
3. A simplified complete bracket to test installation and repeatability.

The prototypes answer different questions. Label each with its purpose and excluded claims. If you substitute a dummy sensor, match the dimensions that matter to the test and record which others are approximate. A dummy without the real cable may give a misleadingly spacious impression.

In the pivot case study, the [interactive assembly](../../projects/triangulated-pivot/viewer/) can expose a hidden fastener or show where two parts meet. It is valuable for spatial understanding. It does not reproduce finger access, print texture, friction or the force required to assemble a real bearing. Use it to plan the next physical test.

## Make action and feedback legible

A user must discover what can be done, perform the action and recognize its effect. A recessed screw that resembles a pivot pin may invite the wrong action. A knob that turns without a visible change may leave the user uncertain whether it is locked. Shape, labels, movement limits and feedback can reduce those ambiguities.

Physical arrangement can communicate a relationship: a control located beside the axis it adjusts is easier to associate with that axis. A captured nut can make assembly less dependent on dexterity. A keyed shape can prevent an unintended orientation, but should not require force to reveal that orientation is wrong. Test with the actual use conditions, including visibility, reach and any gloves or tools involved.

Color can reinforce information, but pair it with shape, position or text. In the pivot viewer, named parts complement colors. In a physical device, a tactile stop or orientation mark can remain useful when lighting is poor. Design for the range of people and circumstances relevant to the job rather than assuming your own hands and familiarity represent everyone.

Don Norman's [The Design of Everyday Things](https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things/9780465050659/) is a deeper reading route for these human-centered questions. It complements the mechanical and electrical chapters; it does not supply their engineering validation.

## Consider the whole life of a part

Assembly order changes geometry. A bolt may fit its hole yet have no path into position after neighboring parts are installed. A driver may reach the head but lack room to turn. Draw the insertion path, tool envelope and hand access. Try the sequence with ordinary tools before adding decorative details.

Repair raises similar questions. Which part is most likely to wear? Can it be replaced? Are fasteners accessible? Are cables strained when the enclosure opens? Reducing part count can simplify assembly, but bonding everything permanently can make a minor failure expensive. Prefer a deliberate tradeoff over a universal rule.

A quick cost model also broadens the decision. In an illustrative batch of ten brackets, assume each uses 25 g of material at an assumed $25/kg, 20 minutes of machine time and 6 minutes of hands-on finishing. Material is about $0.63 per part. That is not the total cost: failed prints, machine ownership, inserts, packaging and your time still exist. If a redesign saves one minute of material deposition but adds five minutes of manual cleanup, the material-only comparison misses the main consequence. Substitute your own prices and measured times; these are planning numbers, not a purchasing quote.

## Lab: test an installation without coaching

Make two low-fidelity concepts for holding a harmless dummy sensor. Use card, tape and existing loose hardware only as nonloaded mockup elements. Do not rely on cardboard to restrain a powered or heavy device. Prepare a short instruction card and a clearly stated task, such as “Place the sensor against the reference and leave the connector accessible.”

Ask a willing adult to try one concept, then the other. Explain that you are testing the design, not the person. Observe their first action, requests for help, reversals and whether the task finishes. Avoid pointing out the intended sequence while the trial is underway. If something unsafe or damaging could happen, stop immediately; withholding help is not more important than the participant.

Afterward, ask what they expected each feature to do. Their explanation can reveal a mismatch you did not see. Record the exact observed difficulty, then change one feature and repeat. If you are working alone, put the prototype away and attempt it later from the instructions; recognize that this does not reproduce a new user's perspective.

Expected outcomes include discovering an ambiguous orientation, obstructed grip or missing instruction. A smooth trial is evidence for that participant and condition, not proof that all users will succeed. If neither concept produces a clear difference, choose a more demanding relevant task or retain the simpler adequate design.

## Check your understanding

**A user asks for a bigger knob. Should that become the requirement?** First identify the underlying difficulty: grip force, reach, visibility or insufficient torque may each suggest a different solution. Preserve the observation and test the need.

**The highest-scoring concept violates an essential access constraint. Can its other strengths compensate?** No. Rework or reject it before comparing preferences.

**What does a successful cardboard trial establish?** Evidence about the represented geometry and interaction under that trial. It does not establish printed strength, thermal behavior or long-term wear.

Your independent task is to revise one requirement after observing a real task, then build a prototype aimed only at the most consequential uncertainty. Keep the old requirement and explain the change. For a deeper project-based structure, [MIT's archived Product Design and Development course](https://ocw.mit.edu/courses/15-783j-product-design-and-development-spring-2006/) connects customer needs, concepts and manufacturing decisions. Its materials are a study resource; you supply the project, collaborators and feedback.
