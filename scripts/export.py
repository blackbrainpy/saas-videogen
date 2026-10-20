"""Deliver a rendered kinetic video: loudness-normalised MP4, SRT subtitles
from the word timings, and a frame sheet pulled from the final file.

    python export.py <project> <rendered.mp4> <out_folder> <name> [--lufs -15]

Writes <out>/<name>.mp4, <name>.srt, <name>-sheet.jpg and prints duration,
size and measured loudness.
"""

import json
import os
import re
import subprocess
import sys

from PIL import Image


def ts(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def srt(project, path):
    idx = open(os.path.join(project, "index.html"), encoding="utf-8").read()
    starts = {}
    for m in re.finditer(r'id="el-(\d+)-[^"]*"\s+class="scene"[\s\S]*?data-start="([\d.]+)"', idx):
        starts[int(m.group(1))] = float(m.group(2))
    meta = json.load(open(os.path.join(project, "audio_meta.json")))
    cues = []
    for v in meta.get("voices", []):
        off, cur = starts.get(v["frame"], 0.0), []
        for w in v["words"]:
            cur.append(w)
            if (w["text"][-1] in ".?!,:" and len(cur) >= 3) or len(cur) >= 7:
                cues.append([off + cur[0]["start"], off + cur[-1]["end"] + 0.25, " ".join(x["text"] for x in cur)])
                cur = []
        if cur:
            cues.append([off + cur[0]["start"], off + cur[-1]["end"] + 0.25, " ".join(x["text"] for x in cur)])
    for i in range(len(cues) - 1):
        cues[i][1] = min(cues[i][1], cues[i + 1][0])
    open(path, "w", encoding="utf-8").write("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues, 1)))
    return len(cues)


def main(argv):
    project, rendered, out, name = argv[:4]
    lufs = float(argv[argv.index("--lufs") + 1]) if "--lufs" in argv else -15.0
    os.makedirs(out, exist_ok=True)
    mp4 = os.path.join(out, name + ".mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", rendered, "-c:v", "copy", "-af",
                    f"loudnorm=I={lufs}:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                    "-movflags", "+faststart", mp4], check=True)
    n = srt(project, os.path.join(out, name + ".srt")) if os.path.exists(os.path.join(project, "audio_meta.json")) else 0
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                               capture_output=True, text=True, check=True).stdout)
    W, H, cols, rows = 480, 270, 4, 4
    sheet = Image.new("RGB", (W * cols, H * rows))
    tmp = os.path.join(out, "_frame.jpg")
    for i in range(cols * rows):
        t = dur * (i + 0.5) / (cols * rows)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1",
                        "-vf", f"scale={W}:{H}", tmp], check=True)
        sheet.paste(Image.open(tmp), ((i % cols) * W, (i // cols) * H))
    os.remove(tmp)
    sheet.save(os.path.join(out, name + "-sheet.jpg"), quality=85)
    loud = subprocess.run(["ffmpeg", "-i", mp4, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = [l.strip() for l in loud.splitlines() if l.strip().startswith("I:")]
    print(f"{mp4}\n  {dur:.1f} s, {os.path.getsize(mp4) / 1e6:.1f} MB, {i[-1] if i else ''}, {n} subtitle cues")


if __name__ == "__main__":
    main(sys.argv[1:])
