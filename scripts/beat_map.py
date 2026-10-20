"""Hit map of a music track for beat-locked editing.

    python -P beat_map.py <music> <STORYBOARD.md> <out.md> [--sens 1.0]

Finds every audible onset (spectral flux peaks, 20 ms hop), grades it
  A = big hit (top ~8% by strength or a loudness jump > 9 dB)
  B = clear beat/accent (next ~25%)
  C = soft tick (the rest above threshold)
measures energy per half second (calm / mid / drive / silence), and writes a
per-frame table in frame-local time using the storyboard's "- start:" and
"- duration:" lines. Frame workers put a visual event on every A and B hit
and let C hits carry small details.
"""
import re
import subprocess
import sys

import numpy as np

SR, HOP = 22050, 441


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def analyse(y, sens):
    n = len(y) // HOP
    fr = y[:n * HOP].reshape(n, HOP)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    mag = np.abs(np.fft.rfft(fr * np.hanning(HOP), axis=1))
    flux = np.r_[0, np.maximum(np.diff(np.log1p(mag * 10), axis=0), 0).sum(axis=1)]
    med = np.convolve(flux, np.ones(31) / 31, mode="same")
    thr = med + sens * 0.9 * flux.std()
    peaks, last = [], -99
    for i in range(1, n - 1):
        if flux[i] > thr[i] and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and i - last >= 6:
            jump = db[i:i + 4].max() - db[max(0, i - 6):i].mean()
            peaks.append((i / 50, float(flux[i]), float(jump)))
            last = i
    s = np.array([p[1] for p in peaks])
    a_cut, b_cut = np.quantile(s, 0.92), np.quantile(s, 0.67)
    hits = [(t, "A" if (f >= a_cut or j > 9) else "B" if f >= b_cut else "C") for t, f, j in peaks]
    halves = []
    for k in range(int(len(y) / SR * 2)):
        seg = db[k * 25:(k + 1) * 25]
        cnt = sum(1 for t, _ in hits if k / 2 <= t < k / 2 + 0.5)
        m = seg.mean()
        halves.append((k / 2, m, "silence" if m < -30 else "drive" if (m > -13 and cnt >= 1) else "mid" if m > -21 else "calm"))
    return hits, halves


def frames(path):
    text = open(path, encoding="utf-8").read()
    out = []
    for block in re.split(r"^##\s+Frame\s+", text, flags=re.M)[1:]:
        name = block.splitlines()[0].strip()
        st = float(re.search(r"^-\s*start:\s*([\d.]+)", block, re.M).group(1))
        du = float(re.search(r"^-\s*duration:\s*([\d.]+)", block, re.M).group(1))
        out.append((name, st, du))
    return out


def main(argv):
    music, sb, out = argv[:3]
    sens = float(argv[argv.index("--sens") + 1]) if "--sens" in argv else 1.0
    hits, halves = analyse(load(music), sens)
    lines = ["# Beat map", "", f"Music: {music}. Grades: **A** big hit (must be a big visual event: morph, cut, reveal),",
             "**B** clear beat (a visible event: word, swap, hop, pop, press), **C** soft tick (small detail: a reading,",
             "a sparkle, a letter). Energy per half second: calm = slow cascades and long holds; mid = steady moves;",
             "drive = something changes on every beat; silence = stillness (hold, or one quiet move with no new sound).",
             f"All hits: {len(hits)} (A {sum(g == 'A' for _, g in hits)}, B {sum(g == 'B' for _, g in hits)}, C {sum(g == 'C' for _, g in hits)}).", ""]
    for name, st, du in frames(sb):
        lines.append(f"## Frame {name}  (film {st:.2f}–{st + du:.2f})")
        fh = [(t, g) for t, g in hits if st - 0.02 <= t < st + du - 0.02]
        lines.append("- hits (frame-local s): " + ", ".join(f"{t - st:.2f}{g}" for t, g in fh) if fh else "- hits: none")
        en = [(t, e) for t, _, e in halves if st <= t < st + du]
        runs, cur = [], None
        for t, e in en:
            if cur and cur[1] == e:
                cur[2] = t + 0.5
            else:
                cur = [t, e, t + 0.5]
                runs.append(cur)
        lines.append("- energy: " + "; ".join(f"{a - st:.1f}–{min(b, st + du) - st:.1f} {e}" for a, e, b in runs))
        lines.append("")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"{out}: {len(hits)} hits")


if __name__ == "__main__":
    main(sys.argv[1:])
