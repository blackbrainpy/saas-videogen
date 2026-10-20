# Audio — voice, music, sound effects, mix

## Voice (ElevenLabs in the user's browser)

1. Open the voice page the user gives (`elevenlabs.io/voices/<id>`) → it redirects to the voice library filtered to that voice → click **Use voice** (the waveform icon at the right end of the row; wait a few seconds, it navigates to Text to Speech with the voice selected).
2. Model: **Eleven v4** (most expressive, follows tags; returns two takes per generation). Multilingual v2 reads flatter. Lower **Stability** toward "Creative" (~0.35–0.4) for an excited read.
3. Script with one tag per line: `[curious] … [excited] … [upbeat] … [playful] … [confident] … [cheerful] …`. Tags are recognised when they turn purple. (Multilingual v2 instead understands `<break time="1.0s" />`; v4 does not need breaks — line endings pause naturally.)
4. Typing into the editor often "times out" in the browser tool but still lands — screenshot to confirm. Clear with click → Ctrl+A → Delete. If the Generate button sticks in a spinner, reload the page (the text persists).
5. Download each take from its row (download icon → MP3). Files land in the browser's download folder. Transcribe both takes (faster-whisper) and pick the one with every word right and the cleanest pauses.
6. Free plan = non-commercial with attribution; tell the user before they publish. Pop-ups offering upgrades: close them, never upgrade on their behalf.

No ElevenLabs? `npx hyperframes tts` (Kokoro, offline) or HeyGen if signed in. No voice at all? See SKILL.md § Variants.

**Split and time it:** `python scripts/align_voice.py --project <dir> --voice take.mp3 --lines lines.txt --lead 0.4 --tail 4.5 --gaps 2:0.6,5:0.6 --music <music.mp3> --music-volume 0.2`. One line per frame in lines.txt (no tags; numbers can be written as shown, e.g. "$9.99"). It transcribes with faster-whisper, aligns your exact lines to the transcript, cuts a clip per frame (from each line's first word to the next line's), adds the lead/gaps/tail, writes `audio_meta.json` and `.kinetic/words.md`.

## Music (Gemini in the user's browser, or their track)

1. gemini.google.com → **+** → **Create music**. Set **Length: Standard** (~60 s; "Short" is ~30 s) and **Vocals: Instrumental**.
2. Prompt: genre, BPM, instruments, structure with timings ("short intro, full groove by 5 s, a lift at ~30 s, clean confident ending"), "leaves room for a narrator; no lead melody fighting the voice".
3. Generate one track at a time — parallel generations in two tabs fail. "Something went wrong / technical issue" is common: send "please try again with the same brief" in the same chat.
4. Hover the player → download icon → **Audio only (MP3)**.
5. Pick the section: `python scripts/loudness_map.py track.mp3` prints loudness per second; choose a start so the drop or lift lands on a key frame (and any built-in silence lands on a deliberate pause). Trim with ffmpeg and a 0.3–0.5 s fade-in. If the track is longer than the film, join intro + ending with `acrossfade`.

## Sound effects

**Fast path (offline, always works):** `python scripts/synth_sfx.py <project>/assets/sfx` writes the 13-sound kit (whoosh-fast, swoosh-soft, swoosh-reverse, riser, pop, click, tick, counter-roll, glitch, typing, impact, shimmer, chime) as level-matched MP3s and prints their lengths.

**Richer path (ElevenLabs Sound Effects, 200 credits per prompt, 4 variations):** elevenlabs.io/app/sound-effects. For each sound: click the prompt box → Ctrl+A → Delete → type the prompt → click the round arrow ("Generate sound effect") → wait ~10 s → row's download icon → MP3. Prompts that worked:
- whoosh-fast: "Fast clean airy whoosh transition for a modern tech product video, short swish passing by, no music"
- riser: "Short rising digital riser building tension into a reveal, clean modern tech, ends on a soft swell"
- counter-roll: "Rapid digital number counter ticking fast then slowing down and stopping, clean UI ticks, like a scoreboard rolling"
- pop: "Soft bubbly modern UI pop for a card or chip appearing on screen, very short, clean"
- impact: "Deep cinematic sub bass impact boom with a short shimmering tail, for a logo or big number reveal"
- shimmer: "Bright magical shimmer sparkle chime rising, for a logo reveal in a tech commercial"
- glitch: "Short digital glitch stutter blip, techy data scramble, clean, for text decoding on screen"
- typing: "Soft fast typing on a modern laptop keyboard, a short burst of clean key clicks"
- chime: "Pleasant positive success notification chime, modern app UI, two bright notes"
- swoosh-soft: "Soft deep cinematic swoosh with slow air movement, smooth transition between scenes"
Then trim silence and level them: `python scripts/synth_sfx.py --normalize <folder-with-downloads> <project>/assets/sfx` (renames by the names above if the files are named that way; tick/click/swoosh-reverse are still synthesized). Mixing the two paths is fine.

## Mix and loudness
- Voice at 1.0 on the root; music 0.18–0.22 on the root; SFX volumes per the style table (pops/ticks quiet, impacts loud but short).
- After rendering, `scripts/export.py` normalises to −15 LUFS integrated, true peak −1.5 dB (web/YouTube).
- Verify the SFX made it: compare loudness at a known hit (e.g. the impact) against a version without effects, or listen to a few frames' windows.
