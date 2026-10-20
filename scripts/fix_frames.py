"""Mechanical fixes on frame files before lint/check:
- every <video>/<audio> gets an id (id-less videos freeze in renders);
- frames that use a font from assets/fonts without @font-face get one;
- generated extrusion layers (class names ending in "-dl") are flagged
  data-layout-allow-overlap so `hyperframes check` accepts deliberate overlap.

    python fix_frames.py <project> [--font "Geist=geist-latin.woff2" ...]
"""

import glob
import os
import re
import sys


def font_faces(project, extra):
    faces = dict(extra)
    if not faces:
        for f in sorted(glob.glob(os.path.join(project, "assets", "fonts", "*.woff2"))):
            base = os.path.basename(f)
            fam = re.sub(r"[-_](latin|regular|variable|vf).*$", "", base[:-6], flags=re.I).replace("-", " ").title()
            faces.setdefault(fam, base)
    return faces


def fix(path, faces):
    html = open(path, encoding="utf-8").read()
    stem = re.sub(r"[^a-z0-9]", "", os.path.basename(path).split("-", 1)[0]) or "x"
    changes, n = [], [0]

    def add_id(m):
        tag = m.group(0)
        if re.search(r"\sid\s*=", tag):
            return tag
        n[0] += 1
        changes.append("media id")
        return tag.replace("<" + m.group(1), f'<{m.group(1)} id="f{stem}-m{n[0]}"', 1)

    html = re.sub(r"<(video|audio)\b[^>]*>", add_id, html)
    missing = [fam for fam in faces if fam.lower() in html.lower() and "@font-face" not in html]
    if missing:
        css = "<style>\n" + "".join(
            f'@font-face {{ font-family: "{fam}"; src: url("assets/fonts/{faces[fam]}") format("woff2"); '
            f"font-weight: 100 900; font-display: block; }}\n" for fam in faces) + "</style>\n"
        m = re.search(r"<template\b[^>]*>", html)
        html = html[:m.end()] + "\n" + css + html[m.end():] if m else css + html
        changes.append("font-face")
    new = re.sub(r'(el\.className\s*=\s*"[\w-]*-dl\b[^;]*;)(?![^\n]*data-layout-allow-overlap)',
                 r'\1 el.setAttribute("data-layout-allow-overlap", "");', html)
    if new != html:
        html = new
        changes.append("overlap flag")
    if changes:
        open(path, "w", encoding="utf-8").write(html)
    return changes


def main(argv):
    project = argv[0]
    extra = [a.split("=", 1) for a in argv[1:] if "=" in a]
    faces = font_faces(project, extra)
    for path in sorted(glob.glob(os.path.join(project, "compositions", "**", "*.html"), recursive=True)):
        ch = fix(path, faces)
        if ch:
            print(os.path.relpath(path, project), ", ".join(sorted(set(ch))))


if __name__ == "__main__":
    main(sys.argv[1:])
