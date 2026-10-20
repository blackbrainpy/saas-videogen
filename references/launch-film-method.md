# Launch film method (the approved default)

This method produced a real 2:10 launch film that its maker approved as final (Oct 2026). It is music-led, with no voice, on a clean off-white ground. This skill applies the method to 45–60 s films only. Its predecessor, the 61 s "pro" cut on black, got the "Absolute Cinema" verdict. The light cut then took the same method and fixed everything the user disliked.

A working demo (opening line, logo switch, end card) is in `examples/demo/`, and a 60-second storyboard template is in `references/example-storyboard.md`. Open the demo frames when you need working code for a move.

## What the user rejected, and so must never come back
- A black ground ("not fitting") and frosted glass ("it looks very bad"). Use clean off-white with soft colour glows; see `light-ground.md`.
- Stock caption-style type. Use the reference type system (Geist + Instrument Serif Italic accent, tumble-in etc.); see `type-motion.md`.
- Sound "too low quality, boring and repetitive and forced": a tick on every word, and the same whoosh + click closing every scene. Use a sparse, meaningful sound design from a real library; see § Sound.
- Cutting on every line like a slideshow. Morph one object through every scene; see § Continuity.
- AI-generated footage or people ("AI slop"). Use real product recordings and screenshots only.

## Length: 45–60 seconds, always
The skill makes one film length: 45–60 s. If the user asks for something longer, make a 60 s film and offer vertical cuts. A tour of every feature doesn't fit; pick the 4–6 features that sell the product.

| Output | Length | Use |
|---|---|---|
| Launch film | 45–60 s, 8–10 frames | Store trailer, site hero, Product Hunt, YouTube |
| Vertical social cuts | 12–20 s each, 3–4 clips | Reels / TikTok / Shorts, cut from the film (`scripts/social_cuts.py`) |

### Structure (see `references/example-storyboard.md`)
1. **0–~7 s: hook, what it is.** One plain line over the real product (what it holds or does), then a second line whose last word does the **logo switch** (§ Logo switch).
2. **~7–12 s: the name.** Logo builds from the pixel, wordmark + a one-line definition, collapse into the hand-over object.
3. **~12–48 s: 4–6 feature beats, 5–7 s each,** on the music's steady pulse. The first line names the feature plainly, then a real capture or rebuilt state of it in use. Every beat starts from and ends on the shared hand-over object.
4. **Proof beat (optional, 2–3 s)** in a music dropout: one real measured fact typed into the silence (e.g. "0% CPU at idle", with the measuring note in small type). Only numbers the user measured.
5. **End card (~8 s):** app icon → wordmark → small facts line → offer line → a store button pill → URL. It lands on the finale hits and holds for 2–3 s.

## Continuity: one object morphs through everything
- Pick the product's own shape as the hand-over object. The original film used its product's black pill: 624×120, r60, #0B0B0C, a 1 px white@8 % hairline, centred, and on light also `box-shadow: inset 0 0 0 1px rgba(255,255,255,.08), 0 18px 36px rgba(20,20,40,.18), 0 2px 6px rgba(20,20,40,.12)`.
- For an app with a window, use a small rounded window card; for a logo-led brand, use the mark.
- Write the exact hand-over state (px position, size, radius, colour) into the storyboard's notes. Every frame starts from it and ends on it. Then neighbouring frames match pixel for pixel and you need no transition layer.
- Scene changes are morphs: the object expands into a card, bursts into tiles, wipes light across, or collapses back. Keep hard cuts under ~4 per minute.

