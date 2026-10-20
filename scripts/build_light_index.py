"""Build index.html for a launch film on the approved light ground (references/light-ground.md).

    python build_light_index.py <project> [--music assets/music/score.mp3 --music-volume 0.7]
                                [--sfx assets/sfx-mix.wav --sfx-volume 0.85]
                                [--ground "#F2F2F0"] [--glow-a "150,140,255"] [--glow-b "90,200,255"]
                                [--grain assets/wallpaper/grain.png]

Reads STORYBOARD.md: frontmatter "format: WxH", then "## Frame N - ..." blocks with "- src:" and
"- duration:" (and optionally "- start:"; otherwise frames run back to back). Writes index.html with
the off-white ground + two drifting bottom glows on track 0, one scene host per frame (track 1), the
music (track 11) and the single sound-effects mix from sound_design.py (track 12). Frames stay
transparent; the hand-over object morphs between them, so no transitions are injected.
"""
import argparse
import os
import re


def parse_storyboard(path):
    text = open(path, encoding="utf-8").read()
    fmt = re.search(r"^format:\s*(\d+)x(\d+)", text, re.M)
    w, h = (int(fmt.group(1)), int(fmt.group(2))) if fmt else (1920, 1080)
    frames, t = [], 0.0
    for block in re.split(r"^##\s+Frame\s+", text, flags=re.M)[1:]:
        src = re.search(r"^-\s*src:\s*(\S+)", block, re.M).group(1)
        dur = float(re.search(r"^-\s*duration:\s*([\d.]+)", block, re.M).group(1))
        st = re.search(r"^-\s*start:\s*([\d.]+)", block, re.M)
        start = float(st.group(1)) if st else t
        frames.append(dict(src=src, id=os.path.splitext(os.path.basename(src))[0], start=round(start, 3), dur=dur))
        t = start + dur
    return w, h, frames, round(t, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--music")
    ap.add_argument("--music-volume", type=float, default=0.7)
    ap.add_argument("--sfx")
    ap.add_argument("--sfx-volume", type=float, default=0.85)
    ap.add_argument("--ground", default="#F2F2F0")
    ap.add_argument("--glow-a", default="150,140,255", help="r,g,b of the main bottom glow (tint toward the brand)")
    ap.add_argument("--glow-b", default="90,200,255")
    ap.add_argument("--grain")
    a = ap.parse_args()
    W, H, frames, total = parse_storyboard(os.path.join(a.project, "STORYBOARD.md"))
    sx, sy = W / 1920, H / 1080
    g = a.ground
    scenes = "\n".join(
        f'      <div id="el-{f["id"]}" class="scene" data-composition-id="{f["id"]}" '
        f'data-composition-src="{f["src"]}" data-start="{f["start"]}" data-duration="{f["dur"]}" '
        f'data-track-index="1"></div>' for f in frames)
    audio = []
    if a.music:
        audio.append(f'      <audio id="el-score" src="{a.music}" data-timeline-role="music" data-start="0" '
                     f'data-duration="{total}" data-track-index="11" data-volume="{a.music_volume}"></audio>')
    if a.sfx:
        audio.append(f'      <audio id="el-sfx" src="{a.sfx}" data-start="0" data-duration="{total}" '
                     f'data-track-index="12" data-volume="{a.sfx_volume}"></audio>')
    grain_css = (f'      #light-grain {{ position: absolute; inset: 0; background: url("{a.grain}") 0 0 / {W}px {H}px; '
                 f'opacity: .18; mix-blend-mode: multiply; }}\n') if a.grain else ""
    grain_div = '<div id="light-grain"></div>' if a.grain else ""
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {g}; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: {g}; }}
      #ground {{ position: absolute; inset: 0; z-index: 0; overflow: hidden; background: {g}; }}
      #glow-a {{ position: absolute; width: {int(1500 * sx)}px; height: {int(760 * sx)}px; left: {int(210 * sx)}px;
        top: {int(760 * sy)}px; border-radius: 50%; filter: blur({int(60 * sx)}px);
        background: radial-gradient(closest-side, rgba({a.glow_a},.55), rgba({a.glow_a},.28) 55%, rgba(242,242,240,0) 100%); }}
      #glow-b {{ position: absolute; width: {int(900 * sx)}px; height: {int(600 * sx)}px; left: {int(1250 * sx)}px;
        top: {int(820 * sy)}px; border-radius: 50%; filter: blur({int(70 * sx)}px);
        background: radial-gradient(closest-side, rgba({a.glow_b},.38), rgba(242,242,240,0) 100%); }}
{grain_css}      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; z-index: 2; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
      <div id="ground" class="clip" data-start="0" data-duration="{total}" data-track-index="0">
        <div id="glow-a"></div><div id="glow-b"></div>{grain_div}
      </div>
{scenes}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      // one slow drift for the whole film, so nothing moves at the seams
      tl.fromTo("#glow-a", {{ x: 0, y: 0, scale: 1 }}, {{ x: {int(140 * sx)}, y: {int(-40 * sy)}, scale: 1.12, duration: {total}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#glow-b", {{ x: 0, y: 0 }}, {{ x: {int(-220 * sx)}, y: {int(-30 * sy)}, duration: {total}, ease: "sine.inOut" }}, 0);
      tl.to({{}}, {{ duration: {total} }}, 0);
    </script>
  </body>
</html>
'''
    open(os.path.join(a.project, "index.html"), "w", encoding="utf-8").write(html)
    print(f"index.html: {len(frames)} frames, {total}s, {W}x{H}, music {'on' if a.music else 'off'}, "
          f"sfx {'on' if a.sfx else 'off'}")


if __name__ == "__main__":
    main()
