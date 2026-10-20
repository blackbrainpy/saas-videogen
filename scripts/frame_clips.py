"""Bake a slow camera punch-in into clips, so small UI (a menu bar, a notch, a
toolbar) reads at video size. Output: <name>-framed.mp4 next to the source.

    python frame_clips.py spec.json

spec.json:
{
  "clips_dir": "videos/_footage/clips",
  "cams": {
    "hover-open": [[320, 0, 1280], [460, 0, 1000]],   # from-region -> to-region
    "calls":      [[480, 0, 960]]                      # one region = static framing that creeps in 5%
  }
}

A region is [x, y, width] on the 1920x1080 source; height follows at 16:9.
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

PUSH = 0.05
SCALE = 2


def smooth(expr: str) -> str:
    return f"(({expr})*({expr})*(3-2*({expr})))"


def framed(clips_dir: str, name: str, start, end) -> str:
    src = os.path.join(clips_dir, name + ".mp4")
    dst = os.path.join(clips_dir, name + "-framed.mp4")
    x0, y0, w0 = start
    x1, y1, w1 = end
    if (x0, y0, w0) == (x1, y1, w1):
        cx, cy = x0 + w0 / 2, y0 + w0 * 9 / 32
        w1 = w0 * (1 - PUSH)
        x1, y1 = cx - w1 / 2, max(0.0, cy - w1 * 9 / 32)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
        capture_output=True, text=True, check=True).stdout)
    frames = max(1, round(dur * 30) - 1)
    p = smooth(f"min(1,on/{frames})")
    w = f"({w0}+({w1}-{w0})*{p})"
    vf = (f"scale={1920 * SCALE}:{1080 * SCALE}:flags=lanczos,"
          f"zoompan=z='1920/{w}':x='{SCALE}*({x0}+({x1}-{x0})*{p})':y='{SCALE}*({y0}+({y1}-{y0})*{p})'"
          f":d=1:s=1920x1080:fps=30,format=yuv420p")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf, "-an", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "18", "-g", "15", "-movflags", "+faststart", dst], check=True)
    return name


def main(spec_path: str) -> None:
    spec = json.load(open(spec_path, encoding="utf-8"))
    d = spec["clips_dir"]
    jobs = [(n, r[0], r[-1]) for n, r in spec["cams"].items()]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for n in pool.map(lambda j: framed(d, *j), jobs):
            print("framed", n)


if __name__ == "__main__":
    main(sys.argv[1])
