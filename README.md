# saas-videogen

An agent skill that makes premium SaaS and product launch films with [HyperFrames](https://hyperframes.heygen.com) (HTML + GSAP, rendered to MP4). Drop it into Claude Code or any agent that reads `SKILL.md` skills, ask for "a launch video for my product", and the agent:
- installs the tools it needs
- plans the film on the music's beats
- builds every scene as code
- designs the sound
- renders the film
- cuts the vertical social clips

![Demo: the opening line breaks into pixels, the logo builds from one pixel, the end card](docs/demo.gif)

*The included demo (`examples/demo`, 18.5 s, [MP4](docs/demo.mp4)): fictional product, real code.*

## The style
The method came out of many feedback rounds on a real launch film, measured against professional SaaS motion references:
- **Light ground:** off-white with soft drifting colour glows.
- **Reference-grade type:** Geist, with one Instrument Serif Italic accent word per line. Words tumble in, ghost to solid, and reduce to a keyword.
- **One object morphs through every scene,** with pixel-exact hand-overs instead of cuts.
- **Logo switch:** the opening line's last word breaks into pixels, which implode into one brand pixel, and the logo builds out of it.
- **Beat-locked:** every event lands on a graded music hit (A/B/C).
- **Sparse, meaningful sound:** a real 42-take SFX library, mixed from short cue lists into one track (about one sound per second, never one per word).
- **Real product footage only,** in rounded windows with soft shadows.

## Outputs
| Cut | Length |
|---|---|
| Hero launch film | 45–65 s |
| Extended "every feature" film (says what the product is in the first 20 s) | ~2 min |
| Vertical 9:16 social clips with hook lines (SAR 1:1, bt709, -14 LUFS) | 15–22 s |
| Stills for image posts | |

## Install
```bash
git clone https://github.com/blackbrainpy/saas-videogen ~/.claude/skills/saas-videogen
python ~/.claude/skills/saas-videogen/scripts/setup.py
```

`setup.py` checks and installs Node.js, the HyperFrames CLI and its Chrome, the HyperFrames agent skills, FFmpeg, and Python with numpy and Pillow. It uses winget, Homebrew or apt/dnf, plus pip. Run `--check` to only report, and `--voice` / `--refs` for the optional extras. See [references/tools.md](references/tools.md).

## Use
Ask your agent, for example:
- "Make a 2 minute launch video for my app <name> that shows every feature and makes it clear in the first 20 seconds what it is. Recordings are in ./videos."
- "60 second Product Hunt promo from these screenshots and our website, plus vertical cuts."

The skill asks only what changes the output: the product, assets, cuts, voice or text, brand colours.

## Inside
| Path | What |
|---|---|
| `SKILL.md` | The method and pipeline the agent follows |
| `references/launch-film-method.md` | The full recipe: structure, continuity, logo switch, music, sound, render, review checklist |
| `references/light-ground.md`, `type-motion.md` | The look: ground, colours, fonts, the text-motion vocabulary |
| `references/pro-motion-study.md` | What six professional SaaS films do differently, measured |
| `references/example-storyboard.md` | A 2-minute storyboard template |
| `references/traps.md` | Failures that cost hours, and their fixes |
| `scripts/` | `setup.py`, `beat_map.py`, `arrange_music.py`, `track_fit.py`, `make_packets.py`, `build_light_index.py`, `sound_design.py`, `social_cuts.py`, `export.py`, reference-study tools and more |
| `assets/sfx-library/` | 42 sound-effect takes in 11 categories, plus the prompts to regenerate or extend them |
| `assets/fonts/` | Geist and Instrument Serif (SIL OFL) |
| `examples/demo/` | A working HyperFrames project: opening line, logo switch, end card, sound cues |

## Credits and licences
- **Code:** MIT (see [LICENSE](LICENSE)).
- **Fonts:** Geist (Vercel) and Instrument Serif, under the SIL Open Font License (`assets/fonts/OFL*.txt`).
- **Sound effects:** generated with ElevenLabs Sound Effects. Check ElevenLabs' terms for your plan before commercial use; see [NOTICE.md](NOTICE.md).
- **Rendering:** [HyperFrames](https://github.com/heygen-com/hyperframes) by HeyGen. Animation: [GSAP](https://gsap.com).
- **Music:** none included. The skill guides you to generate a score and pick one, and you are responsible for its licence.
