# Tools this skill uses

On a new machine or a new agent, run `python scripts/setup.py` first. It checks every installable tool below and installs what is missing: winget on Windows, Homebrew on macOS, apt/dnf on Linux, `pip --user` for Python packages. Use `--check` to only report, `--voice` for voice-over mode, and `--refs` to download reference videos. After a fresh Node or FFmpeg install on Windows, open a new terminal so PATH picks it up.

## Installed by setup.py
| Tool | Used for | Install |
|---|---|---|
| Node.js ≥ 20 + npx | the HyperFrames CLI | winget `OpenJS.NodeJS.LTS` / `brew install node` / apt `nodejs npm` |
| HyperFrames CLI (`npx --yes hyperframes`, tested 0.8.181) | `init`, `lint`, `check`, `snapshot`, `render`, `beats`, `capture`, `doctor` | runs through npx; each project pins its version in package.json |
| Chrome headless shell | HyperFrames rendering and snapshots | `npx hyperframes browser ensure` (cached in `~/.cache/hyperframes`) |
| HyperFrames agent skills (`hyperframes`, `hyperframes-core`, `-animation`, `-cli`, …) | the composition rules frame workers follow | `npx hyperframes skills`; `npx hyperframes skills update product-launch-video` for kinetic mode's `transitions.mjs` |
| FFmpeg + FFprobe 8.x | cutting clips, the sound mix, loudness, social cuts, frame sheets | winget `Gyan.FFmpeg` / `brew install ffmpeg` / apt `ffmpeg` |
| Python 3.10+ with numpy and Pillow | every script in `scripts/` | `pip install --user numpy Pillow` |
| faster-whisper (optional, `--voice`) | `align_voice.py` word timings for a voice-over | `pip install --user faster-whisper` |
| yt-dlp (optional, `--refs`) | downloading reference videos the user links. Ask before each download. | `pip install --user yt-dlp` |

GSAP 3.14.2 loads from cdn.jsdelivr.net inside each composition; nothing to install. The fonts (Geist, Instrument Serif; OFL) and the sound-effect library ship in `assets/`.

## Web tools (the user's own accounts, in their browser; never installed, never signed in for them)
| Tool | Used for | Notes |
|---|---|---|
| Gemini, "Create music" (gemini.google.com) | the film's score: 3 instrumental options, the user picks | No brand names in the prompt (they make it answer in text). One generation at a time. Downloads land in the browser's download folder. No commercial licence on the free plan; say so. |
| ElevenLabs Sound Effects | new library takes (see `assets/sfx-library/PROMPTS.md`) | Free plan: fixed 2.0 s = 80 credits, prompt influence 65 %. Download WAVs through each history row's download menu. The Explore library needs a paid plan, so don't use it and never click an upgrade. No commercial licence on the free plan. |
| ElevenLabs voices (kinetic VO mode only) | voice-over | Eleven v4 with [excited]/[upbeat] tags. |
| Pinterest / YouTube / the user's files | reference films to study | `scripts/study_refs.py`, `sync_score.py`, `clip_sheet.py`. |

If a browser tool is needed, use the browser the user names. If the right account isn't signed in, ask them to switch profile; don't sign in for them.

## Only when new footage must be recorded
| Tool | Notes |
|---|---|
| OBS Studio | Drive it by hotkeys only and use a separate profile, never the user's own. Record 60 fps at CQP 14–18. Capture the real product; never use AI-generated footage. |
| The product itself | Real states and captures only. Cover third-party logos; blur names, PC names, IPs and other personal data. |

## Not needed
`npx hyperframes doctor` also lists Docker, whisper-cpp, Kokoro TTS and MusicGen. This skill doesn't use them, so ignore those ✗ lines.