## Logo switch (the user asked for this one again by name)
The last word of the opening sentence breaks into pixels, which implode to one brand-colour pixel, and the logo builds out of that pixel.
- **Opening frame end (e01, last ~1.2 s):** the final word (e.g. "opens.") splits into ~64 ink squares (8–10 px). They drift outward 20–40 px, then implode to the centre and merge into one brand-colour square (40×40, r4) by +0.45 s. Hold it on the beat until the frame ends.
- **Name frame start (e02):** begin from that same pixel at the same position. On the reveal hit, ink tiles burst out of it (seeded random directions, rotation ±25°) and land into the logo's grid by +0.3 s. A capsule/outline closes around them at +0.5 s, then the wordmark letters assemble and the definition line tumbles in. At the end, the lockup collapses into the hand-over object.
- **Sound:** a pixel crackle on the break, a soft pop as the cyan pixel forms, a reverse swell ending exactly on the reveal hit, then a deep swoosh + impact on the reveal.
- Working code: `examples/demo/compositions/frames/d01-open.html` (the break) and `d02-name.html` (the build).
- Logo rule: nothing square outside a rounded logo (see the user's memory "Logo round edges"). The pixel N tiles are ink on light; the accent pixel keeps the brand colour.

## Music
- Generate 3 options (Gemini "Create music", instrumental, ~80–95 bpm). Use a clean electronic/cinematic brief: a near-silent intro, glossy stabs, a sub pulse and clear dropouts. Let the user pick.
- `scripts/track_fit.py` compares candidates. `scripts/arrange_music.py` re-arranges the chosen track to the film length (intro · stab phrase ×N · steady pulse ×N · silence · finale).
- Plan the structure around the music: big reveals land on the stab phrase's opening hit, feature chapters ride the steady pulse, and the proof beat sits in the silence.
- `scripts/beat_map.py <music> STORYBOARD.md .kinetic/beats.md` grades every onset A/B/C and writes per-frame hit tables. Every storyboard frame gets a `BEAT LOCK:` line; snap events to the nearest A/B hit within ±0.05 s.
- Music sits at root volume ~0.7.

## Sound (rebuilt after the user's "forced, repetitive" feedback)
- **Library:** `assets/sfx-library/` in this skill. 41 ElevenLabs takes (free plan) across 11 categories, 3–4 takes each, peak-normalised; one of the 42 files (tap_1) is a muddy take the script skips. The prompts to regenerate or extend it are in `assets/sfx-library/PROMPTS.md`. Fixed 2.0 s duration costs 80 credits; Auto costs 200.
- **Cue lists, not audio tags.** Frame workers don't put `<audio>` in frames. Each worker writes `.kinetic/sfx/<frame-id>.json` with only the meaningful moments: `[{"t": 0.52, "cat": "snap", "why": "card opens"}]`. Film-level cues go in `.kinetic/sfx/_film.json` (film time): swooshes into the stab phrases, the end impact.
- `scripts/sound_design.py <project>` merges the cue lists using the frame starts from index.html. For each sound it:
  - thins the list (per-category spacing, max 2 sounds per 0.3 s, the bigger sound wins)
  - rotates the takes, with ±1–1.5 semitone pitch and ±1.2 dB level jitter
  - aligns each take on its own transient (swells and swooshes on their peak)
  - loudness-matches it to the category's target
  
  It renders ONE track, `assets/sfx-mix.wav`, which goes in index.html at volume ~0.85. Many `<audio>` tags make the HyperFrames audio mix fail on Windows ("spawn ENAMETOOLONG"); one track avoids that.
- **What gets a sound:**

  | When | Category |
  |---|---|
  | A panel/card opens or locks | snap |
  | Something enters the frame fast | swipe |
  | A real key or button press | key |
  | A small element appears or lands | pop |
  | Glass or a light sweep | shimmer |
  | A reminder, notification or "done" | chime |
  | Logo pixels | pixels |
  | Into a big reveal | swell (ends on the hit) |
  | Big reveal | swoosh + impact |
  | Typing in the silence | key, every ~0.1 s |

- **What never gets a sound:** words of text, every beat, the closing of every frame, hover states.
- **Density:** the approved film averaged ~0.95 sounds/s (a 60 s film: ~50–60 cues). Over ~1.5/s in a frame reads as forced again.

## Render, export, deliver
- Lint: `npx hyperframes lint` (0 errors; file-size warnings are fine). Snapshot the joins (`npx hyperframes snapshot --at …`), especially the logo switch and the end card.
- Render: `npx hyperframes render --quality high --video-frame-format jpg --output renders/<name>.mp4`. Set TEMP/TMP to a roomy drive. ~6 min for 2:10 on the user's laptop.
- Export: two-pass loudnorm to −15 LUFS (see `scripts/export.py`), then a frame sheet; look at it. Deliver to a clear folder (e.g. `<Product>-Launch-Videos/`) and give the full path.
- Social: `scripts/social_cuts.py <film.mp4> <cuts.json> <out>` makes 9:16 clips. Each has a hook line on top, the film's centre in the middle, the glow fading into the ground, and the end-card tail. All are SAR 1:1 with bt709 tags; X and Instagram reject anything else. Then pull 10–12 PNG stills at settled moments (not mid-animation) for image posts.
- Always mention licence caveats: Gemini music and ElevenLabs free-plan sounds have no commercial licence.

## Review checklist (look at the frames yourself)
- [ ] A stranger knows what the product is by 0:20.
- [ ] Every scene change is a morph through the hand-over object; joins match pixel for pixel.
- [ ] Off-white ground everywhere; nothing full-bleed dark unless the story needs it.
- [ ] One accent word per line (serif italic); sentence 54 px; ≥60 % empty canvas.
- [ ] Only real product states and footage. Third-party logos in captures are covered; personal data is blurred.
- [ ] Every claim comes from the user, their site or their app. No invented numbers.
- [ ] Sound ~1 per second at most, only on meaningful moments, ~8–10 dB under the music.
- [ ] Social cuts: ffprobe shows 1080x1920, SAR 1:1, bt709.
