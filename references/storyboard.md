# Script and storyboard

## Writing the lines (one line = one frame)

6–10 lines, 45–60 s at an upbeat read (~150 wpm). Write for the ear: short phrases with natural cue points, because each phrase becomes the kinetic type on screen. Every claim must be true and sourced (site, app, user).

A beat menu (pick what the product supports; reorder freely):

| Beat | What it does | Example shape |
|---|---|---|
| Hook | a question or claim about the viewer, not the product | "How much of your day goes to switching windows?" |
| Name + answer | the product name by line 2, with the one message | "Lumen. One timer, zero distractions." |
| Why / how | one mechanism, plain words | "It only draws when something changes…" |
| Proof in use | the product working where it matters | "So it rides right along in your game…" |
| Wow feature | the most visual feature | "And your browser comes too!" |
| Breadth | 5–6 features, one word each, rhythmic | "Music. A file shelf. Clipboard history…" |
| And more | a fast list | "Plus widgets, weather, timers, reminders…" |
| Trust | remove objections | "No account. No ads. No subscription." |
| CTA | offer + where | "Try it free for fourteen days. Get it at lumen.example!" |

Line rules: name numbers as they will be shown ("thirteen megabytes" spoken → "13 MB" on screen); one idea per line; end on the CTA with the place to get it. For ElevenLabs v4 add one delivery tag per line ([curious], [excited], [upbeat], [playful], [confident], [cheerful]) — tags are not spoken and must not appear in `lines.txt`.

## STORYBOARD.md shape

```markdown
---
format: 1920x1080
duration: 55s
message: "<the one thing the video must say>"
music: <track name and where it lifts>
captions: kinetic (no caption track)
---

## Frame 1 — <short title>

- scene: <one line>
- voiceover: "<the exact line>"
- duration: 3.4s
- transition_in: cut
- src: compositions/frames/01-<slug>.html
- asset_candidates: assets/<clip>.mp4 — <what it shows, its length, when the key moment happens>; assets/logo.png — <…>
- prior_build: <optional path to an older version of this frame to keep>

Words: How 0.4 · much 0.7 · of 0.9 · your 1.0 · PC 1.2 · …
<Concrete shot: where the type sits, which words are emphasised, which icons pop on which words, what the footage does and when, the hero effect of this frame, and the sound cues (time, sound).>
```

- `duration` and the `Words:` line come from `.kinetic/words.md` (written by align_voice.py). Durations already include the pauses ElevenLabs left between lines.
- `transition_in`: `cut` (default between fast beats), `blur-crossfade` (calm change), `zoom-through` (section change, punchy), `crossfade 0.3s`. Use cuts generously; the frames carry their own motion.
- Give every frame one **hero effect** (extruded number, camera through a word, card wall, floating window fly-in, slide pill…) and vary them; don't repeat the same trick in adjacent frames.
- Describe footage by what happens at which second of the clip, so workers can line the action up with the words (use `data-media-start` to skip dead time).
- Put the shared style in `.kinetic/style-direction.md`, not in every frame block.

## Packet contents (make_packets.py)

Each `.kinetic/packets/NN-*.md` = the frame block + the asset list with real clip lengths (ffprobe) + pointers to the style file and fonts. Workers read only their packet, the style file and the HyperFrames worker contract.
