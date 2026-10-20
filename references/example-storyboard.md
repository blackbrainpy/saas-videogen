---
title: <Product>, launch film (~60 s)
format: 1920x1080
fps: 30
duration: <45–60>
music: assets/music/score.mp3 (fitted with arrange_music.py: short intro · stab phrase · steady pulse · silence · finale), root, volume 0.7
voice: none: on-screen text tells the story
style: .kinetic/light-ground.md + .kinetic/type-motion.md
---

# The brief (quote the user verbatim)
"<the user's own words>". Length 45–60 s, on-screen text only.

# Notes (win over the prose below)
- **Clarity first.** By ~8 s a new viewer knows *what* it is and *why* they'd want it. Then each feature beat names one feature plainly in its first line.
- **Hand-over state:** unless a frame says otherwise, every frame starts from and ends on <your object>. For example, a black pill 624x120, r60, #0B0B0C, 1 px white @ 8 % hairline, centred at 960,540, with the soft shadow from light-ground.md.
- **Copy:** only what is written here. Facts come from the product's own notes or site. No invented numbers.
- **Third parties:** logos visible in real captures get covered; personal data gets blurred.
- **BEAT LOCK:** every frame has a BEAT LOCK line, and it wins over the prose. If a BEAT LOCK time is not within ±0.05 s of a hit in the packet's hit map, snap that event to the nearest A or B hit.

# Score map (fill from beat_map.py)
Intro to <t0>. Stab phrase at <t1> (the logo reveal lands on its first hit). Steady pulse <a–b> (feature beats). Silence <c–d> (proof). Finale hits <…> (end card).

## Frame 1 — Hook: what it is (~7 s)
- src: compositions/frames/f01-hook.html
- start: 0.000
- duration: ~7
- assets: a real clip of the product in use, in a rounded window
- BEAT LOCK:
  - L1 lands on the first hits.
  - The real product fades up behind/under the text; L2's accent lands on the biggest early A hit.
  - The last word slides to the centre, breaks into pixels and implodes into ONE brand pixel (the logo switch, code in `examples/demo/compositions/frames/d01-open.html`). Hold.
- Copy:
  - L1: "<what it holds or does, 3–5 nouns or a sharp claim>."
  - L2: "<Product> keeps them in one *<place>*." (end on the word that breaks)

## Frame 2 — The name (~5 s)
- starts from the brand pixel (code: `d02-name.html`)
- BEAT LOCK: tiles burst out of the pixel on the reveal A hit · the logo assembles · the outline closes · the wordmark letters assemble · the definition line tumbles in · collapse into the hand-over object.
- Copy: lockup "<Product>" · line: "A <category> for *<platform/audience>*."

## Frames 3–7 — Feature beats (4–6 frames, 5–7 s each, on the steady pulse)
For each frame:
- the first line names the feature plainly, e.g. "*Pin* the things you paste every day."
- a real capture or rebuilt state of it in use, morphing out of the hand-over object and back into it
- at most one small proof line

Order: the most loved feature first, then alternate big visual moments with quieter utility ones. End on customisation ("Make it *yours*.") if the product has it.

## Frame 8 — Proof (optional, 2–3 s, in the music silence)
- One real measured fact typed in, with `key` cues (e.g. "<n>% CPU at idle"), and a small note on how it was measured.

## Frame 9 — End card (~8 s, on the finale hits; code: `d03-end.html`)
- The hand-over object becomes the app icon → wordmark → small facts line → price/offer line with one accent → a button pill with a press → URL typed character by character. Hold for 2–3 s.

Timing check: 7 + 5 + (4–6 × 5–7) + 0–3 + 8 = 45–60 s.
