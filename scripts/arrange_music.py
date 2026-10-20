"""Lengthen a music track by re-arranging its own sections on bar lines.

    python -P arrange_music.py <src> <out.mp3> --bar0 12.283 --beat 0.7585 \
        --plan "0:b0, b0:b8, b8:b11, b0:b8, b8:b11, b0:b8, b8:b12, b12:end" [--xfade 0.03] [--fade-out 1.0]

Plan items are "start:end" with times in seconds or bar lines "bN" (bar0 + N*4*beat),
"end" = end of file. Contiguous items join without a seam; jumps get an equal-power
crossfade. Prints the seam times and each section's start in the new timeline.
"""
import argparse
import subprocess

import numpy as np

SR = 48000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--bar0", type=float, required=True)
    ap.add_argument("--beat", type=float, required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--xfade", type=float, default=0.03)
    ap.add_argument("--fade-out", type=float, default=1.0)
    a = ap.parse_args()
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.src, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).reshape(-1, 2)
    total = len(y) / SR

    def tm(s):
        s = s.strip()
        if s == "end":
            return total
        if s.startswith("b"):
            return a.bar0 + float(s[1:]) * 4 * a.beat
        return float(s)

    plan = [tuple(tm(x) for x in item.split(":")) for item in a.plan.split(",")]
    xf = int(a.xfade * SR)
    fo = np.cos(np.linspace(0, np.pi / 2, xf))[:, None]
    fi = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]
    out, prev_end = None, None
    for s, e in plan:
        seg = y[int(round(s * SR)):int(round(e * SR))].copy()
        start_new = 0.0 if out is None else len(out) / SR
        if out is None:
            out = seg
        elif abs(s - prev_end) < 1e-3:
            out = np.concatenate([out, seg])
        else:
            out[-xf:] = out[-xf:] * fo + seg[:xf] * fi
            out = np.concatenate([out, seg[xf:]])
            start_new -= a.xfade
            print(f"seam at {start_new:.3f}s (source {prev_end:.3f} -> {s:.3f})")
        print(f"  section {s:7.3f}-{e:7.3f}  starts at {start_new:7.3f}s")
        prev_end = e
    n = int(a.fade_out * SR)
    out[-n:] *= np.linspace(1, 0, n)[:, None]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "libmp3lame", "-q:a", "0", a.out], input=out.astype(np.float32).tobytes(), check=True)
    print(f"{a.out}: {len(out) / SR:.2f}s")


if __name__ == "__main__":
    main()
