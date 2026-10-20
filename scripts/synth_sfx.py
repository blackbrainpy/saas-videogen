"""The 13-sound kit for kinetic launch videos.

    python synth_sfx.py <out_dir>                        # synthesize the whole kit (offline)
    python synth_sfx.py --normalize <downloads> <out_dir>  # trim + level downloaded sounds
                                                           # (files named whoosh-fast.mp3 etc.), then
                                                           # synthesize whatever is still missing

Sounds: whoosh-fast, swoosh-soft, swoosh-reverse, riser, pop, click, tick,
counter-roll, glitch, typing, impact, shimmer, chime. Everything is
deterministic (fixed seeds), loudness-matched and written as 44.1 kHz MP3.
Prints each file's length — put those in the style table.
"""

import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 44100
NAMES = ["whoosh-fast", "swoosh-soft", "swoosh-reverse", "riser", "pop", "click", "tick",
         "counter-roll", "glitch", "typing", "impact", "shimmer", "chime"]


def t_(sec):
    return np.arange(int(SR * sec)) / SR


def lowpass_sweep(x, f0, f1):
    """One-pole low-pass whose cutoff sweeps f0 -> f1 (Hz) across the signal."""
    y = np.zeros_like(x)
    fc = np.linspace(f0, f1, len(x))
    a = np.exp(-2 * np.pi * fc / SR)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def env(n, attack, release, shape=2.0):
    a = int(n * attack)
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a) ** shape if a else 1
    r = int(n * release)
    e[n - r:] *= np.linspace(1, 0, r) ** shape if r else 1
    return e


def whoosh(sec, f0, f1, seed, peak_at=0.55):
    rng = np.random.default_rng(seed)
    n = int(SR * sec)
    noise = rng.standard_normal(n)
    up = int(n * peak_at)
    sweep = np.concatenate([np.linspace(f0, f1, up), np.linspace(f1, f0 * 0.8, n - up)])
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * sweep[i] / SR)
        acc = (1 - a) * noise[i] + a * acc
        y[i] = acc
    hp = y - lowpass_sweep(y, 180, 180)
    shape = np.concatenate([np.linspace(0, 1, up) ** 2.2, np.linspace(1, 0, n - up) ** 1.6])
    return hp * shape


