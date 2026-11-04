# 18. AI and computer vision: build the test before trusting the prediction

A camera could help a bench rig find a fiducial, check whether a printed part is present, or record how far a loaded bracket bends. “Use AI” is not yet a specification. The useful question is what observation the system must make, under which conditions, with which consequences when it is wrong. A simple light threshold may solve the task more transparently than a trained network; a trained network may handle variation that a threshold cannot.

This chapter develops a small visual classifier and deliberately exposes its weakness under changed lighting. You will separate training from evaluation, calculate a confusion matrix, and define a sensible boundary between an AI assistant and a physical controller. You need the software/data chapter and basic fractions. The lab uses synthetic grayscale images and Python's standard library, so a camera, GPU, account, and machine-learning installation are unnecessary.

## Start with an observable decision

Suppose a printed coupon should carry a dark registration mark. The task is to classify a small image region as “mark present” or “mark absent.” A useful requirement might specify the camera distance, lighting range, allowed part rotation, minimum mark size, and acceptable false-accept and false-reject rates. It should also define what happens when the image is blurred or the part is outside the expected region.

The label is the answer assigned to an example, preferably from an independent inspection. The feature is a measured property used to make the decision: number of dark pixels, edge position, or a learned representation. The model maps features to a prediction. Training chooses the model's parameters from examples. Inference applies those fixed parameters to a new example.

Our baseline counts pixels darker than intensity 100 and predicts a mark when the count reaches a learned threshold. It is intentionally limited. It ignores whether the dark pixels form the right shape or occupy the right location. Naming those assumptions makes its failures useful. A complicated model without an explicit baseline can look impressive while offering no measurable improvement over a few understandable operations.

The baseline can also reveal that the physical setup needs improvement. A matte background, fixed camera mount, controlled illumination, and a repeatable part location may remove more variation than a larger model. Engineering the observation is part of computer vision.

## Separate learning from the final examination

A model evaluated on its training examples answers “Can this rule fit information it has already seen?” Deployment asks whether it works on a new part, session, or lighting condition. Keep a training set for choosing parameters, a validation set for choosing among approaches, and an untouched test set for the final estimate. With a tiny teaching dataset we use only training and held-out test records, and explicitly avoid tuning on the test results.

Data leakage occurs when information from the evaluation set influences training or model selection. It can be subtle. Adjacent video frames share almost the same object and background. Randomly dividing those frames places near-duplicates on both sides of the split. A high score can then measure recognition of a recording session instead of generalization to new parts.

Split according to the intended deployment uncertainty. If the system must work on newly printed parts, keep all images of one physical part in one group. If lighting changes between sessions, hold out entire sessions. Fit normalization parameters only on training data. Keep the final test labels out of the model-building loop, and record when a supposedly held-out dataset has become familiar enough that it is now effectively validation data.

Statistical learning provides the language for these distinctions. The authors' site for [An Introduction to Statistical Learning](https://www.statlearning.com/) offers the Python edition and chapter labs; its model assessment material is a useful next step after this deliberately small experiment.

## Accuracy can hide the failure you care about

Imagine inspecting 100 parts, of which 95 are acceptable and 5 have defects. A classifier that always says “acceptable” has 95% accuracy while detecting none of the defects. The number sounds strong because the common class dominates it.

Choose the positive class explicitly. In our lab, positive means “mark present.” A true positive is a present mark predicted present. A false positive is an absent mark predicted present. A false negative is a present mark missed. A true negative is a correctly rejected absent mark.

For eight held-out images, our classifier produces 3 true positives, 2 false positives, 2 true negatives, and 1 false negative. Therefore:

`accuracy = (3 + 2) / 8 = 0.625`

`precision = 3 / (3 + 2) = 0.600`

`recall = 3 / (3 + 1) = 0.750`

Precision asks how often a positive prediction is correct. Recall asks how many actual positives are found. Which matters more depends on the process. If a falsely accepted part causes an expensive assembly failure, false positives deserve special attention. If missing a valid mark merely asks an operator to inspect the image, that cost is different. State the decision cost rather than declaring one metric universally best.

Eight synthetic examples cannot estimate a production error rate with useful confidence. The counts teach the arithmetic and reveal failure mechanisms. Real evaluation needs representative independent examples, documented labels, and uncertainty appropriate to the sample size. A confidence score from a model is also not automatically a calibrated probability of correctness.

## Run an experiment that fails for an understandable reason

Download [vision_baseline.py](../examples/computing/vision_baseline.py), then run:

```sh
python3 vision_baseline.py
python3 vision_baseline.py --images vision-images
```

The first run prints a threshold of 3 dark pixels and training accuracy 1.000. On the held-out records it prints `tp=3 fp=2 tn=2 fn=1`, followed by accuracy 0.625, precision 0.600, and recall 0.750. The second run writes eight plain-text PGM image files. Each contains an 8-by-8 grayscale array with values from 0 to 255; even without an image viewer, a text editor exposes every pixel.

