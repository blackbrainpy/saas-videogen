---
title: <Product>, extended cut (every feature, ~2:10)
format: 1920x1080
fps: 30
duration: 130.35
music: assets/music/score.mp3 (arranged with arrange_music.py: intro · stab phrase x3 · steady pulse x3 · silence · finale), root, volume 0.7
voice: none: on-screen text tells the story
style: .kinetic/light-ground.md + .kinetic/type-motion.md
---

# The brief (quote the user verbatim)
"<the user's own words>". Length ~2 min, on-screen text only.

# Notes (win over the prose below)
- **Clarity first.** A new viewer must understand within ~20 s:
  - *what* it is (one plain line over the real product)
  - *what it holds or does* (a short list)
  - *how* you use it (one sentence)
  - *why* (one line about the viewer's day)

  After that, each chapter is one feature, named plainly in its first line.
- **Chapter tag:** every feature chapter opens with a tiny tag top-left at x 96, y 84: Geist Mono 20 px, ink 45 %, e.g. "04 — <FEATURE>".
- **Hand-over state:** unless a frame says otherwise, every frame starts from and ends on <your object>. For example, a black pill 624x120, r60, #0B0B0C, 1 px white @ 8 % hairline, centred at 960,540, with the soft shadow from light-ground.md.
- **Copy:** only what is written here. Facts come from the product's own notes or site. No invented numbers.
- **Third parties:** logos visible in real captures get covered; personal data gets blurred.
- **BEAT LOCK:** every frame has a BEAT LOCK line, and it wins over the prose. If a BEAT LOCK time is not within ±0.05 s of a hit in the packet's hit map, snap that event to the nearest A or B hit.

# Score map (fill from beat_map.py)
Stab phrase plays at <t1>, <t2>, <t3>. Steady pulse at <…>. Silence <a–b>. Finale hits <…>.

## Frame 1 — What it is
- src: compositions/frames/e01-what.html
- start: 0.000
- duration: ~12
- assets: a real clip of the product in use, in a rounded window
- BEAT LOCK:
  - L1 cascades on the first hits; L1 greys out.
  - The real product fades up behind/under the text.
  - L2 lands, with its accent on the hook's biggest A hit.
  - L3 lands while the product is used (a click/hover in the clip).
  - The last word slides to the centre, breaks into pixels and implodes into ONE brand pixel (the logo switch). Hold.
- Copy:
  - L1: "<what it holds, as a list of 3–5 nouns>."
  - L2: "<Product> keeps them in one *<place>*…"
  - L3: "…<how you use it, ending on a strong verb>."

## Frame 2 — The name
- starts from the brand pixel
- BEAT LOCK: tiles burst out of the pixel on the reveal A hit · the logo assembles · the capsule/outline closes · the wordmark letters assemble · the definition line tumbles in · hold through the silence · collapse into the hand-over object.
- Copy: lockup "<Product>" · line: "A <category> for *<platform/audience>*."

## Frame 3 — Why you'd want it
- assets: 5–6 real product states (small, ≤ 520 px wide)
- BEAT LOCK: the states fan out around the hand-over object, one per hit · "Everything you <verb> all day." · swap to "One *glance* away." while the states pull in · fold back into the object.

## Frames 4–16 — One chapter per feature (5–9 s each)
For each frame:
- chapter tag
- first line names the feature plainly, e.g. "*Pin* the things you paste every day."
- a real capture or rebuilt state of it in use
- one small proof line
- start and end on the hand-over object
- BEAT LOCK on the steady pulse

Order: the most loved feature first, then alternate big visual moments with quieter utility ones. End on customisation ("Make it *yours*.").

## Frame 17 — Proof (in the music silence, 2–3 s)
- One real measured fact typed in, with `key` cues (e.g. "<n>% CPU at idle"), and a small note on how it was measured.

## Frame 18 — End card (10–13 s, on the finale hits)
- The hand-over object becomes the app icon → wordmark → small facts line → price/offer line with one accent → a button pill with a press → URL typed character by character. Hold for 2–3 s.