def synth():
    out = {}
    out["whoosh-fast"] = whoosh(0.5, 600, 5200, 1, 0.5)
    soft = whoosh(1.5, 250, 2200, 2, 0.6)
    out["swoosh-soft"] = soft
    out["swoosh-reverse"] = soft[::-1].copy()
    t = t_(0.8)
    glide = np.cumsum(np.linspace(180, 1400, len(t))) / SR
    rng = np.random.default_rng(3)
    out["riser"] = (0.5 * np.sin(2 * np.pi * glide) + 0.35 * lowpass_sweep(rng.standard_normal(len(t)), 300, 6000)) \
        * np.linspace(0, 1, len(t)) ** 2.5
    t = t_(0.25)
    f = np.linspace(950, 320, len(t))
    out["pop"] = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22) * env(len(t), 0.02, 0.2)
    t = t_(0.09)
    out["click"] = (0.9 * np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 120) + 0.5 * np.sin(2 * np.pi * 700 * t)
                    * np.exp(-t * 60) + 0.4 * np.random.default_rng(4).standard_normal(len(t)) * np.exp(-t * 600))
    t = t_(0.06)
    tick = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 90) + 0.35 * np.random.default_rng(5).standard_normal(len(t)) * np.exp(-t * 400)
    out["tick"] = tick
    roll = np.zeros(int(SR * 1.0))
    gap, pos, k = 0.035, 0.0, 0
    while pos < 0.95:
        i = int(pos * SR)
        seg = tick * (0.6 + 0.4 * ((k % 2) == 0))
        roll[i:i + len(seg)] += seg[: len(roll) - i]
        pos += gap
        gap *= 1.09
        k += 1
    out["counter-roll"] = roll
    rng = np.random.default_rng(6)
    n = int(SR * 0.5)
    g = np.zeros(n)
    for j in range(14):
        s = int(rng.uniform(0, 0.45) * SR)
        l = int(rng.uniform(0.01, 0.04) * SR)
        f0 = rng.uniform(200, 2500)
        tt = np.arange(l) / SR
        g[s:s + l] += np.sign(np.sin(2 * np.pi * f0 * tt)) * 0.5 + 0.3 * rng.standard_normal(l)
    out["glitch"] = np.round(g * 6) / 6 * env(n, 0.01, 0.3)
    typing = np.zeros(int(SR * 0.8))
    rng = np.random.default_rng(7)
    pos = 0.02
    while pos < 0.75:
        i = int(pos * SR)
        tt = t_(0.03)
        key = (np.sin(2 * np.pi * rng.uniform(1800, 2600) * tt) * np.exp(-tt * 180) + 0.6 * rng.standard_normal(len(tt)) * np.exp(-tt * 300))
        typing[i:i + len(key)] += key * rng.uniform(0.5, 1.0)
        pos += rng.uniform(0.05, 0.11)
    out["typing"] = typing
    t = t_(1.2)
    f = 42 + 70 * np.exp(-t * 9)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    hit = lowpass_sweep(np.random.default_rng(8).standard_normal(len(t)), 2500, 400) * np.exp(-t * 14)
    out["impact"] = boom + 0.6 * hit
    t = t_(1.0)
    sh = np.zeros(len(t))
    for j, fr in enumerate([2093, 2637, 3136, 3951, 4699, 5274]):
        start = j * 0.06
        tt = np.clip(t - start, 0, None)
        sh += (t >= start) * np.sin(2 * np.pi * fr * tt) * np.exp(-tt * 4.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt))
    out["shimmer"] = sh * env(len(t), 0.03, 0.4)
    t = t_(1.0)
    ch = np.zeros(len(t))
    for start, fr in [(0.0, 1318.5), (0.13, 1975.5)]:
        tt = np.clip(t - start, 0, None)
        note = sum(np.sin(2 * np.pi * fr * h * tt) / h ** 1.6 for h in (1, 2, 3))
        ch += (t >= start) * note * np.exp(-tt * 5)
    out["chime"] = ch
    return out


def write_mp3(x, path):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    y = (np.repeat(x[:, None], 2, 1) * 32767).astype(np.int16)
    tmp = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y.tobytes())
    level(tmp, path)
    os.remove(tmp)


def level(src, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af",
                    "silenceremove=start_periods=1:start_threshold=-55dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-60dB,areverse,loudnorm=I=-16:TP=-2",
                    "-ar", "44100", "-ac", "2", "-b:a", "192k", dst], check=True)


def length(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout)


def main(argv):
    downloads = None
    if argv and argv[0] == "--normalize":
        downloads, argv = argv[1], argv[2:]
    out = argv[0]
    os.makedirs(out, exist_ok=True)
    have = set()
    if downloads:
        for name in NAMES:
            for ext in (".mp3", ".wav"):
                p = os.path.join(downloads, name + ext)
                if os.path.exists(p):
                    level(p, os.path.join(out, name + ".mp3"))
                    have.add(name)
                    break
    kit = synth()
    for name in NAMES:
        if name in have:
            continue
        if name == "swoosh-reverse" and "swoosh-soft" in have:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(out, "swoosh-soft.mp3"),
                            "-af", "areverse", "-b:a", "192k", os.path.join(out, "swoosh-reverse.mp3")], check=True)
            continue
        write_mp3(kit[name], os.path.join(out, name + ".mp3"))
    for name in NAMES:
        print(f"{name:15s} {length(os.path.join(out, name + '.mp3')):.2f}s  {'downloaded' if name in have else 'synthesized'}")


if __name__ == "__main__":
    main(sys.argv[1:])
