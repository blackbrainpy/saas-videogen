# Traps (each one cost real time once)

**Composition**
- A child with inline `visibility: visible` escapes the frame's clip gating and shows across the whole film. Use opacity for show/hide.
- Ids starting with a digit break `#id` selectors (`querySelector` throws). Prefix `fNN-`.
- Every `<video>` needs an `id`, or lint fails ("will be FROZEN in renders"). `fix_frames.py` adds missing ones.
- Fonts must be declared with `@font-face` inside every frame (and the files must exist in `assets/fonts/`), or text falls back silently. `fix_frames.py` adds Geist declarations when a frame uses Geist without one; adapt FONT_FACE for other brands.
- Timing on both a `<video>` and its wrapper = wrong frames then the clip vanishes. Timing on the video only.
- A video window longer than the clip freezes on its last frame. Use `data-media-start` to skip dead time and keep `start + duration ≤ length`.
- 3D extruded numbers (stacked text layers) fail `hyperframes check` as "content_overlap". Mark each layer `data-layout-allow-overlap` (`fix_frames.py` does it for elements with class names ending in `-dl`, the convention workers use; tell workers to set the attribute themselves on generated layers).
- Opaque full-frame backgrounds in a frame hide the root aurora and any footage underneath. Frames stay transparent.

**Assembly**
- Don't use product-launch-video's `assemble-index.mjs` for this style: it hoists videos to the root with fixed geometry (no tilt/blur/scale) and errors on inline media. Use `build_index.py`.
- `transitions.mjs inject` also edits frame files (it extends roots and tail clips for the overlap). Run it AFTER the final frames are written, and re-run it whenever frames are replaced. It is idempotent.
- Keep pristine copies of approved frames (`.kinetic/frames-vN/`) before any tool rewrites them; a restyle or retime gives workers the old file as `prior_build`.

**Rendering**
- Rendering needs several GB of temp space; on a full C: drive set `TEMP`/`TMP` to another drive before `npx hyperframes render`, and pass `--video-frame-format jpg`.
- `npx hyperframes snapshot --at t1,t2,…` writes contact sheets to `snapshots/`; delete the folder first so old sheets don't mislead you.

**Browser services (ElevenLabs, Gemini)**
- Screenshots of a background tab can time out; reading via `find`/`get_page_text` still works. Re-take the screenshot once before assuming the page is broken.
- Typing reports a timeout but usually lands. Always verify the text box before generating — a stale prompt plus new text concatenates and wastes credits.
- ElevenLabs download icons open a small menu (MP3 / WAV / Save to assets); click MP3 via its menu item. Downloads go to the browser's default folder (check it; on some machines it is a different drive).
- Gemini: one music generation at a time; retry in the same chat on "technical issue".
- Never click upgrade/pay buttons; close the pop-up. Close the tabs you opened when done.

**Content**
- Real footage can contain third-party videos, logos, notifications or personal data — list what's visible when delivering.
- Free-tier voice/SFX/music may not allow commercial use — say so with the delivery.

**Launch-film mode (added Oct 2026, from the approved 2:10 film)**
- Hundreds of `<audio>` tags make the render's audio mix fail on Windows with "spawn ENAMETOOLONG". Use one sfx track from `sound_design.py`; `bake_sfx.py` only rescues old tag-based projects.
- HyperFrames lint rejects `letterSpacing` tweens. For the accent bloom, animate per-glyph spans (x/scale/blur) instead.
- FFmpeg 8.1 (Windows build): an odd scaled height in yuv420p crashes with no message (exit 0xC0000374 or 127). Keep every height even.
- FFmpeg `drawtext` segfaults (fontconfig). Render text with Pillow to a PNG and overlay it.
- Stretching a 2–16 px strip with `scale` sets a compensating SAR, and `vstack` passes it on. Browsers then read a 1080x1920 clip as 40555x1920, and X and Instagram refuse it. Add `setsar=1` after every scale, tag bt709 with `setparams`, and check with ffprobe before handing clips over.
- Stills for image posts: pick settled moments. A frame taken mid tumble-in or mid ghost-to-solid looks broken as a still.
- The proof beat sits in the music's silence. Its typed sound is `key` cues every ~0.1 s and nothing else.
- ElevenLabs download menus: coordinate clicks toggle the menu shut or download twice. Run this in the page instead (4 newest rows; WAV):
  ```js
  const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const out=[]; const btns=[...document.querySelectorAll('button[data-testid="sfx-download-history-group"]')].slice(0,4); for(const b of btns){ b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,button:0,pointerType:'mouse'})); await sleep(450); const item=[...document.querySelectorAll('[role="menuitem"]')].find(m=>/WAV/.test(m.innerText)); if(item){ item.click(); out.push('ok'); } else { out.push('nomenu'); } await sleep(2600); document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true})); await sleep(300);} ({n:btns.length,out})
  ```
  Chrome asks once to allow multiple downloads. The user clicks Allow; you don't.
- ElevenLabs history search: add `?q=<words>` to the Sound Effects URL. The Explore library needs a paid plan, so don't use it.
- Gemini music: brand or product names in the prompt make it reply in text instead of generating. Describe the mood, tempo and instruments only.
- Use the browser profile the user is signed in with. If a site shows a sign-in page, ask the user to switch profile; never sign in for them.
