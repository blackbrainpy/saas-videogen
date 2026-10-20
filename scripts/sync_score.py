"""Audio onsets vs visual change events, numpy only.

    python -P sync_refs.py <ref_dir>
Prints tempo estimate, onset rate, visual-event rate and how many visual events
have a sound onset within 80 ms (the "every move has a sound" score).
"""
import os
import subprocess
import sys

import numpy as np

SR, HOP = 22050, 441  # 20 ms


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def flux(y):
    n = len(y) // HOP
    frames = y[:n * HOP].reshape(n, HOP) * np.hanning(HOP)
    mag = np.abs(np.fft.rfft(frames, axis=1))
    f = np.maximum(np.diff(np.log1p(mag * 10), axis=0), 0).sum(axis=1)
    return np.concatenate([[0], f])


def peaks(sig, rate, k=1.6, gap=0.09):
    med = np.convolve(sig, np.ones(25) / 25, mode="same")
    thr = med + k * sig.std()
    out, last = [], -1
    for i in range(1, len(sig) - 1):
        if sig[i] > thr[i] and sig[i] >= sig[i - 1] and sig[i] >= sig[i + 1] and (i - last) / rate > gap:
            out.append(i / rate)
            last = i
    return np.array(out)


def tempo(f):
    f = f - f.mean()
    ac = np.correlate(f, f, "full")[len(f) - 1:]
    lo, hi = int(60 / 180 * 50), int(60 / 70 * 50)
    lag = lo + int(np.argmax(ac[lo:hi]))
    return 60 / (lag / 50)


def visual(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", "fps=25,scale=96:54,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, np.uint8).reshape(-1, 54 * 96).astype(np.float32)
    d = np.abs(np.diff(v, axis=0)).mean(axis=1)
    return np.concatenate([[0], d])


def main(ref_dir):
    for f in sorted(os.listdir(ref_dir)):
        if not f.endswith(".mp4"):
            continue
        p = os.path.join(ref_dir, f)
        y = pcm(p)
        fl = flux(y)
        on = peaks(fl, 50)
        vis = peaks(visual(p), 25, k=1.2, gap=0.2)
        dur = len(y) / SR
        hit = sum(1 for t in vis if len(on) and np.min(np.abs(on - t)) < 0.08)
        print(f"== {f} ({dur:.1f}s): ~{tempo(fl):.0f} bpm | audio onsets {len(on)} ({len(on) / dur:.1f}/s) | "
              f"visual events {len(vis)} ({len(vis) / dur:.1f}/s) | visual events with a sound within 80ms: "
              f"{hit}/{len(vis)} ({100 * hit / max(1, len(vis)):.0f}%)")


if __name__ == "__main__":
    main(sys.argv[1])
