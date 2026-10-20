"""Build index.html for a kinetic launch video.

    python build_index.py <project> [--palette "#050B16,#0A84FF,#1E5BFF,#6CC2FF,#CFE8FF"]
                          [--no-voice] [--music-volume 0.2]

Reads STORYBOARD.md (frames: "## Frame N — …" blocks with "- src:" and
"- duration:"; canvas from frontmatter "format: WxH") and audio_meta.json
(voices + bgm, from align_voice.py). Writes index.html with:
  - a root aurora layer (base colour + three drifting blooms + a faint highlight,
    blurred, vignetted) running the whole film behind every frame;
  - one sub-composition host per frame (id="el-<frame-id>", class="scene"),
    back to back;
  - per-frame voice <audio> (track 10) and the music bed (track 11).
Footage and sound effects live inside the frames. Afterwards run
transitions.mjs inject (product-launch-video) to overlap frames per their
transition_in.
"""

import argparse
import json
import os
import re

BLOB_PATHS = [
    [(-260, -320), (520, -120), (980, 160), (300, 380), (-200, 60), (640, -280), (-260, -320)],
    [(1100, 380), (420, 520), (-120, 300), (700, -60), (1240, 120), (860, 560), (1100, 380)],
    [(760, -260), (1320, 120), (980, 520), (260, -140), (40, 420), (1180, -200), (760, -260)],
    [(300, 520), (980, 300), (1460, 620), (620, 700), (120, 260), (1300, 380), (300, 520)],
]
BLOB_SIZE = [1250, 1000, 760, 520]
BLOB_OPACITY = [0.55, 0.55, 0.38, 0.16]
ANCHOR = 'window.__timelines["main"] = gsap.timeline({ paused: true });'


def parse_storyboard(path):
    text = open(path, encoding="utf-8").read()
    fmt = re.search(r"^format:\s*(\d+)x(\d+)", text, re.M)
    w, h = (int(fmt.group(1)), int(fmt.group(2))) if fmt else (1920, 1080)
    frames = []
    for block in re.split(r"^##\s+Frame\s+", text, flags=re.M)[1:]:
        num = int(re.match(r"(\d+)", block).group(1))
        src = re.search(r"^-\s*src:\s*(\S+)", block, re.M).group(1)
        dur = float(re.search(r"^-\s*duration:\s*([\d.]+)", block, re.M).group(1))
        frames.append(dict(num=num, src=src, id=os.path.splitext(os.path.basename(src))[0], dur=dur))
    return w, h, frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--palette", default="#050B16,#0A84FF,#1E5BFF,#6CC2FF,#CFE8FF")
    ap.add_argument("--no-voice", action="store_true")
    ap.add_argument("--music-volume", type=float)
    a = ap.parse_args()
    p = a.project
    W, H, frames = parse_storyboard(os.path.join(p, "STORYBOARD.md"))
    base, *blooms = a.palette.split(",")
    meta_path = os.path.join(p, "audio_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {"voices": [], "bgm": None}
    voice = {v["frame"]: v for v in meta.get("voices", [])}

    sx, sy = W / 1920, H / 1080
    t, body = 0.0, []
    for f in frames:
        body.append(f'''      <div
        id="el-{f["id"]}"
        class="scene"
        data-composition-id="{f["id"]}"
        data-composition-src="{f["src"]}"
        data-start="{round(t, 3)}"
        data-duration="{f["dur"]}"
        data-track-index="1"
      ></div>''')
        v = voice.get(f["num"])
        if v and not a.no_voice:
            body.append(f'''      <audio
        id="el-{f["id"]}-voice"
        src="{v["path"]}"
        data-start="{round(t, 3)}"
        data-duration="{f["dur"]}"
        data-track-index="10"
        data-volume="1"
      ></audio>''')
        t += f["dur"]
    total = round(t, 3)
    bgm = meta.get("bgm")
    if bgm:
        vol = a.music_volume if a.music_volume is not None else bgm.get("volume", 0.2)
        body.append(f'''      <audio
        id="el-bgm"
        src="{bgm["path"]}"
        data-start="0"
        data-duration="{total}"
        data-track-index="11"
        data-volume="{vol}"
      ></audio>''')

    blob_css = "".join(
        f"      #aurora #b{i + 1} {{ width: {int(BLOB_SIZE[i] * sx)}px; height: {int(BLOB_SIZE[i] * sx)}px; "
        f"background: {blooms[i % len(blooms)]}; opacity: {BLOB_OPACITY[i]}; }}\n"
        for i in range(4))
    seg = total / (len(BLOB_PATHS[0]) - 1)
    tweens = []
    for i, path in enumerate(BLOB_PATHS):
        for k in range(len(path) - 1):
            (x0, y0), (x1, y1) = path[k], path[k + 1]
            tweens.append(
                f'        tl.fromTo("#b{i + 1}", {{ x: {int(x0 * sx)}, y: {int(y0 * sy)} }}, '
                f'{{ x: {int(x1 * sx)}, y: {int(y1 * sy)}, duration: {seg:.3f}, ease: "sine.inOut", '
                f'immediateRender: {"true" if k == 0 else "false"} }}, {k * seg:.3f});')

    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: {base}; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      #root > .scene {{ z-index: 2; }}
      #aurora {{ position: absolute; inset: 0; overflow: hidden; background: {base}; z-index: 0; }}
      #aurora .blob {{ position: absolute; border-radius: 50%; filter: blur({int(150 * sx)}px); will-change: transform; }}
      #aurora .vignette {{ position: absolute; inset: 0;
        background: radial-gradient(ellipse at 50% 45%, transparent 35%, {base}8C 80%, {base}D9 100%); }}
{blob_css}    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total}"
      data-width="{W}"
      data-height="{H}"
    >
      <div id="aurora" class="clip" data-start="0" data-duration="{total}" data-track-index="0">
        <div class="blob" id="b1"></div>
        <div class="blob" id="b2"></div>
        <div class="blob" id="b3"></div>
        <div class="blob" id="b4"></div>
        <div class="vignette"></div>
      </div>
{chr(10).join(body)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      {ANCHOR}
      // ── aurora ──
      (function () {{ var tl = window.__timelines["main"];
{chr(10).join(tweens)}
        tl.to({{}}, {{ duration: {total} }}, 0);
      }})();
    </script>
  </body>
</html>
'''
    open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(html)
    print(f"index.html: {len(frames)} frames, {total}s, {W}x{H}, voice {'off' if a.no_voice or not voice else 'on'}, "
          f"music {'on' if bgm else 'off'}")


if __name__ == "__main__":
    main()
