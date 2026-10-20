# Type and text motion (the approved system)

The user's brief: "use the text style that is used in that video [StateSync] and the six Pinterest references … what text they use and what kind of motion effects on text they're using". The reference breakdowns are in `pro-motion-study.md`.

## Fonts (ship them in the project's `assets/fonts/` and @font-face them; copies are in this skill's `assets/fonts/`, OFL)
- **Sentence:** Geist Medium. **Hero single words:** Geist SemiBold. **Small lines:** Geist Regular. **Chapter tags:** Geist Mono.
- **Accent word:** Instrument Serif Italic.
  - Set it at 1.18× the sentence size, the same colour, letter-spacing −0.01em, optically aligned to the sans baseline.
  - **Exactly one accent per line:** the word marked `*like this*` in the storyboard copy.
- **Sizes on 1920×1080:**
  - Sentence 54 px (−0.025em), centred, max ~40 characters per line, two lines per screen at most.
  - Hero words 150–200 px (−0.045em).
  - Chapter tag 18–20 px, letter-spacing 0.12em.
- Never a box behind text. Colours are in `light-ground.md`.

## Motion vocabulary (use these; the old blur-in cascade is retired)
1. **Tumble-in (StateSync).** The default word entrance:
   - Each word goes from `y:+36, rotationX:-70, opacity 0, blur 10px` to `y:0, rotationX:0, opacity 1, blur 0`.
   - 0.62 s `expo.out`, stagger 0.055 s, transformPerspective 900, transformOrigin "50% 100%".
   - The last word lands slightly late with a touch more rotation.
2. **Ghost-to-solid (Wabi).** For a line timed across several beats: the whole line shows first as a ghost (opacity 0.22, blur 2px), then each word turns solid on its beat (0.25 s).
3. **Accent bloom.** The serif accent arrives with blur 14→0 and scale 1.12→1, 0.7 s `expo.out`, plus one soft highlight sweep (background-clip:text, 0.6 s) on its hit. Lint rejects letterSpacing tweens: move per-glyph spans instead.
4. **Smear opener (Wabi).** The first word of a chapter headline: scaleX 2.6→1, blur 18→0, with a faint red/cyan fringe that fades out, 0.35 s. The rest tumbles in.
5. **Reduce-to-keyword exit (StateSync).** Instead of a plain fade:
   - The line scales 1→0.92.
   - The non-accent words drop away (y +18, blur 8, opacity 0, stagger 0.04, 0.3 s).
   - The accent holds a beat, then blurs out.
6. **Letter assemble (Synaps / StateSync).** For hero words and wordmarks: letters fly from scattered offsets (±160 px, ±25°, seeded) to place, `back.out(1.4)`, stagger 0.03.
7. **Line swap.** The old line does the reduce-to-keyword exit while the new line tumbles in, overlapping by 0.1 s.

**Timing rules:**
- Every word landing sits ON a listed music hit (the BEAT LOCK line).
- Calm holds (1.5–3 s on a settled phrase) alternate with snaps of 4–8 frames.
- Ease with expo.out / power4.out. Use back.out only for letters and pop-ins.
