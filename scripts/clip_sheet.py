"""Timestamped contact sheet of one clip (N evenly spaced frames).

    python -P clip_sheet.py <clip> <out.jpg> [frames=18] [cols=6] [width=400]
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def main(clip, out, n=18, cols=6, w=400):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                               capture_output=True, text=True, check=True).stdout)
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(n):
            t = dur * (i + 0.5) / n
            fp = os.path.join(tmp, f"{i}.jpg")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", clip, "-frames:v", "1",
                            "-vf", f"scale={w}:-2", fp], check=True)
            tiles.append((t, Image.open(fp).copy()))
    th = tiles[0][1].height
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (th + 16)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (t, im) in enumerate(tiles):
        x, y = (i % cols) * w, (i // cols) * (th + 16)
        sheet.paste(im, (x, y + 16))
        d.text((x + 4, y + 2), f"{t:.2f}s", fill=(255, 220, 0))
    sheet.save(out, quality=86)
    print(f"{out} ({dur:.2f}s)")


if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], *(int(x) for x in a[3:6]))
