"""Write one worker packet per storyboard frame.

    python make_packets.py <project>

Each .kinetic/packets/<frame-id>.md = the frame's storyboard block, the real
length of every asset it names (ffprobe), and pointers to the style file,
fonts and sound kit. Workers read their packet + .kinetic/style-direction.md.
"""

import os
import re
import subprocess
import sys


def length(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout.strip()
        return float(out) if out and out != "N/A" else None
    except Exception:
        return None


def main(p):
    text = open(os.path.join(p, "STORYBOARD.md"), encoding="utf-8").read()
    fmt = re.search(r"^format:\s*(\S+)", text, re.M)
    out = os.path.join(p, ".kinetic", "packets")
    os.makedirs(out, exist_ok=True)
    fonts = sorted(os.listdir(os.path.join(p, "assets", "fonts"))) if os.path.isdir(os.path.join(p, "assets", "fonts")) else []
    sfx_dir = os.path.join(p, "assets", "sfx")
    sfx = [f"{f[:-4]} {length(os.path.join(sfx_dir, f)):.2f}s" for f in sorted(os.listdir(sfx_dir))
           if f.endswith(".mp3")] if os.path.isdir(sfx_dir) else []
    kin = os.path.join(p, ".kinetic")
    light = os.path.exists(os.path.join(kin, "light-ground.md"))
    beats_path = os.path.join(kin, "beats.md")
    beats = open(beats_path, encoding="utf-8").read() if os.path.exists(beats_path) else ""
    hit_maps = {int(m.group(1)): m.group(0).strip()
                for m in re.finditer(r"^##\s+Frame\s+(\d+)\b[\s\S]*?(?=^##\s|\Z)", beats, re.M)}
    if light:
        style = ".kinetic/light-ground.md + .kinetic/type-motion.md (read both in full; launch-film mode)"
        sound = (f"no <audio> tags: write your cues to .kinetic/sfx/<frame-id>.json "
                 f"(see the launch-film section of the worker brief)")
    else:
        style = ".kinetic/style-direction.md (read it in full)"
        sound = f"Sound kit in assets/sfx/: {', '.join(sfx) or 'none'}"
    for block in re.split(r"^(?=##\s+Frame\s+)", text, flags=re.M)[1:]:
        fid = os.path.splitext(os.path.basename(re.search(r"^-\s*src:\s*(\S+)", block, re.M).group(1)))[0]
        num = int(re.match(r"##\s+Frame\s+(\d+)", block).group(1))
        names = sorted(set(re.findall(r"assets/([\w./-]+\.(?:mp4|mov|webm|png|jpg|jpeg|webp|svg))", block)))
        assets = []
        for n in names:
            fp = os.path.join(p, "assets", n)
            if not os.path.exists(fp):
                assets.append(f"- assets/{n} — MISSING (stage it before dispatch)")
            else:
                ln = length(fp) if n.split(".")[-1] in ("mp4", "mov", "webm") else None
                assets.append(f"- assets/{n}" + (f" — {ln:.2f} s long" if ln else ""))
        packet = f"""# Packet: {fid}

- Project: {os.path.abspath(p)}
- Canvas: {fmt.group(1) if fmt else '1920x1080'}
- Style truth: {style}
- Fonts in assets/fonts/: {', '.join(fonts) or 'none — use the style file'}
- Sound: {sound}

## Assets named by this frame
{chr(10).join(assets) or '- none (type, icons and drawn elements only)'}

## Storyboard block
{block.strip()}
"""
        if num in hit_maps:
            packet += f"\n## Hit map (measured from the music; BEAT LOCK events snap to its A/B hits)\n{hit_maps[num]}\n"
        open(os.path.join(out, fid + ".md"), "w", encoding="utf-8").write(packet)
        missing = sum("MISSING" in a for a in assets)
        print(f"{fid}: {len(assets)} assets" + (f", {missing} MISSING" if missing else ""))


if __name__ == "__main__":
    main(sys.argv[1])
