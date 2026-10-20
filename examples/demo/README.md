# Demo: "Lumen" (a fictional product)

An 18.5 s HyperFrames project showing the method's signature pieces on the light ground:
1. **d01-open:** the opening line with tumble-in and an accent bloom. Reduce-to-keyword, then the word breaks into pixels and implodes into ONE brand pixel.
2. **d02-name:** the pixel snaps home as the logo's last tile. The ink tiles burst out of it and assemble the mark, and the capsule draws closed. The camera pulls back into the lockup, the wordmark letters assemble, and the definition line tumbles in. Reduce-to-keyword, then everything collapses into the hand-over pill.
3. **d03-end:** the pill morphs into the app icon, then the wordmark, the facts line, the offer line, a button press, and the URL typed out.

The sound comes from the cue lists in `.kinetic/sfx/*.json`, rendered to `assets/sfx-mix.wav` by `scripts/sound_design.py`. There's no music here; add your own score.

```bash
cd examples/demo
python ../../scripts/build_light_index.py . --sfx assets/sfx-mix.wav --sfx-volume 1
python ../../scripts/sound_design.py . --lib ../../assets/sfx-library
npx hyperframes lint
npx hyperframes render --quality high --output renders/demo.mp4
```

Every hit time sits at the top of each frame's script (`HIT_…`). Replace them with your film's beat map. Swap the tile pattern (`TILES`), the brand colour (`ACCENT`) and the copy for your product.
