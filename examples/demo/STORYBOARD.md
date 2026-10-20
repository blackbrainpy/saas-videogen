---
title: Lumen, demo (opening, logo switch, end card)
format: 1920x1080
fps: 30
duration: 18.5
music: none in the demo (add your own score at root volume ~0.7)
voice: none: the on-screen text tells the story
style: .kinetic/light-ground.md + .kinetic/type-motion.md
---

# The brief
A fictional product, "Lumen, a focus timer for your desktop". It shows the three signature pieces of the method:
the opening line, the **logo switch** (the last word breaks into pixels → one brand pixel → the logo builds from it),
and the end card. A real film puts the 20-second "what it is" opening and the feature chapters between them
(see `references/example-storyboard.md`).

# Notes (win over prose)
- **Hand-over states:**
  - d01 ends on ONE brand pixel: 40x40, r4, #6C5CE7, centred at 960,540, soft shadow.
  - d02 ends on the pill: 624x120, r60, #0B0B0C, 1 px white @ 8 % hairline, centred, with the soft shadow.
  - d03 starts from that pill.
- Type: Geist Medium 54 px ink #111114; one Instrument Serif Italic accent per line at 1.18x.

## Frame 1 - The opening line
- src: compositions/frames/d01-open.html
- start: 0
- duration: 6
- BEAT LOCK: "Start the timer." tumbles in on 0.20 · "Stay in" on 1.40 · accent *flow.* blooms on 1.80 · 3.20 reduce-to-keyword ·
  tension build 4.30-4.80 · 4.80 the word breaks into pixels · 5.08 the brand pixel is born · hold to 6.0
- Copy: L1 "Start the timer." · L2 "Stay in *flow.*"

## Frame 2 - The name
- src: compositions/frames/d02-name.html
- start: 6
- duration: 5.5
- BEAT LOCK: 0.05 tiles burst out of the pixel · 0.34 the letter is complete · 0.52 capsule closes, lockup · 1.50 wordmark lands ·
  1.70 punch · 2.60 line tumbles in · 3.00 accent *desktop.* · 4.20 reduce-to-keyword · 4.95 collapse into the pill (lands 5.35)
- Copy: wordmark "Lumen" · line "A focus timer for your *desktop.*"

## Frame 3 - End card
- src: compositions/frames/d03-end.html
- start: 11.5
- duration: 7
- BEAT LOCK: 0.00 pill → app icon · 0.42 glyph · 0.90 wordmark · 1.60 facts · 2.10 price line · 3.00 button · 3.60 press · 3.95 URL types
- Copy: "Works offline · No account · Mac and Windows" · "*Free* for 14 days." · button "Get Lumen" · "lumen.example"
