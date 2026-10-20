---
name: saas-videogen
description: Make a premium product launch film in HyperFrames, using the method behind a real launch film whose maker approved it as final. It is music-led, beat-locked and has no voice-over. It runs on a clean off-white ground with reference-grade type (Geist + one serif-italic accent per line), one product object morphs through every scene, a pixel-to-logo reveal, real product footage in rounded windows, and a sparse, meaningful sound design from a real SFX library. It makes 45–60 second films only, which say what the product is in the first ~7 seconds, plus 9:16 social cuts and stills from the film. A kinetic voice-over variant is also available. Works for any product (app, SaaS, website, hardware, game, service) with any assets (screen recordings, screenshots, a website URL, a logo, or nothing). Use it whenever the user wants a launch video, promo, trailer, explainer-style product film, "a video like this reference", a feature tour, Product Hunt / App Store / Microsoft Store / YouTube / social promo or vertical cuts, or a new film for a new product, even if they don't say "kinetic" or "HyperFrames".
---

# Launch film

This is the method behind a real 2:10 launch film (Oct 2026) that went through rounds of feedback until its maker approved it as final. Use it as the default for every new product. Films are always 45–60 s. The full recipe, and the feedback that shaped it, are in `references/launch-film-method.md`. A rendered, working demo (opening line, pixel logo switch, end card, sound cues) is in `examples/demo/`; a 60-second storyboard template is in `references/example-storyboard.md`.

## 0. Setup (any machine, any agent)
Run `python scripts/setup.py` before anything else. It checks Node, the HyperFrames CLI and its Chrome, the HyperFrames agent skills, FFmpeg/FFprobe, Python with numpy/Pillow, and the optional faster-whisper/yt-dlp. It installs whatever is missing through winget/brew/apt and pip. Use `--check` to only report. `references/tools.md` lists every tool, including the web tools (Gemini music, ElevenLabs), which run in the user's own browser accounts and are never installed or signed into for them.

## 1. Brief (ask only what changes the output, one question at a time)
Ask for:
- the product and its one message
- which assets exist (`references/assets.md`)
- the length within 45–60 s (the skill only makes 45–60 s films), and whether vertical cuts are wanted
- voice or on-screen text only (default: text only)
- brand colours and fonts (otherwise take them from the site or logo)

Never invent product facts, prices or numbers. Follow the user's own marketing rules (memory/CLAUDE.md), e.g. no emojis, no claims they can't back, real footage only.

## 2. Pipeline (launch-film mode)
Work in `<repo>/videos/<project>/`, created with `npx hyperframes init <dir> --non-interactive --example=blank`. Scripts are in this skill's `scripts/`.

1. **References.** Read `references/pro-motion-study.md`. If the user sends new reference films, study them with `study_refs.py` / `clip_sheet.py` / `sync_score.py`.
2. **Assets.**
   - Gather real recordings and screenshots: `cut_clips.py`, and `frame_clips.py` for punch-ins.
   - Copy `assets/fonts/*` into the project's `assets/fonts/`.
   - Pick the **hand-over object**: the product's own shape, such as a pill, a window card or the mark.
3. **Music.**
   - Generate 3 instrumental options in Gemini (prompt shape in `references/launch-film-method.md` § Music) and let the user pick.
   - Fit it to the film length with `track_fit.py` and `arrange_music.py`.
   - Map the beats: `beat_map.py <music> STORYBOARD.md .kinetic/beats.md`.