The training examples have bright backgrounds of 180 and mark pixels of 60. Negative examples contain zero, one, or two dark pixels; positive examples contain four, six, or eight. Several count thresholds classify all training records correctly. The code deliberately selects the smallest equally accurate threshold, 3. This tie-breaking rule is part of the experiment and makes the result reproducible.

The test set contains a true mark with only two dark pixels, causing the false negative. It also contains two images from a dim session with background intensity 80. Every pixel in those images now falls below the fixed darkness cutoff of 100. The classifier sees many dark pixels and reports a mark even when none is present. Those are the two false positives.

Read the session identifiers in `records()`. Training groups A and B are separate from test groups C and D. The [shared tests](../examples/computing/test_labs.py) verify this separation and the confusion counts. All images are synthetic fixtures created to isolate a mechanism; they are not photographs of successfully inspected printed parts.

Before changing the algorithm, write a prediction. Would a lower intensity cutoff distinguish a 60-valued mark from an 80-valued background? In this synthetic dataset, yes. Would that guarantee performance on real images? No: shadows, reflections, camera gain, blur, and material color could overlap those intensities. Once you use these test images to choose a new cutoff, they are no longer an untouched final test. Create a new held-out session to evaluate the revised hypothesis.

## From pixel decisions to geometric measurements

Finding a dark region and measuring a physical distance are different tasks. A pixel coordinate has no inherent millimetre scale. For a flat target at a fixed distance, a reference object in the same plane can provide a local scale. Move the target closer to the camera and the same physical length spans more pixels. Tilt it and foreshortening changes the apparent shape.

Lens distortion can bend straight edges, especially toward the image boundary. Camera calibration estimates the imaging model from known geometry; camera pose relates that model to the object or robot frame. The [OpenCV calibration tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) explains these separate parameters and a pattern-based workflow. A calibration is tied to the optical configuration; changing focus, image crop, or resolution requires checking whether the previous parameters remain valid.

For a first bench measurement, fix the camera, use a flat target, keep the reference scale in the measurement plane, and collect images at several known distances or positions. Compare the estimated distances against independent measurements. If the error grows near the edges, inspect distortion and perspective. If repeated measurements vary at one position, inspect lighting, blur, feature localization, and mechanical movement. Report the uncertainty rather than rounding a noisy estimate to many decimal places.

## A useful model must also fit the device

A laptop demonstration does not establish that a microcontroller or small single-board computer can run the same pipeline. Account for image capture, resizing, model inference, communication, and decision logic. If capture takes 20 ms, preprocessing 5 ms, inference 35 ms, and decision handling 5 ms sequentially, the end-to-end delay is 65 ms. That is more relevant to a moving target than quoting inference time alone.

Memory includes model parameters, intermediate activations, input buffers, and the rest of the application. Power and heat can reduce sustained performance. Quantization can reduce storage and computation but may alter the error distribution; re-evaluate the deployed representation. Measure worst-case or suitably high-percentile latency on the actual device, not only average speed on a development computer.

If you need learned visual features after establishing the baseline, [fast.ai's Practical Deep Learning for Coders](https://course.fast.ai/) offers an applied route for people who already write code. For a wider algorithmic foundation, [CS50 AI](https://cs50.harvard.edu/ai/) covers search, uncertainty, learning, and language; its stated prerequisite is CS50x or at least one year of Python experience. Neither is the first programming lesson, and external notebooks may require environment adjustments as dependencies change.

## Use language models as reviewable assistants

A language model can help explain an unfamiliar function, suggest tests, summarize a log, or draft an implementation. Its fluent answer is not a measurement. Ask for assumptions, units, input/output examples, and a way to falsify the proposed result. Run generated code against known fixtures and inspect the operations that touch files, credentials, networks, or devices.

For physical projects, keep an LLM outside the direct actuator-control path. Let it propose a plan or bounded configuration for human review; deterministic software should enforce ranges, timing, interlocks, and stop behavior. Sensor text, web content, and retrieved documents can contain misleading instructions, so treat them as data rather than authority to alter a machine's permissions.

An assistant that proposes moving to `(x, y)` still needs a valid frame, reachable geometry, collision checks, a permitted state, and a tested motion controller. A natural-language assurance cannot replace any of those. Use the same discipline as for another contributor's code: review the change, reproduce the result, and retain the evidence.

## Check the claim before extending it

**Predict:** Why can 100% training accuracy coexist with poor deployment? **Answer:** The model can fit the available examples while relying on a condition, such as lighting, that changes later. Training performance does not test independence or coverage.

**Predict:** Is a random frame split adequate for a camera recording one part? **Answer:** Usually not for estimating performance on new parts; near-duplicate frames leak shared information across the split.

**Predict:** A vision model reports a point with 0.99 confidence. May the robot move there immediately? **Answer:** No. The point still needs a timestamp, frame transformation, uncertainty and workspace checks, and authorization through the deterministic motion system.

For an independent project, photograph five distinct paper fiducials over several sessions using a fixed camera. Keep one entire session untouched. Compare a threshold baseline with a shape-based rule, documenting lighting, labels, false positives, and false negatives. Stop at an on-screen inspection result. Your deliverable is a reproducible evaluation and failure gallery; connecting the result to motion is a separate integration project with additional checks.
