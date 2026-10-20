"""Break reference videos into timestamped contact sheets, cut list and audio profile.

    python -I analyze_refs.py <ref_dir> [step_seconds]
"""
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def sheets(path, out_dir, step, cols=6, rows=5, w=320):
    dur = probe(path)
    name = os.path.splitext(os.path.basename(path))[0]
    frames_dir = os.path.join(out_dir, name + "_f")
    os.makedirs(frames_dir, exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-vf", f"fps=1/{step},scale={w}:-2",
                    os.path.join(frames_dir, "%04d.jpg")], check=True)
    files = sorted(os.listdir(frames_dir))
    if not files:
        return dur, 0
    first = Image.open(os.path.join(frames_dir, files[0]))
    fw, fh = first.size
    per = cols * rows
    for s in range(0, len(files), per):
        chunk = files[s:s + per]
        sheet = Image.new("RGB", (fw * cols, (fh + 18) * rows), (20, 20, 20))
        d = ImageDraw.Draw(sheet)
        for k, f in enumerate(chunk):
            x, y = (k % cols) * fw, (k // cols) * (fh + 18)
            sheet.paste(Image.open(os.path.join(frames_dir, f)), (x, y + 18))
            t = (s + k) * step
            d.text((x + 4, y + 3), f"{t:.1f}s", fill=(255, 220, 0))
        sheet.save(os.path.join(out_dir, f"{name}_sheet{s // per + 1:02d}.jpg"), quality=88)
    return dur, len(files)


def cuts(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return [round(float(m), 2) for m in re.findall(r"pts_time:([\d.]+)", r)]


def audio(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    il = [l.strip() for l in r.splitlines() if l.strip().startswith("I:")]
    vd = subprocess.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    mx = re.search(r"max_volume: ([-\d.]+)", vd)
    return (il[-1] if il else "?"), (mx.group(1) if mx else "?")


def main(ref_dir, step):
    out = os.path.join(ref_dir, "analysis")
    os.makedirs(out, exist_ok=True)
    for f in sorted(os.listdir(ref_dir)):
        if not f.endswith(".mp4"):
            continue
        p = os.path.join(ref_dir, f)
        dur = probe(p)
        st = step if dur > 10 else 0.2
        d, n = sheets(p, out, st)
        c = cuts(p)
        loud, peak = audio(p)
        gaps = [round(b - a, 2) for a, b in zip([0] + c, c + [dur])]
        print(f"{f}: {dur:.1f}s, {n} frames @{st}s, loud {loud}, peak {peak} dB")
        print(f"  cuts ({len(c)}): {c}")
        print(f"  shot lengths: {gaps}")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.5)
