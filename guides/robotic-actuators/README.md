# Robotic actuators — From load to motion

An illustrated design guide for makers learning mechanical robotics, Fusion, and actuator selection. The three shared studies are a belt-driven rotary joint, a horizontal screw stage, and a tendon-driven finger. The source uses the Invention Lab handbook's worked-example and experiment style.

## Rebuild

From the repository root, use Node 20 or newer and Python 3.10 or newer:

```sh
npm ci
npm run build:actuators
npm run validate:actuators
python3 -m unittest discover -s guides/robotic-actuators/examples -p 'test_*.py' -v
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000/projects/robotic-actuators/`. The build owns only `docs/projects/robotic-actuators/`; it never replaces the handbook or pivot. `scripts/package_actuator_guide.py` creates a deterministic archive, rewrites links to other site areas to online URLs, and checks the archive's file hashes and local navigation.

## Source layout

- `chapters/`: ten Markdown lessons, each with one H1 title. The renderer supplies chapter navigation and prefixes section IDs.
- `assets/`: original explanatory diagrams.
- `designs/`: native CAD envelopes, two-view DXFs, screenshots, parameter files, generators, and modeling notes. Read `designs/README.md` for scope and commands.
- `examples/`: standard-library Python calculation and analysis labs with behavioral tests.
- `worksheets/`: editable measurement records and explicitly synthetic sample data.
- `research/`: primary-source resource annotations with access, prerequisites, a first task, limits, and verification date.
- `web/`: presentation and three interactive teaching models. The source JavaScript is bundled into one local classic script for the portable page.

The source has no runtime service or remote JavaScript dependency. Browser testing uses HTTP previews. Offline packaging checks relative links, archive integrity and checksums directly; it does not claim a browser `file:`-URL test.

## Evidence boundary

The native files are editable component envelopes with explicit layout dimensions, not completed fabrication assemblies. Manual lessons teach constrained, parameter-driven modeling. Supplier-specific tooth profiles, threads, fits, mounting and retention details, wiring, guards, thermal limits, and load qualification remain further work. Calculation results validate the stated mathematical models; no physical actuator has been built or tested for this edition.

The public guide is at https://nicholashazen.github.io/invention-lab/projects/robotic-actuators/.
