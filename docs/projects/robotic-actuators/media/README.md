# Original mechanism motion clips

These three **silent schematic animations** accompany the actuator guide. They are original drawings generated from the stated kinematic relationships. They are neither physical test footage nor CAD dynamics simulations.

| Clip | Watch for | What it helps compare |
| --- | --- | --- |
| `motion-belt.mp4` | Three input turns produce one output turn through a 20T:60T open belt | Motor placement, speed/torque trade, elasticity and support loads |
| `motion-screw.mp4` | A guided nut advances 50 mm during 25 turns of a 2 mm/rev screw | Force leverage, required motor speed, friction, backlash and separate guidance |
| `motion-tendon.mp4` | A 60° finger rotation shortens the wrapped arc by 10.47 mm while an 8 mm spool winds 75° | Remote motor placement, constant effective radius, routing, slack and compliance |

Every clip is 12 seconds, 1280×720 pixels, H.264 with a widely supported `yuv420p` pixel format, and 24 frames per second. The files contain no audio track. Motion timing is chosen for explanation, not as the guide's commanded motion profile. Each poster shows the end state; press Play to see the change.

Matching `.vtt` files provide timed captions. The `*-transcript.md` files describe the full motion, assumptions and tradeoffs in text. `manifest.json` supplies guide-relative paths and teaching notes for the website. Native video controls provide playback, pause, scrubbing and fullscreen; the page should not autoplay these clips.

## Regenerate

Use Python 3.10 or newer with Pillow, plus `ffmpeg` and `ffprobe` available on your PATH. The script looks for Arial on macOS/Windows or DejaVu Sans on Linux. Add your font path in `load_font()` if neither is available.

```sh
python3 generate_motion_media.py
```

The script writes clips, posters, caption files, transcripts and the manifest beside itself. It streams frames directly into ffmpeg and leaves no intermediate frame directory. Use `--only belt`, `--only screw`, or `--only tendon` to regenerate a single clip. Keep the remaining clips when using that option; the manifest always lists all three.

The generator verifies the encoded duration, frame count, resolution, codec and pixel format. The released files were also decoded with ffmpeg and selected frames were visually inspected. These checks validate the media and its stated mathematical relationships, not the capacity or behavior of a real mechanism.
