"""Cut 9:16 social clips (Reels / TikTok / Shorts) from a 16:9 launch film on the light ground.

    python -P social_cuts.py <film.mp4> <cuts.json> <out_dir> [--prefix Product-Vertical]
                             [--tail 123.5:127.0] [--crop-w 1600] [--ground "242,242,240"] [--font <ttf>]

cuts.json: [{"name": "01-what-it-is", "start": 0.0, "end": 17.75, "hook": "A focus timer|for your desktop."}, ...]
("|" breaks the hook line; keep each line <= ~26 characters). --tail = the end card's Store-CTA span in the film,
appended to every clip that does not already end on it (clips ending within 1 s of the film's end keep their own).

Layout on 1080x1920: the hook line in Geist SemiBold (ink on the ground) in the top band, the film's centre
crop (crop-w x full height) scaled to 1080 wide in the middle, the film's own top/bottom rows stretched to
fill the rest, with the bottom glow fading into the ground so there is no seam. Loudness -14 LUFS.
Output is SAR 1:1 with bt709 tags: X and Instagram reject anything else (a stretched strip through vstack
otherwise carries a 9125:243 SAR). Every scaled height is EVEN: odd heights crash ffmpeg 8.1 in yuv420p.
"""
import argparse
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(os.path.dirname(HERE), "assets", "fonts", "Geist-SemiBold.ttf")
INK = (17, 17, 20, 255)
TOP_H = 600


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "default=nw=1", path],
                         capture_output=True, text=True, check=True).stdout
    kv = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
    return int(kv["width"]), int(kv["height"]), float(kv["duration"])


def overlay_png(text, path, vid_h, ground, font_path):
    """Full-canvas overlay: the hook on top, and a fade from the film's glow into the ground below it."""
    font = ImageFont.truetype(font_path, 66)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = text.split("|")
    lh = 82
    y = TOP_H // 2 + 30 - len(lines) * lh // 2
    for ln in lines:
        d.text(((1080 - d.textlength(ln, font=font)) / 2, y), ln, font=font, fill=INK)
        y += lh
    fill_h = 1920 - TOP_H - vid_h
    for i in range(fill_h):
        alpha = int(255 * min(1.0, i / (fill_h * 0.55)) ** 1.6)
        d.line([(0, TOP_H + vid_h + i), (1079, TOP_H + vid_h + i)], fill=ground + (alpha,))
    img.save(path)


def cut(film, film_info, c, out_dir, a):
    fw, fh, fdur = film_info
    vid_h = int(round(fh * 1080 / a.crop_w / 2)) * 2
    png = os.path.join(out_dir, f".hook-{c['name']}.png")
    overlay_png(c["hook"], png, vid_h, a.ground, a.font)
    start, end = float(c["start"]), float(c["end"])
    tail = a.tail if a.tail and end < fdur - 1.0 else None
    seg = end - start
    inputs = ["-ss", f"{start:.3f}", "-t", f"{seg:.3f}", "-i", film]
    if tail:
        inputs += ["-ss", f"{tail[0]:.3f}", "-t", f"{tail[1] - tail[0]:.3f}", "-i", film]
    png_idx = 2 if tail else 1
    inputs += ["-i", png]
    fc = [f"[0:a]afade=t=in:d=0.08,afade=t=out:st={seg - 0.35:.3f}:d=0.35[a0]"]
    if tail:
        tl = tail[1] - tail[0]
        fc += ["[0:v][1:v]concat=n=2:v=1:a=0[v0]",
               f"[1:a]afade=t=in:d=0.3,afade=t=out:st={tl - 0.6:.3f}:d=0.6[a1]",
               "[a0][a1]concat=n=2:v=0:a=1[ac]"]
    else:
        fc += ["[0:v]null[v0]", "[a0]anull[ac]"]
    x = (fw - a.crop_w) // 2
    fc += [f"[v0]crop={a.crop_w}:{fh}:{x}:0,scale=1080:{vid_h}:flags=lanczos,format=yuv444p,setsar=1,split=3[m][t][bt]",
           f"[t]crop=1080:16:0:0,scale=1080:{TOP_H}:flags=bilinear,setsar=1[top]",
           f"[bt]crop=1080:16:0:{vid_h - 16},scale=1080:{1920 - TOP_H - vid_h}:flags=bilinear,setsar=1[bot]",
           "[top][m][bot]vstack=inputs=3[stk]",
           f"[stk][{png_idx}:v]overlay=0:0,setsar=1,format=yuv420p,"
           "setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]",
           "[ac]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"]
    out = os.path.join(out_dir, f"{a.prefix}-{c['name']}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-r", "30",
                    "-aspect", "9:16", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(png)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("cuts")
    ap.add_argument("out_dir")
    ap.add_argument("--prefix", default="Vertical")
    ap.add_argument("--tail", help="start:end of the end-card CTA in the film, e.g. 123.5:127.0")
    ap.add_argument("--crop-w", type=int, default=1600)
    ap.add_argument("--ground", default="242,242,240")
    ap.add_argument("--font", default=FONT)
    a = ap.parse_args()
    a.tail = tuple(float(v) for v in a.tail.split(":")) if a.tail else None
    a.ground = tuple(int(v) for v in a.ground.split(","))
    os.makedirs(a.out_dir, exist_ok=True)
    info = probe(a.film)
    for c in json.load(open(a.cuts, encoding="utf-8")):
        out = cut(a.film, info, c, a.out_dir, a)
        w, h, d = probe(out)
        sar = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=sample_aspect_ratio", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
        print(f"{os.path.basename(out)}  {d:.1f}s  {w}x{h}  SAR {sar}")


if __name__ == "__main__":
    main()
