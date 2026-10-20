"""Pre-mix each frame's sound effects into one audio file per frame.

    python -P bake_sfx.py <project> [--frames-glob "compositions/frames/*.html"]

Long films with hundreds of <audio> sfx tags make the HyperFrames audio mix
fail on Windows ("spawn ENAMETOOLONG"). This keeps the originals in
.kinetic/frames-presfx/, renders every frame's sfx (src, data-start,
data-duration, data-volume, data-media-start) into assets/sfx-baked/<frame>.wav
and swaps those tags for ONE <audio> that plays the mix from 0.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess


def attr(tag, name, default=None):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return m.group(1) if m else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--frames-glob", default="compositions/frames/*.html")
    a = ap.parse_args()
    p = a.project
    os.makedirs(os.path.join(p, "assets", "sfx-baked"), exist_ok=True)
    os.makedirs(os.path.join(p, ".kinetic", "frames-presfx"), exist_ok=True)
    for fi, f in enumerate(sorted(glob.glob(os.path.join(p, a.frames_glob)))):
        html = open(f, encoding="utf-8").read()
        name = os.path.splitext(os.path.basename(f))[0]
        tags = re.findall(r"<audio\b[^>]*>(?:\s*</audio>)?", html)
        tags = [t for t in tags if "sfx-baked" not in t]
        if not tags:
            continue
        shutil.copy(f, os.path.join(p, ".kinetic", "frames-presfx", os.path.basename(f)))
        dur = float(re.search(r'data-composition-id="[^"]+"[^>]*data-duration="([\d.]+)"', html).group(1))
        inputs, chains = [], []
        for i, t in enumerate(tags):
            src = os.path.join(p, attr(t, "src"))
            start = float(attr(t, "data-start", "0"))
            d = float(attr(t, "data-duration", "1"))
            vol = float(attr(t, "data-volume", "1"))
            ms = float(attr(t, "data-media-start", "0"))
            inputs += ["-ss", f"{ms:.3f}", "-t", f"{d:.3f}", "-i", src]
            delay = int(round(start * 1000))
            chains.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},"
                          f"adelay={delay}|{delay}[a{i}]")
        mix = "".join(f"[a{i}]" for i in range(len(tags)))
        fc = ";".join(chains) + f";{mix}amix=inputs={len(tags)}:normalize=0:dropout_transition=0,apad,atrim=0:{dur}[out]"
        out = os.path.join(p, "assets", "sfx-baked", name + ".wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
                        "-ar", "48000", "-ac", "2", out], check=True)
        first = True

        def swap(m):
            nonlocal first
            if "sfx-baked" in m.group(0):
                return m.group(0)
            if first:
                first = False
                return (f'<audio id="{name}-sfxmix" src="assets/sfx-baked/{name}.wav" data-start="0" '
                        f'data-duration="{dur}" data-track-index="{900 + fi}" data-volume="1" '
                        f'data-hf-media-start-basis="local"></audio>')
            return ""
        html = re.sub(r"<audio\b[^>]*>(?:\s*</audio>)?", swap, html)
        open(f, "w", encoding="utf-8").write(html)
        print(f"{name}: {len(tags)} sfx -> {os.path.relpath(out, p)}")


if __name__ == "__main__":
    main()
