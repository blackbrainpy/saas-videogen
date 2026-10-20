# Pro SaaS motion study (Oct 2026)

Six references the user picked as "professional SaaS motion graphics", broken down frame by frame
(sheets in `<repo>/videos/_ref/pinterest/analysis/`). Our Kinetic-v3 cut was judged "not professional"
next to them. These are the rules that separate them from it. Read this before writing a storyboard.

| # | Film | Look | Voice |
|---|------|------|-------|
| p1 | Polestar (Best Design Awards ident, 5 s) | one word repeated in a 3D tunnel, light-leak colour cycling | none |
| p2 | Wabi (76 s) | off-white #F0F0F0, black type, rebuilt app UI cards, glass sphere | none |
| p3 | ElevenLabs Flows (34 s) | white, node canvas, one pink accent | VO |
| p4 | Wix Harmony (86 s) | pastel blue/green gradient, UI + editorial photos | VO |
| p5 | Synaps (80 s) | pure black, glossy blue 3D ribbons, rebuilt dark UI in perspective | none |
| p6 | Bleap (29 s) | black, blue/violet light, italic-serif accent words | none |

## 1. Morph, don't cut
Measured shot lengths: Flows has **zero hard cuts in 34 s**, Synaps holds one shot for 49 s, Wabi has 2 cuts in 76 s.
Every scene change is an object turning into the next object:
- "Introducing" → "Flows" (blur-in, purple tint) → the word gets a white pill behind it → the pill shrinks to a chip → the chip becomes a node card on a canvas → camera pulls back to the whole canvas.
- Bleap: the logo symbol draws as an arc → becomes a glyph → the glyph moves left and the wordmark types out.
- Flows: the "Run" button → lines leave it → the lines become the logo's two bars.
- Bleap: a light shape grows until it fills the frame, and the next sentence is written on the light (a **light wipe**).
Our film cut on every voice line, which is why it read as a slideshow.

## 2. Restraint is what makes it look premium
- **One idea per screen.** A sentence sits alone in the middle with ~70% empty canvas.
- **Sentence type is small** (about 3–4% of frame height); only a single hero word goes huge ("Finally", "Instantly", "Grow", "Read|").
- **One typeface** (geometric grotesk), with one accent device: a colour word (Synaps blue "change", "architectural"), an italic serif word (Bleap "*evolved*", "*rebuilt*", "*crypto*") or a highlight box.
- **One accent colour** per section, everything else neutral. No constant gradient: the background is flat black or off-white, and light/3D shapes appear only as transitions or behind hero words.
- No icon on every noun and no 3D numerals. Decoration only shows up when it *is* the message (avatars inside "with your [faces] entire team").

## 3. Text-motion vocabulary (the move list)
1. **Word cascade.** Words arrive one at a time from the right (x +20–40 px), with blur 8→0 and opacity 0→1 over 0.35–0.5 s, ~100 ms stagger, expo.out. Words not yet spoken show as a 25% grey ghost first, then turn solid (Wabi "A new era *of software is here*").
2. **Smear / stretch-in.** The first letter arrives hugely stretched horizontally with directional blur and an RGB fringe, then snaps to shape while the rest of the word settles (Wabi "new era", "Discover", "Connect"). It takes 6–10 frames. This is their signature section opener.
3. **Letter scatter-assemble.** Letters start at random offsets (±80 px, some rotated), then fly into place with staggered back.out (Synaps logo, Bleap "beyond money").
4. **Depth zoom word.** A giant word (25–35% of frame height) scales from 1.15→1 with blur 20→0 while the background 3D shape drifts. The next phrase blurs in at normal size (Synaps "Get feedback", "Grow together").
5. **In-place swap.** "No more [modeling → texturing → lighting]": the swapped word slides up with a glow streak behind it. Use it for lists.
6. **Typing into a prompt box,** with a caret, ~18 chars/s, a key tick per character, then a send button press (scale 0.92→1) and the result card blooms.
7. **Inline objects in the sentence.** The sentence opens a gap, and avatars, an emoji or a toggle pop into the line (Wabi "Keep your mini-app private [lock]" → the toggle flips → "or share it with the world [globe]").
8. **Selection box + multiplayer cursor.** A word gets a blue bounding box with handles, and named cursor tags ("Sarah", "Robert") move around it. This shows "editing/collab" without a screen recording.
9. **Grey-out exit.** Old text fades to grey + blur while the new text arrives; it never just disappears.

