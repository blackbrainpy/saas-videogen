"""Turn downloaded SFX generations into a clean, de-duplicated variation library.

    python -P build_sfx_library.py <download_dir> <out_dir> "<prefix>=<category>" ...

Each downloaded WAV whose name starts with <prefix> becomes <out_dir>/<category>_<n>.wav:
exact duplicates (md5) are dropped, leading silence is trimmed (−50 dB), the tail is
trimmed after the sound decays (−55 dB for 0.25 s), a 20 ms fade-out is added and
every file is peak-normalised to −3 dBFS so variations in a category sit at the same level.
Prints a table: category, variations, durations.
"""
import hashlib
import os
import subprocess
import sys


def main(argv):
    src, out = argv[0], argv[1]
    mapping = [a.split("=", 1) for a in argv[2:]]
    os.makedirs(out, exist_ok=True)
    seen, counts = set(), {}
    for f in sorted(os.listdir(src)):
        if not f.lower().endswith(".wav"):
            continue
        cat = next((c for p, c in mapping if f.startswith(p)), None)
        if not cat:
            continue
        p = os.path.join(src, f)
        h = hashlib.md5(open(p, "rb").read()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        counts[cat] = counts.get(cat, 0) + 1
        dst = os.path.join(out, f"{cat}_{counts[cat]}.wav")
        af = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.005,"
              "areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.25,areverse,"
              "afade=t=out:st=0:d=0,dynaudnorm=f=500:g=31:p=0.708:m=1")
        tmp = dst + ".tmp.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", p, "-af",
                        "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.005,"
                        "areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.25,areverse",
                        "-ar", "48000", "-ac", "2", tmp], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", tmp],
                                   capture_output=True, text=True).stdout or 0)
        vd = subprocess.run(["ffmpeg", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
        peak = float(vd.split("max_volume:")[1].split("dB")[0]) if "max_volume:" in vd else 0.0
        gain = -3.0 - peak
        fade_st = max(0.0, dur - 0.02)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af",
                        f"volume={gain:.2f}dB,afade=t=out:st={fade_st:.3f}:d=0.02", dst], check=True)
        os.remove(tmp)
        print(f"{os.path.basename(dst):24s} {dur:5.2f}s  (from {f})")
    print({k: v for k, v in sorted(counts.items())})


if __name__ == "__main__":
    main(sys.argv[1:])
