"""Score candidate music tracks against a launch-film shape.

    python -P track_fit.py <track.mp3> [<track2.mp3> ...] [--drop 8] [--dropout 50]

For each track prints: duration, tempo estimate, intro loudness (first 6 s)
vs body, the biggest loudness jump (where the drop really lands), dips that
could serve as the dropout, and a 1-second loudness strip to eyeball the shape.
"""
import subprocess
import sys

import numpy as np

SR, HOP = 22050, 441  # 20 ms frames


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def tempo(y):
    n = len(y) // HOP
    mag = np.abs(np.fft.rfft(y[:n * HOP].reshape(n, HOP) * np.hanning(HOP), axis=1))
    f = np.maximum(np.diff(np.log1p(mag * 10), axis=0), 0).sum(axis=1)
    f = f - f.mean()
    ac = np.correlate(f, f, "full")[len(f) - 1:]
    lo, hi = int(50 * 60 / 160), int(50 * 60 / 70)
    return 60 / ((lo + int(np.argmax(ac[lo:hi]))) / 50)


def loud_per_second(y):
    s = len(y) // SR
    rms = np.sqrt((y[:s * SR].reshape(s, SR) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms)


def report(path, drop, dropout):
    y = pcm(path)
    db = loud_per_second(y)
    body = float(np.median(db[10:-5])) if len(db) > 20 else float(np.median(db))
    intro = float(db[:6].mean())
    jumps = np.diff(db)
    j = int(np.argmax(jumps[2:20])) + 3
    dips = [i for i in range(10, len(db) - 3) if db[i] < body - 6]
    print(f"\n== {path.split('/')[-1]}  {len(y) / SR:.1f}s  ~{tempo(y):.0f} bpm")
    print(f"  intro {intro:.1f} dB vs body {body:.1f} dB ({intro - body:+.1f}); biggest early jump at {j}s "
          f"(+{jumps[j - 1]:.1f} dB; target {drop}s)")
    print(f"  dips >6 dB below body: {dips or 'none'} (target ~{dropout}s)")
    print("  " + "".join(" .:-=+*#%@"[max(0, min(9, int((d - body + 18) / 3)))] for d in db))


def main(argv):
    drop = float(argv[argv.index("--drop") + 1]) if "--drop" in argv else 8
    dropout = float(argv[argv.index("--dropout") + 1]) if "--dropout" in argv else 50
    for p in [a for a in argv if a.endswith((".mp3", ".wav", ".m4a"))]:
        report(p, drop, dropout)


if __name__ == "__main__":
    main(sys.argv[1:])
