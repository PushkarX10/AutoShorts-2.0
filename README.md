# WHAT IF? — Space & Planet Exploration AutoShorts

> An autonomous, 100% free AI video automation platform creating broadcast-ready 2D vector animated space survival Shorts (1080×1920, 30 FPS, vertical 9:16) with scientific infographics, Mission Control telemetry HUDs, and interactive community voting cliffhangers.

---

## 🌌 Central Channel Concept

> **"WHAT IF YOU ACTUALLY LIVED THERE?"**

- *What if you lived on Mars for 30 days?*
- *What if you were born on the Moon?*
- *What if you fell into Jupiter?*
- *What if you survived inside a black hole?*
- *What if Earth had two moons?*
- *What if you lived on Titan?*

---

## 🎨 Visual Identity & Directorial Rules

1. **2D Vector Stickman Universe:**
   - Recurring astronaut stickman protagonist with circular light helmet (`#F5F6F8`), cyan reflective bubble visor (`#55D7E8`), chest life-support module, oxygen backpack with dual hoses, and chunky boots.
   - Poses: `walk_explore`, `low_gravity_jump` (buoyant 0.38g / 0.16g parabolic arc), `check_telemetry` (wrist hologram display), `enter_airlock`, `panic_o2` (gasping with blinking suit alarm), `point_sky`.
   - Strictly avoids photorealistic AI images, 3D, and generic stock illustrations.

2. **Controlled Space Color Palette:**
   - Space Black: `#080B14`
   - Deep Space Navy: `#10182A`
   - Midnight Blue: `#182744`
   - Steel Blue: `#536780`
   - Planetary Orange: `#F18B45`
   - Mars Red: `#C65B45`
   - Electric Cyan: `#55D7E8`
   - Solar Yellow: `#FFD36B`
   - Oxygen Green: `#7BD69A`

3. **Zero Text Overlap & Safe Screen Zones:**
   - **Mission Control Telemetry HUD:** Anchored at `top: 70px` (real-time O2 meter, temperature, gravity, mission timer).
   - **Visual Action Field:** Characters and scientific infographics bounded between `y: 260px` and `y: 1280px`.
   - **Kinetic Subtitles:** Positioned at `bottom: 110px` (`y: 1670px – 1810px`) with **390px+ clearance**, completely avoiding visual interference.

4. **Interactive Audience Decision Ending:**
   - Every Short ends with two high-stakes survival options:
     - `[ A ] BRAVE THE STORM`: Manual repair, high suit breach risk.
     - `[ B ] CRYO-HIBERNATE`: Heaters cut, sleep pod hypothermia risk.
   - Prompts audience comments to decide the outcome in Part 2.

---

## 🛠️ Free Autonomous Tech Stack

- **Narrator Audio:** Microsoft Edge-TTS (`en-US-ChristopherNeural`, `+9%` rate).
- **Audio Mixing & Mastering:** FFmpeg complex filter combining voice, ambient space tension score, and sound effects.
- **Animation & Video Engine:** Remotion 4.0 React composition (1080×1920, 30 FPS).
- **Cost:** 100% Free (no paid APIs or subscriptions).

---

## 🚀 Terminal CLI Usage

Run directly from the terminal without needing any dashboard or web UI:

```powershell
# List supported planetary databases and physical constants
py -3.12 -m autoshorts2.space.cli list-planets

# Generate a Mars exploration short
py -3.12 -m autoshorts2.space.cli generate "What if you lived on Mars for 30 days?" --planet mars

# Generate a Moon exploration short
py -3.12 -m autoshorts2.space.cli generate "What if you were born on the Moon?" --planet moon

# Generate a Jupiter exploration short
py -3.12 -m autoshorts2.space.cli generate "What if you fell into Jupiter?" --planet jupiter
```

---

## 📂 Project Structure

```text
AutoShorts2.0/
├── autoshorts2/
│   ├── space/
│   │   ├── planet_data.py          # Scientific database (gravity, atm, temp, hazards)
│   │   ├── pipeline.py             # 4-stage autonomous production pipeline
│   │   └── cli.py                  # Terminal command-line interface
│   ├── assets/
│   │   ├── bgm/                    # Tension and curiosity ambient scores
│   │   └── sfx/                    # Radio static, whoosh, scan, alarm, impacts
│   └── voice/                      # TTS and subtitle generation
├── renderer/
│   ├── src/
│   │   ├── components/
│   │   │   └── space/
│   │   │       ├── AstronautStickman.tsx # Articulated 2D vector stickman
│   │   │       ├── SpaceEnvironment.tsx # Handcrafted vector environments
│   │   │       ├── SpaceHUD.tsx         # Mission Control telemetry
│   │   │       └── SpaceCaptions.tsx    # Safe-zone kinetic subtitles
│   │   ├── WhatIfAnimatedShort.tsx      # Main Short composition
│   │   └── Root.tsx                     # Remotion root configuration
│   └── public/                          # Static assets and audio
├── output/                              # Rendered 1080x1920 MP4s and stills
└── projects/                            # Project metadata and timings
```
