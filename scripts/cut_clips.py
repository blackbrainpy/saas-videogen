"""Cut short, seek-friendly clips out of longer screen recordings.

    python cut_clips.py spec.json

spec.json:
{
  "out": "videos/_footage/clips",          # output folder
  "size": "1920x1080",                     # optional, default 1920x1080
  "clips": {
    "hover-open": {"src": "rec/hover.mp4", "start": 13.6, "end": 19.6,
                    "desc": "card springs open at 0.9 s"}
  }
}

Writes <out>/<name>.mp4 (H.264, CRF 18, 30 fps, no audio, keyframe every 15
frames so HyperFrames can seek cleanly) and <out>/clips.md, an asset list with
real lengths for the storyboard.
"""

import json
import os
import subprocess
import sys


def cut(src: str, start: float, end: float, dst: str, size: str) -> None:
    w, h = size.split("x")
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}", "-i", src,
         "-t", f"{end - start:.3f}", "-an", "-vf", vf, "-c:v", "libx264",
         "-preset", "medium", "-crf", "18", "-g", "15", "-movflags", "+faststart", dst],
        check=True,
    )


def main(spec_path: str) -> None:
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = spec["out"]
    size = spec.get("size", "1920x1080")
    os.makedirs(out, exist_ok=True)
    lines = []
    for name, c in spec["clips"].items():
        cut(c["src"], float(c["start"]), float(c["end"]), os.path.join(out, name + ".mp4"), size)
        lines.append(f"- {name}.mp4 [video] {float(c['end']) - float(c['start']):.1f}s — {c.get('desc', '')}")
        print("cut", name)
    with open(os.path.join(out, "clips.md"), "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
