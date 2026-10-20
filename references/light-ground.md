# Light ground (the approved background)

The user rejected black ("not fitting") and frosted glass ("it looks very bad"). They chose **clean light / off-white**, like the Wabi, ElevenLabs Flows and StateSync references. The root paints the ground; every frame stays transparent.

## Root (build it with `scripts/build_light_index.py`)
- Base `#F2F2F0`.
- **Two soft glows drifting along the bottom edge**, blurred 60–70 px:
  - `#glow-a`: 1500×760 at left 210, top 760. `radial-gradient(closest-side, rgba(150,140,255,.55), rgba(120,170,255,.28) 55%, transparent)`.
  - `#glow-b`: 900×600 at left 1250, top 820. `rgba(90,200,255,.38)`.
  - Tint them toward the brand colour, but keep them soft and pastel.
- One slow drift across the whole film: glow-a moves x +140, y −40, scale 1.12; glow-b moves x −220. Ease `sine.inOut`, duration = the film. Nothing moves at the seams.
- Optional grain PNG at opacity .18, `mix-blend-mode: multiply`.

## Colours on light
- **Text:**
  - Sentences: ink `#111114`. The accent word (serif italic) is ink too.
  - Ghost words: ink at 18 %. Secondary lines: ink at 55 %. Chapter tags: ink at 45 %.
- **No dark text shadows** (they look dirty on white). Over imagery, use a faint halo `0 0 18px rgba(242,242,240,.9)`, or place the line where the ground is clean.
- **Accent highlight pass:** a darker sweep (ink → violet #4A4AFF at 70 % → ink), subtle. **Smear fringe:** red/cyan at half strength.
- **Dark product objects** (a black pill, a dark app window) stay as they are; dark on white is the look. Give them a soft shape-hugging shadow: `filter: drop-shadow(0 18px 36px rgba(20,20,40,.18)) drop-shadow(0 2px 6px rgba(20,20,40,.12))`.
- **Logo on light:** the mark and wordmark become ink; the brand accent keeps its colour. The app icon tile stays as designed. Nothing square outside a rounded logo.
- **Things made to read on black** (paper rings, glints, hairline catch-lights, glows): switch to ink or violet at low alpha, or remove them. Remove full-frame dark scrims/vignettes, or turn them into a light veil `rgba(242,242,240,.6)`.
- **Real footage/wallpaper** goes in rounded windows (r 20–28) with the soft shadow above. Nothing full-bleed dark unless the story needs it; a "glass" moment may open full-frame.

## Vertical (9:16) version of the ground
In `scripts/social_cuts.py`, the film's middle sits between two strips stretched from the film's own top and bottom rows. The bottom strip then fades into the ground with a gradient, so the glow continues without a seam.
