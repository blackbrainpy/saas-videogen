# Assets — work with whatever exists

Inventory first, then pick the path. Always prefer the real product over anything drawn; never invent UI the product doesn't have, and never use AI-generated pictures of the product.

## Screen recordings (best)
- Find the moments: build a frame sheet (one still every 0.5–1 s) of each recording and look at it; note the second each key action happens.
- Cut short clips (4–10 s) around each moment: write a JSON spec and run `python scripts/cut_clips.py spec.json`:
  `{"out": "videos/_footage/clips", "clips": {"hover-open": {"src": "rec/hover.mp4", "start": 13.6, "end": 19.6, "desc": "card opens at 0.9 s"}}}` → 1080p30, no audio, keyframe every 15 frames (seek-friendly), plus `clips.md`.
- Small UI on a big screen (a menu bar, a notch, a toolbar): bake a slow punch-in with `python scripts/frame_clips.py spec.json` (regions as x, y, width on the source) → `<name>-framed.mp4`. Workers can also scale the wrapper, but baked punch-ins stay sharper.
- Privacy: check frames for personal data (names, emails, installed apps, chats) and third-party content (videos, logos) before using a clip; tell the user what's visible.

## Screenshots / product photos
- Same floating-window and card-wall treatments with `<img>`; add a slow drift, a light sweep and a parallax layer so stills feel alive.
- Product photos with a plain background: cut out (`npx hyperframes remove-background` or media-use) to float the object in 3D.

## A website URL only
- `npx hyperframes capture <url> -o capture --json` → screenshots, brand colours, fonts, copy, logos. Use the full-page screenshot as a scrolling "device" plate, and its copy as the source of truth for claims.

## Logo / brand
- Logo PNG/SVG for the intro and end card (flip in with depth; if the PNG has a baked shadow, put the shadow on a separate plate when extruding).
- Brand fonts: copy the .woff2 files into `assets/fonts/` (variable fonts preferred) — every frame declares them with @font-face. No brand font → Geist or Inter.
- Brand colours → the aurora palette and emphasis colour.

## Nothing at all
- The style still works: kinetic type + drawn glossy icons + big numbers + simple HTML "UI cards" showing the product's real states with real copy (from the user's description). Keep drawn UI honest and simple.

## Where things go
`<project>/assets/` (clips, images, logo), `assets/fonts/`, `assets/sfx/`, `assets/voice/` (written by align_voice.py), `assets/bgm/`.
