"""Render a film's sound effects as ONE mixed track from cue lists and a take library.

    python -P sound_design.py <project> [--lib <dir>] [--out assets/sfx-mix.wav] [--dry-run]

Cues (only the moments that MEAN something on screen; see references/launch-film-method.md § Sound):
  <project>/.kinetic/sfx/<frame-id>.json   frame-local time, written by each frame worker
  <project>/.kinetic/sfx/_film.json        film time (swooshes into big phrases, the end impact)
  each file: [{"t": 0.52, "cat": "snap", "why": "card opens"}, ...]
Frame starts come from index.html (data-composition-src=".../<frame-id>.html" data-start="...").

Categories (library files are <cat>_<n>.wav): impact, swoosh, swell, snap, swipe, pop, key, shimmer,
chime, pixels, tap. The script thins the list (per-category spacing, max two sounds per 0.3 s, the bigger
sound wins), round-robins the takes with small pitch/level jitter, aligns each take on its own transient
(swell/swoosh on their peak, so the peak lands on the cue), loudness-matches each category and writes one
48 kHz stereo WAV. Put it in index.html as one <audio> (volume ~0.85) under the music (~0.7).
"""
import argparse
import glob
import json
import os
import re
import subprocess

import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIB = os.path.join(os.path.dirname(HERE), "assets", "sfx-library")

TARGET_DB = {"impact": -17.0, "swoosh": -22.0, "swell": -23.0, "snap": -24.0, "swipe": -26.0, "pop": -25.0,
             "key": -24.0, "shimmer": -27.0, "chime": -24.0, "pixels": -25.0, "tap": -26.0}
PLAY = {"impact": 1.8, "swoosh": 3.0, "swell": 1.3, "swipe": 0.55, "snap": 0.6, "pop": 0.35,
        "shimmer": 1.3, "chime": 1.4, "pixels": 1.1, "key": 0.16, "tap": 0.3}
RANK = {"impact": 9, "swoosh": 8, "swell": 7, "chime": 6, "snap": 5, "pixels": 5, "key": 4, "swipe": 3,
        "pop": 3, "tap": 3, "shimmer": 2}
MIN_GAP = {"pop": 0.9, "swipe": 1.3, "shimmer": 2.5, "pixels": 1.5, "key": 0.09, "chime": 2.0, "tap": 0.6,
           "snap": 1.5, "swell": 4.0, "impact": 2.0, "swoosh": 8.0}
PITCH = {"pop": 1.5, "key": 1.0, "swipe": 1.0, "snap": 1.0, "shimmer": 0.7, "tap": 1.0}  # +/- semitones
SKIP = {"tap_1"}  # a muddy 7 s take in the shipped library


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def hit_point(y, cat):
    n = len(y) // 240 * 240
    db = 20 * np.log10(np.sqrt((y[:n].mean(1) ** 2).reshape(-1, 240).mean(1) + 1e-12))
    if cat in ("swell", "swoosh"):
        return int(np.argmax(db)) * 240 / SR
    return int(np.argmax(db > db.max() - 10)) * 240 / SR


def library(lib_dir):
    lib = {}
    for f in sorted(glob.glob(os.path.join(lib_dir, "*.wav"))):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in SKIP:
            continue
        cat = name.rsplit("_", 1)[0]
        y = load(f)
        lib.setdefault(cat, []).append((name, y, hit_point(y, cat)))
    return lib