## 4. Product UI is rebuilt, staged and cropped
- The UI is recreated as clean vector cards (HTML) with soft shadows, not shown as full-screen recordings. When real UI captures are used (Wix), they're cropped tightly and choreographed: cursor path → click glow → a panel pops.
- **Perspective + depth of field:** Synaps tilts the whole UI (rotateX 35–55°, rotateZ −20°), blurs the far side, and drifts the camera along a toolbar.
- **The cursor is a character:** a big glossy pointer, a click ring, and a hover glow on the target button.
- Wall-of-uses montage: a grid of tiles slides diagonally (Wabi and Flows open/close with a photo mosaic that dissolves to white tile by tile).
- For a real product, the rebuilt UI must match the real app exactly (same states, copy, colours). Never invent a feature. Mix it with short real captures for proof.

## 5. Pacing and easing
- Calm reading holds (1.5–3 s on a settled phrase) alternate with snaps of 4–8 frames. The holds are what make the snaps feel expensive.
- Easing is expo.out / power4.out almost everywhere: fast start, long soft settle. No linear moves and no bouncy back.out except for letters assembling and pop-ins.
- The end lands on the logo, letters assembling, then a single small line (URL / "Join thousands…") held for 2–3 s.

## 6. Sound design: measured
Measured with `sync_score.py`. Shown as visual events that have a sound onset within 80 ms, and audio onsets per second:

| Film | Sound-to-visual sync | Onsets/s | Tempo |
|------|----------------------|----------|-------|
| Synaps | 64% | 3.1 | ~80 bpm |
| Bleap | 62% | 3.0 | ~83 bpm |
| Wix | 53% | 2.8 | ~103 bpm |
| Wabi | 48% | 3.6 | ~103 bpm |
| **Ours (Kinetic-v3)** | **30%** | **2.3** | ~73 bpm |

- 4 of 6 have **no voice-over**: music + SFX carry the film, and the text is the narrator. When there's a VO (Flows, Wix), it's calm and confident, not hyped, and the text shows only 1–4 keywords, never the full sentence.
- The music is clean electronic/minimal with a clear pulse, and big moments (logo, "Introducing") land on a downbeat after a riser or a dropout.
- Sound layer: soft UI clicks for every pop-in, airy whooshes on every smear/zoom, key ticks while typing, a soft "bloop" for avatars/toggles, a sub hit + shimmer on the logo, and a reverse swell into each light wipe. Every motion beat gets a sound, mixed low (−18 to −24 dB under the music) so it's felt more than heard.

## Checklist before rendering
- [ ] Fewer than ~4 hard cuts per minute; every other change is a morph, match-move or light wipe
- [ ] Each screen has one idea and ≥60% empty canvas; sentence type ≤ 4% of frame height
- [ ] One typeface, one accent device, one accent colour per section
- [ ] Background is flat by default; light/3D shapes appear only for transitions and hero words
- [ ] Product moments are rebuilt UI or tight crops with a choreographed cursor, never a raw full-screen recording
- [ ] Every motion beat has a sound (target ≥ 55% on `sync_score.py`)

## 7. StateSync (30 s, light Bleap-style template; studied 2026-10-13)
Off-white canvas with a soft blue/violet glow drifting at the bottom. No voice-over, zero cuts, sound sync 46%, 3.2 onsets/s, ~94 bpm.
Structure: "Agents *evolved*" / "Harness *tooling* didn't" / "So we rebuilt it." → logo → three stat beats → app UI → logo + "*Start saving today.*" + small URL line.
New moves worth stealing:
- **The logo becomes the graphic system.** The mark splits into its parts: two bracket corners fly apart to become a chart frame, and its bar multiplies into ~80 thin bars that grow left to right. The chart reshapes (sorted → bell curve) while a highlighted bar acts as a playhead and the number counts (53% → 85%). Then the bars collapse to a line and dissolve. Every scene is drawn with the brand's own shapes.
- **Honest data viz instead of 3D numerals:** a thin-bar chart with a big plain number top-right and a small serif-italic caption. Small grey source footnote at the bottom.
- **Words tumble in** with a slight 3D rotation from below-right (the last word lands late). The line then shrinks as the camera pulls back, and words drop out one by one until only the keyword is left ("So we rebuilt it." → "rebuilt.").
- **Inline living glyph** between two words: a dot that morphs into a small spinning icon ("Agents • evolved").
- **Stat with letters scatter-assembling** ("Same plan. 86% more work."), with glossy 3D integration icons floating around in depth (blurred near and far ones = depth of field).
- **UI enters small and grows:** a dropdown card flips up in perspective, expands into the full app window and settles flat. The caption sits above it, mixing sans and serif italic ("*Switch* agents and keep going.").
For a product whose UI is itself a shape (e.g. a notch/pill), use that shape the way StateSync uses its logo: one pill that morphs through every scene.
