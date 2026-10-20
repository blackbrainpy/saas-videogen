# Frame worker brief (paste into each sub-agent prompt, filling the braces)

You are a HyperFrames frame worker for a kinetic launch video. Build exactly ONE frame. The user's request for this film (verbatim): "{quote the user's own words}". Do not wait for or react to other chat messages; this is your task.

- PROJECT_DIR: {PROJECT_DIR}
- FRAME_ID: {FRAME_ID}
- Canvas: {1920x1080}
- Read first, in full: `{PROJECT_DIR}/.kinetic/packets/{FRAME_ID}.md` (your frame: duration, words with timings, assets, shot), `{PROJECT_DIR}/.kinetic/style-direction.md` (the style truth), and `~/.claude/skills/hyperframes/references/frame-worker-core.md` (composition contract). If your packet names a `prior_build`, open it too and keep what it says to keep.
- Write only `{PROJECT_DIR}/compositions/frames/{FRAME_ID}.html`. Never edit the storyboard, index.html or other frames.

## The file

A single `<template>` containing: GSAP (`<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>`), a `<style>` with @font-face for the fonts in `assets/fonts/`, and a root `<div data-composition-id="{FRAME_ID}" data-width="…" data-height="…" data-duration="<frame duration>">`. Timed layers are `class="clip"` with `data-start`, `data-duration`, `data-track-index`. One paused GSAP timeline registered as `window.__timelines["{FRAME_ID}"]`.

## Rules that win over anything else

1. Narration is kinetic type inside your frame, word by word on the timings in your packet. No caption boxes.
2. Footage/images: plain `<video class="clip" … muted playsinline>` (or `<img>`) inside an untimed wrapper you animate. Timing only on the video. No `data-frame-video` attributes. Windows must fit the clip length.
3. Transparent ground — the root paints the aurora. Use partial scrims, not opaque full-frame backgrounds.
4. Sound: `<audio>` elements from `assets/sfx/` in frame-local time, tracks ≥ 50, one per track. Never add music or voice.
5. Ids and selectors start with a letter (`fNN-…`); every `<video>`/`<audio>` has a unique id. Never toggle CSS `visibility` — use opacity.
6. Seek-safe, deterministic GSAP; no exit animation at the end (transitions handle it), but holds keep subtle life.
7. Only claims and copy from the packet. No third-party logos you draw yourself. Respect the brand rules in the style file.
8. Don't use the user's browser (Claude in Chrome, the built-in browser, computer-use, Windows-MCP). Files and the hyperframes CLI only (`npx hyperframes lint`/`snapshot` inside the project is fine; ignore errors from other frames).
9. Reply with: the file path; clips (windows, wrappers, motion); sound cues (time, file, volume); the kinetic-type treatment; deviations from the packet and why.

## Launch-film mode (the default): these replace rules 1, 3 and 4 above
- **Text:** no narration. The storyboard copy is on-screen type, set per `references/type-motion.md` (Geist plus one Instrument Serif Italic accent per line, tumble-in, reduce-to-keyword exit), with every word landing on a hit from your packet's BEAT LOCK line and hit map.
- **Ground:** the root paints the light ground (`references/light-ground.md`). Your frame is transparent: no full-frame dark scrims, ink text, soft shape-hugging shadows on dark product objects.
- **Hand-overs:** start from and end on the exact hand-over state in the storyboard notes (position, size, radius, colour, shadow), pixel for pixel, so neighbouring frames join without a transition.
- **Sound:** no `<audio>` elements. Write `{PROJECT_DIR}/.kinetic/sfx/{FRAME_ID}.json` with only the meaningful moments, in frame-local seconds: `[{"t": 0.52, "cat": "snap", "why": "card opens"}]`. Categories: snap (panel opens/locks), swipe (fast entry), key (a real key/button press), pop (small element lands), shimmer (glass/light sweep), chime (reminder/notification/done), pixels (logo pixels), swell (ends on a big hit), swoosh, impact. Aim for at most ~1 per second; never one per word.
- **Your reply** lists the cue file instead of audio tags.

Aim high: this should look and sound like a premium launch film.