def frame_starts(project):
    idx = open(os.path.join(project, "index.html"), encoding="utf-8").read()
    starts = {}
    for tag in re.findall(r"<div\b[^>]*data-composition-src=[^>]*>", idx):
        src = re.search(r'data-composition-src="([^"]+)"', tag).group(1)
        st = re.search(r'data-start="([\d.]+)"', tag)
        if st:
            starts[os.path.splitext(os.path.basename(src))[0]] = float(st.group(1))
    dur = float(re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', idx).group(1))
    return starts, dur


def cues(project, starts):
    ev = []
    for f in sorted(glob.glob(os.path.join(project, ".kinetic", "sfx", "*.json"))):
        key = os.path.splitext(os.path.basename(f))[0]
        if key != "_film" and key not in starts:
            print(f"warning: {key}.json has no frame in index.html; skipped")
            continue
        t0 = 0.0 if key == "_film" else starts[key]
        for c in json.load(open(f, encoding="utf-8")):
            if c["cat"] not in RANK:
                raise SystemExit(f"{f}: unknown category {c['cat']!r}; use one of {sorted(RANK)}")
            ev.append((round(t0 + float(c["t"]), 3), c["cat"], key + ":" + c.get("why", "")))
    return ev


def thin(ev):
    kept, last = [], {}
    for t, cat, why in sorted(ev, key=lambda e: (-RANK[e[1]], e[0])):
        if any(abs(t - lt) < MIN_GAP[cat] for lt in last.get(cat, [])):
            continue
        # a swell sounds BEFORE its cue (it ends on the hit), so it never crowds the hit itself
        if cat != "swell" and sum(1 for k in kept if k[1] != "swell" and abs(k[0] - t) < 0.3) >= 2:
            continue
        kept.append((t, cat, why))
        last.setdefault(cat, []).append(t)
    return sorted(kept)


def repitch(seg, semis):
    if abs(semis) < 0.05:
        return seg
    n = int(len(seg) / 2 ** (semis / 12))
    x = np.linspace(0, len(seg) - 1, n)
    return np.stack([np.interp(x, np.arange(len(seg)), seg[:, c]) for c in range(2)], 1).astype(np.float32)


def place(out, t, cat, take, rng):
    _, y, hp = take
    lead = {"swell": PLAY["swell"], "swoosh": hp}.get(cat, 0.012)
    a = max(0, int(round((hp - lead) * SR)))
    seg = y[a:a + int((PLAY[cat] + lead) * SR)].copy()
    if len(seg) < 64:
        return
    seg = repitch(seg, rng.uniform(-PITCH.get(cat, 0), PITCH.get(cat, 0)))
    rms_db = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    seg *= 10 ** ((TARGET_DB[cat] + rng.uniform(-1.2, 1.2) - rms_db) / 20)
    pk = np.abs(seg).max()
    if pk > 0.8:
        seg *= 0.8 / pk
    fade = min(len(seg), int(0.06 * SR))
    seg[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    s = int(round((t - lead) * SR))
    if s < 0:
        seg, s = seg[-s:], 0
    seg = seg[:max(0, len(out) - s)]
    out[s:s + len(seg)] += seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--lib", default=DEFAULT_LIB)
    ap.add_argument("--out", default="assets/sfx-mix.wav")
    ap.add_argument("--dry-run", action="store_true", help="print the thinned cue list, render nothing")
    a = ap.parse_args()
    starts, dur = frame_starts(a.project)
    raw = cues(a.project, starts)
    ev = thin(raw)
    counts = {}
    for _, c, _ in ev:
        counts[c] = counts.get(c, 0) + 1
    print(f"cues: {len(raw)}  after thinning: {len(ev)}  ({len(ev) / dur:.2f}/s over {dur:.1f} s)")
    print("per category:", dict(sorted(counts.items())))
    bounds = sorted(starts.items(), key=lambda kv: kv[1]) + [("_end", dur)]
    for (key, t0), (_, t1) in zip(bounds, bounds[1:]):
        inside = [e for e in ev if t0 <= e[0] < t1]
        dens = len(inside) / max(t1 - t0, 0.1)
        flag = "  <- dense, reads as forced" if dens > 1.5 else ""
        print(f"{key:24s} {len(inside):3d} ({dens:.2f}/s){flag}  " + " ".join(f"{t - t0:.2f}{c[:3]}" for t, c, _ in inside))
    if a.dry_run:
        return
    lib = library(a.lib)
    missing = sorted({c for _, c, _ in ev} - set(lib))
    if missing:
        raise SystemExit(f"library {a.lib} has no takes for {missing}")
    out = np.zeros((int(dur * SR), 2), np.float32)
    rr, rng = {}, np.random.default_rng(7)
    for t, cat, _ in ev:
        i = rr.get(cat, 0)
        rr[cat] = i + 1
        place(out, t, cat, lib[cat][i % len(lib[cat])], rng)
    pk = np.abs(out).max()
    if pk > 0.89:
        out *= 0.89 / pk
    path = a.out if os.path.isabs(a.out) else os.path.join(a.project, a.out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", path], input=out.tobytes(), check=True)
    print(path)


if __name__ == "__main__":
    main()
