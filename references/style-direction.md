# Style direction — kinetic cut (template)

Copy this file to `<project>/.kinetic/style-direction.md`, replace every `{…}` with the brand's values, and delete lines that don't apply. Every frame worker reads it; it is the style truth for the film.

## The film
{One paragraph: product, the one message, audience, tone. E.g. "A 55-second launch film for <product>, a <what it is>. Upbeat, premium, fast. The viewer should leave knowing <message>."}

## Moves to use (the kinetic vocabulary)
- **Narration is the typography.** Each spoken word appears on its timestamp, large, by blurring in (blur 16px→0, opacity 0→1, y +28→0, scale 1.04→1, ~0.35 s, power3.out). Show the current phrase, not a transcript: when a new phrase starts, the previous one blurs out upward (blur →12px, opacity →0, y →−24, ~0.25 s). Place words where the frame's layout wants them, never in a caption box.
- **Inline glossy icons inside the sentence** next to key nouns: drawn in SVG, rounded, brand-gradient body, lighter top highlight, rim light, soft drop shadow, slight 3D tilt; spring-pop in with the word (scale 0→1.12→1, rotate −12°→0), optional glow ring and glint. Draw them yourself — no emoji, no third-party logos.
- **Camera through type:** a giant word the camera zooms THROUGH (scale 1→9+, blur rising) into the next shot; footage can show inside the letters just before (knock-out).
- **Letter scramble / glitch decode** on numbers and short words (deterministic glyph swaps by timeline time; a brief chromatic split that snaps clean).
- **3D extruded numerals** for hero numbers (8–12 stacked offset layers, brand colour → base colour, front face light gradient); numbers **count** with ticks.
- **Floating product windows:** footage/screenshots in rounded windows that fly in from depth with a CSS 3D tilt (rotateY ~22°, rotateX ~8°, translateZ, blur → settle near flat), glow shadow beneath, slow drift while held; sets of features as a perspective **card wall**.
- **Full-bleed footage** gets a fast push-in and a 0.12 s blur-in at each cut.
- **CTA:** logo flips in with depth and bloom; price counts up; a frosted "slide to get" pill whose knob slides across and completes with a check ("Get it ✓") and a chime.
- **Pace:** something new every 0.6–1.2 s; one held, calm beat before the end card.

## Palette and type
- Base (root, behind everything): `{#050B16}` with a drifting aurora of `{#bloom1}`, `{#bloom2}`, `{#bloom3}` and a faint `{#highlight}` — painted by the root, not by frames. Frames are transparent; use partial ink scrims (gradients) where type sits over busy footage.
- Text `{#F4F8FF}`; emphasis `{brand colour}` or text with a brand-coloured glow (text-shadow 0 0 24px); muted text at ~55 % opacity.
- Display + narration font `{Brand font}` from `assets/fonts/{file}.woff2` (declare @font-face in every frame); mono `{mono font}` for tiny labels.
- {Brand rules: words never to use, colours the client dislikes, claims that need a footnote, etc.}

## Footage and images
Plain `<video id="fNN-…" class="clip" src="assets/<clip>.mp4" muted playsinline data-start="S" data-duration="D" data-track-index="T" [data-media-start="M"]></video>` (or `<img>`) inside an untimed wrapper div that GSAP animates; timing only on the video, never also on the wrapper. Keep `data-media-start + D ≤ clip length`. Don't toggle CSS `visibility` on anything (it escapes the frame's clip gating); use opacity.

## Sound design
Every visual event gets a sound: `<audio id="fNN-…" src="assets/sfx/<name>.mp3" data-start="S" data-duration="D" data-track-index="T" data-volume="V"></audio>` inside the frame (frame-local seconds, one per track, tracks ≥ 50, D ≤ file length). At most ~3 overlapping. Kit (lengths from the project's sfx folder):

| sound | use | volume |
|---|---|---|
| whoosh-fast | frame starts, fast moves, cuts | 0.30–0.35 |
| swoosh-soft | big scene moves, camera through type | 0.30 |
| swoosh-reverse | sucks into a hit — start it ~1.5 s before the hit | 0.30 |
| riser | short build into a reveal | 0.30–0.35 |
| pop | icons, chips, cards appearing | 0.25–0.30 |
| click | presses, toggles, the CTA knob | 0.30–0.35 |
| tick | every number change, list rows, small accents | 0.22–0.28 |
| counter-roll | a number counting (trim to the count) | 0.30 |
| glitch | scramble/decode (trim to ~0.5 s) | 0.25–0.30 |
| typing | typed text | 0.25 |
| impact | hero number / logo slam | 0.45–0.55 |
| shimmer | logo, sparkle, shine sweeps | 0.20–0.35 |
| chime | success moments, the CTA completing | 0.35 |

## Motion grammar
power3/power4.out entrances, expo.inOut camera moves, overshoot only on icon pops. Reveal on the spoken word. Holds keep subtle life (drift ≤ 2 %, a shine sweep), never freeze dead. Seek-safe GSAP only (fromTo with explicit from-states, no Math.random/Date.now, finite repeats).

## Keep-out
No caption band; keep important content inside x 60–(W−60), y 40–(H−80). For 9:16, keep the top 10 % and bottom 15 % clear of key text (platform UI).
