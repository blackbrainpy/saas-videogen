"""Split one voice-over take into a clip per frame, with word timings.

    python align_voice.py --project videos/acme --voice take.mp3 --lines lines.txt
        [--lead 0.4] [--tail 4.5] [--gaps 2:0.6,5:0.6]
        [--music music.mp3 --music-volume 0.2] [--model small.en]

lines.txt: one line per frame, exactly as spoken (no delivery tags). Numbers may
be written as they will be shown ("$9.99"); alignment tolerates the mismatch.

Each frame's clip runs from its first word (frame 1: from 0) to the next
frame's first word, so the natural pauses stay inside the frames. --lead adds
silence before the first word, --gaps adds silence after frame N's line, --tail
holds the last frame (the end card).

Writes:
  <project>/assets/voice/NN.wav
  <project>/assets/bgm/<music>          (if --music)
  <project>/audio_meta.json             {bgm, voices:[{frame, path, duration_s, words}], sfx:[]}
  <project>/.kinetic/words.md           per-frame duration + "Words:" lines for the storyboard
Needs: ffmpeg, faster-whisper (pip install faster-whisper).
"""

import argparse
import difflib
import json
import os
import re
import subprocess

RATE = 44100


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def duration(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def transcribe(path: str, model_name: str):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(path, word_timestamps=True, language="en", beam_size=5)
    return [(w.word.strip(), w.start, w.end) for s in segments for w in s.words if w.word.strip()]


def align(lines, heard):
    script = [(i, w) for i, line in enumerate(lines) for w in line.split()]
    a = [norm(w) for _, w in script]
    b = [norm(w) for w, _, _ in heard]
    match = {}
    for block in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(block.size):
            match[block.a + k] = block.b + k
    times = [(heard[match[i]][1], heard[match[i]][2]) if i in match else None for i in range(len(script))]
    for i, t in enumerate(times):
        if t is not None:
            continue
        prev = next((times[j] for j in range(i - 1, -1, -1) if times[j]), None)
        nxt = next((times[j] for j in range(i + 1, len(times)) if times[j]), None)
        s = prev[1] if prev else (nxt[0] - 0.3 if nxt else 0.0)
        e = nxt[0] if nxt else s + 0.3
        times[i] = (s, max(s + 0.05, e))
    return [(li, w, t[0], t[1]) for (li, w), t in zip(script, times)]


def cut(src, start, end, before, after, dst):
    filt = []
    if before > 0:
        filt.append(f"adelay={int(before * 1000)}:all=1")
    if after > 0:
        filt.append(f"apad=pad_dur={after:.3f}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}"]
    if end is not None:
        cmd += ["-to", f"{end:.3f}"]
    cmd += ["-i", src, "-ac", "2", "-ar", str(RATE)]
    if filt:
        cmd += ["-af", ",".join(filt)]
    cmd.append(dst)
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--lines", required=True)
    ap.add_argument("--lead", type=float, default=0.4)
    ap.add_argument("--tail", type=float, default=4.5)
    ap.add_argument("--gaps", default="")
    ap.add_argument("--music")
    ap.add_argument("--music-volume", type=float, default=0.2)
    ap.add_argument("--model", default="small.en")
    a = ap.parse_args()

    lines = [l.strip() for l in open(a.lines, encoding="utf-8") if l.strip()]
    gaps = {int(k): float(v) for k, v in (p.split(":") for p in a.gaps.split(",") if p)}
    heard = transcribe(a.voice, a.model)
    words = align(lines, heard)
    starts = [min(w[2] for w in words if w[0] == i) for i in range(len(lines))]

    os.makedirs(os.path.join(a.project, "assets", "voice"), exist_ok=True)
    os.makedirs(os.path.join(a.project, ".kinetic"), exist_ok=True)
    voices, md = [], ["# Frame durations and word timings (frame-local seconds)\n"]
    for i, line in enumerate(lines):
        frame = i + 1
        seg_start = 0.0 if i == 0 else max(0.0, starts[i] - 0.12)
        seg_end = (starts[i + 1] - 0.12) if i + 1 < len(starts) else None
        before = a.lead if i == 0 else 0.0
        after = gaps.get(frame, 0.0) + (a.tail if seg_end is None else 0.0)
        rel = f"assets/voice/{frame:02d}.wav"
        cut(a.voice, seg_start, seg_end, before, after, os.path.join(a.project, rel))
        dur = round(duration(os.path.join(a.project, rel)), 3)
        off = before - seg_start
        fw = [dict(id=f"w{frame:02d}_{k:02d}", text=w, start=round(s + off, 3), end=round(e + off, 3))
              for k, (_, w, s, e) in enumerate(x for x in words if x[0] == i)]
        voices.append(dict(frame=frame, path=rel, duration_s=dur, words=fw))
        md.append(f"## Frame {frame} — {dur}s\n\n\"{line}\"\n\nWords: " +
                  " · ".join(f"{w['text']} {w['start']:.1f}" for w in fw) + "\n")
        print(f"frame {frame}: {dur:5.2f}s  {line[:70]}")

    bgm = None
    if a.music:
        os.makedirs(os.path.join(a.project, "assets", "bgm"), exist_ok=True)
        rel = "assets/bgm/" + os.path.basename(a.music)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.music, "-c", "copy",
                        os.path.join(a.project, rel)], check=True)
        bgm = dict(path=rel, volume=a.music_volume, duration_s=round(duration(a.music), 3))
    json.dump(dict(bgm=bgm, voices=voices, sfx=[]), open(os.path.join(a.project, "audio_meta.json"), "w"), indent=2)
    open(os.path.join(a.project, ".kinetic", "words.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"film length {sum(v['duration_s'] for v in voices):.1f}s -> audio_meta.json, .kinetic/words.md")


if __name__ == "__main__":
    main()