4. **Storyboard** (`STORYBOARD.md`, shaped like the example's):
   - Frontmatter, then the brief quoted.
   - Notes: the hand-over state in px, the chapter tag style, and the copy rules.
   - A score map.
   - One block per frame with `- src:`, `- start:`, `- duration:`, assets, a `BEAT LOCK:` line (events on A/B hits) and copy with one `*accent*` word per line.
   - Structure (45–60 s): hook that says what it is (~7 s) → logo switch into the name (~5 s) → 4–6 feature beats of 5–7 s → optional proof beat in a music silence → end card (~8 s). Template: `references/example-storyboard.md`.
5. **Style files.** Copy `references/light-ground.md` and `references/type-motion.md` into `<dir>/.kinetic/` and fill in the brand tints.
6. **Frames.**
   - `make_packets.py <dir>`. Each packet gets the frame's hit map from `.kinetic/beats.md` and points at the launch-film style files.
   - Run one sub-agent per frame, at most 5 at a time (or the user's cap), each with `references/frame-worker-brief.md` filled in, using its launch-film section.
   - Workers write `compositions/frames/<id>.html` plus `.kinetic/sfx/<id>.json` sound cues. They never use the user's browser.
   - Reuse code from the demo frames: d01/d02 for the **logo switch**, d03 for the end card.
7. **Assemble.**
   - `build_light_index.py <dir> --music assets/music/score.mp3 --sfx assets/sfx-mix.wav --glow-a "<r,g,b>"`.
   - Write `.kinetic/sfx/_film.json`: a swoosh into each stab phrase, a swell + impact on the end card.
   - `sound_design.py <dir> --dry-run`: check density (~1/s; it flags frames over 1.5/s). Then run it without `--dry-run` to render `assets/sfx-mix.wav`.
   - `fix_frames.py <dir>`, then `npx hyperframes lint` (0 errors).
8. **Review.** Run `npx hyperframes snapshot --at <every join and frame midpoint>` and look at the sheets yourself, against the checklist in `launch-film-method.md`.
9. **Render.** `npx hyperframes render --quality high --video-frame-format jpg --output renders/<name>.mp4` (put TEMP/TMP on a roomy drive). Then `export.py <dir> renders/<name>.mp4 <out> <Name>`, and look at the sheet it writes.
10. **Social.**
    - `social_cuts.py <film.mp4> cuts.json <out>/vertical --prefix <Product>-Vertical --tail <end-card CTA span>`: 9:16, SAR 1:1, bt709, −14 LUFS.
    - Make 3–4 vertical clips (12–20 s each) and pull 6–8 PNG stills at settled moments.
    - Write `ASSETS.md` listing every file with its length and hook.
11. **Deliver.** Give full paths, say what's new, and list the licence caveats: Gemini music and ElevenLabs free-plan sounds have no commercial licence, and note any third-party content visible in footage.

## Decisions to keep (each came from user feedback)
- **Ground:** light off-white with soft bottom glows. Black and frosted glass were rejected.
- **Type:** the reference type system, one accent per line. No caption boxes, no icon on every noun, no 3D numerals.
- **Continuity:** one object morphs through every scene, with pixel-exact hand-overs. Cutting on every line reads as a slideshow.
- **Logo switch:** last word → pixels → one brand pixel → logo. The user asked for it back by name.
- **Sound:** a real library, only meaningful moments, one mixed track. A sound on every word or every scene end reads as "forced, repetitive". Many `<audio>` tags also break the Windows render ("spawn ENAMETOOLONG").
- **Footage:** real product footage and states only. AI-generated footage or people are "AI slop" to the user.

## Hard-won traps
Read `references/traps.md`. The ones that cost the most:
- **FFmpeg / social cuts:**
  - Odd scaled heights crash FFmpeg 8.1 in yuv420p.
  - A stretched strip through vstack gives a broken SAR that X and Instagram reject. Use `setsar=1` + bt709 tags; social_cuts does this.
  - drawtext segfaults on Windows, so render text with Pillow.
- **HyperFrames lint:** it rejects letterSpacing tweens.
- **Opacity, not visibility:** use opacity, never CSS `visibility`, to show and hide.
- **Ids and fonts:** ids must not start with a digit, and fonts must be @font-face'd from `assets/fonts`.
- **Browser tools:**
  - Gemini answers in text when the prompt has brand names.
  - ElevenLabs downloads need the row's menu (the JS pointerdown helper is in traps.md).
  - Use the browser profile the user names.

## Kinetic voice-over mode (the older variant)
Use it only when the user wants narration. The voice-over becomes blur-in kinetic words with inline icons over a drifting aurora:
- `align_voice.py` for word timings (needs `setup.py --voice`)
- `synth_sfx.py` or the library for sounds
- `build_index.py --palette …` for the aurora root, then `transitions.mjs inject` from the product-launch-video skill
- `references/storyboard.md`, `style-direction.md`, `audio.md`

The pro-motion-study rules (restraint, morphs, a pro type system) still apply. For any new film, prefer the launch-film mode's ground and type.
