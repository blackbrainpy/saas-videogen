# Sound-effect library

There are 42 takes in this folder, `<category>_<n>.wav`. The script skips `tap_1`, a muddy 7 s take, so 41 are usable. They were generated with ElevenLabs Sound Effects (free plan) in Oct 2026 for a real launch film.

**Licence:** the free plan gives no commercial licence. Tell the user before a film is published.

## Settings in ElevenLabs
- Duration: fixed 2.0 s (80 credits; Auto costs 200).
- Prompt influence: 65%.
- 4 variations per prompt.

## Processing
Download the WAVs to one folder, then run:
`python -P scripts/build_sfx_library.py <download_dir> <out_dir> "<file-prefix>=<category>" ...`

It drops duplicates, trims silence and peak-normalises to −3 dBFS. `sound_design.py` then aligns each take on its transient and loudness-matches it per category.

## Prompts

| Category | Prompt | Peak |
|---|---|---|
| tap | Premium soft UI tap: one clean glassy click, very short and crisp but gentle, high fidelity, luxury app interface, tiny natural room | ~0.05 s; takes 2 and 4 peak late, ~1.1 s |
| swipe | Soft airy swipe whoosh, short and smooth, filtered air moving past, modern premium tech product video transition, clean and subtle | 0.18–0.34 s |
| swoosh | Cinematic transition swoosh with a deep warm sub body and silky air on top, smooth and slow, premium product reveal, clean ending, no harsh noise | 1.4–2.4 s; the script lands this peak on the cue |
| impact | Clean deep cinematic impact for a premium tech logo reveal: a warm sub boom with a soft glassy shimmer tail, polished and modern, not aggressive, no distortion | 0.1–0.5 s |
| shimmer | Delicate liquid glass shimmer: crystalline glints and soft sparkles rising, light catching on glass, elegant and airy, high fidelity, gentle | 0.25–0.6 s |
| pixels | Tiny digital pixel blips assembling into a logo: soft granular data clicks snapping together quickly, playful but premium, clean, very short | |
| key | Premium mechanical keyboard key press: a single deep satisfying thocky keystroke, clean close microphone, no room noise, quick release | several strokes; the script plays the first 0.16 s |
| chime | Soft friendly notification chime: two gentle glassy notes, warm and minimal, like a premium operating system alert, short and calm, no long echo | |
| pop | Soft rounded pop for a UI element appearing: subtle bubble-like pop, clean and quiet, premium app sound, very short, no echo | |
| snap | Smooth glass panel expanding and locking into place: an airy soft slide that ends with a gentle precise click, premium interface motion sound, clean | |
| swell | Short reverse swell rising into a cut: soft breathy reverse cymbal with airy shimmer, smooth tension build that ends abruptly at the peak, clean, cinematic | 0.9–1.3 s; the end is the hit |

## Brand-specific sounds
To add a sound for one product, generate it with the same settings, name the files `<newcat>_<n>.wav`, and add the category to the tables at the top of `sound_design.py` (TARGET_DB, PLAY, RANK, MIN_GAP).
