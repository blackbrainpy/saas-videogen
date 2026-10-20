"""Check and install everything this skill needs. Run it first on any new machine or agent.

    python setup.py              # check, then install whatever is missing
    python setup.py --check      # only report
    python setup.py --voice      # also faster-whisper (voice-over mode: align_voice.py)
    python setup.py --refs       # also yt-dlp (downloading reference videos the user links)

Required (the launch-film method):
  - Node.js >= 20 + npx           HyperFrames CLI (npx hyperframes ...), GSAP comes from a CDN in the page
  - HyperFrames CLI               npx --yes hyperframes (pinned per project in package.json by `hyperframes init`)
  - Chrome for rendering          npx hyperframes browser ensure (downloads chrome-headless-shell into ~/.cache)
  - HyperFrames agent skills      npx hyperframes skills (hyperframes, hyperframes-core, -animation, -cli, ...),
                                  plus `npx hyperframes skills update product-launch-video` (kinetic VO mode's transitions.mjs)
  - FFmpeg + FFprobe              renders, cuts, loudness, sound mix (8.x tested; drawtext is NOT used)
  - Python 3.10+ with numpy, Pillow
Optional: faster-whisper (--voice), yt-dlp (--refs).
Web tools (in the user's own browser, free plans, never installed): ElevenLabs Sound Effects / voices,
Gemini "Create music". OBS Studio only if new screen recordings must be made.
Installs use the platform package manager: winget (Windows), Homebrew (macOS), apt/dnf (Linux), and
`pip install --user` for Python packages. Nothing is installed with --check.
"""
import argparse
import importlib.util
import os
import platform
import shutil
import subprocess
import sys

SYSTEM = platform.system()
PKG = {
    "node": {"Windows": ["winget", "install", "-e", "--id", "OpenJS.NodeJS.LTS", "--accept-source-agreements",
                         "--accept-package-agreements"],
             "Darwin": ["brew", "install", "node"], "apt": ["sudo", "apt-get", "install", "-y", "nodejs", "npm"],
             "dnf": ["sudo", "dnf", "install", "-y", "nodejs", "npm"]},
    "ffmpeg": {"Windows": ["winget", "install", "-e", "--id", "Gyan.FFmpeg", "--accept-source-agreements",
                           "--accept-package-agreements"],
               "Darwin": ["brew", "install", "ffmpeg"], "apt": ["sudo", "apt-get", "install", "-y", "ffmpeg"],
               "dnf": ["sudo", "dnf", "install", "-y", "ffmpeg"]},
}
PY = {"numpy": "numpy", "PIL": "Pillow"}
PY_OPT = {"voice": {"faster_whisper": "faster-whisper"}, "refs": {"yt_dlp": "yt-dlp"}}

results = []


def run(cmd, timeout=900):
    exe = shutil.which(cmd[0]) or cmd[0]
    try:
        p = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def report(name, ok, detail=""):
    results.append((name, ok))
    print(f"  {'OK ' if ok else 'MISSING'}  {name:28s} {detail}")


def system_install(tool):
    key = SYSTEM if SYSTEM in ("Windows", "Darwin") else ("apt" if shutil.which("apt-get") else "dnf")
    cmd = PKG[tool].get(key)
    if not cmd or not shutil.which(cmd[0]):
        print(f"    cannot install {tool} automatically here: install it by hand ({' '.join(cmd or ['?'])})")
        return False
    print(f"    installing {tool}: {' '.join(cmd)}")
    code, out = run(cmd, timeout=1800)
    if code != 0:
        print("    " + out[-400:])
    if SYSTEM == "Windows":
        print("    note: open a NEW terminal (or restart the agent) so PATH picks up the new tool")
    return code == 0


def check_tool(name, cmd, version_ok, install_key, check_only):
    found = shutil.which(cmd[0])
    if found:
        code, out = run(cmd, timeout=60)
        line = out.splitlines()[0] if out else ""
        if code == 0 and version_ok(line):
            return report(name, True, line[:60])
        report(name, False, f"found but unusable: {line[:60]}")
    else:
        report(name, False, "not on PATH")
    if not check_only and install_key:
        system_install(install_key)


def node_ok(line):
    try:
        return int(line.lstrip("v").split(".")[0]) >= 20
    except ValueError:
        return False


def pip_install(pkgs, check_only):
    for mod, pkg in pkgs.items():
        if importlib.util.find_spec(mod):
            report(f"python: {pkg}", True)
            continue
        report(f"python: {pkg}", False)
        if not check_only:
            print(f"    pip install --user {pkg}")
            code, out = run([sys.executable, "-m", "pip", "install", "--user", pkg])
            if code != 0:
                print("    " + out[-400:])


def hyperframes(check_only):
    if not shutil.which("npx"):
        report("hyperframes CLI", False, "needs Node.js/npx first")
        return
    code, out = run(["npx", "--yes", "hyperframes", "--version"], timeout=600)
    report("hyperframes CLI", code == 0, out.splitlines()[-1] if out else "")
    if code != 0:
        return
    code, out = run(["npx", "--yes", "hyperframes", "browser", "path"], timeout=120)
    has_chrome = code == 0 and os.path.exists(out.splitlines()[-1].strip()) if out else False
    report("Chrome for rendering", has_chrome)
    if not has_chrome and not check_only:
        print("    npx hyperframes browser ensure")
        run(["npx", "--yes", "hyperframes", "browser", "ensure"], timeout=1800)
    skills_dir = os.path.join(os.path.expanduser("~"), ".claude", "skills")
    have = all(os.path.isdir(os.path.join(skills_dir, s)) for s in ("hyperframes", "hyperframes-core"))
    report("HyperFrames agent skills", have, skills_dir if have else "")
    if not have and not check_only:
        print("    npx hyperframes skills")
        run(["npx", "--yes", "hyperframes", "skills"], timeout=900)
    plv = os.path.isdir(os.path.join(skills_dir, "product-launch-video"))
    report("product-launch-video skill", plv, "(kinetic VO mode only)")
    if not plv and not check_only:
        run(["npx", "--yes", "hyperframes", "skills", "update", "product-launch-video"], timeout=900)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="only report, install nothing")
    ap.add_argument("--voice", action="store_true")
    ap.add_argument("--refs", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"saas-videogen setup on {SYSTEM} ({platform.machine()}), Python {platform.python_version()}")
    if sys.version_info < (3, 10):
        report("Python 3.10+", False, "upgrade Python first")
    else:
        report("Python 3.10+", True, platform.python_version())
    check_tool("Node.js >= 20", ["node", "--version"], node_ok, "node", a.check)
    check_tool("FFmpeg", ["ffmpeg", "-version"], lambda l: "ffmpeg version" in l, "ffmpeg", a.check)
    check_tool("FFprobe", ["ffprobe", "-version"], lambda l: "ffprobe version" in l, None, a.check)
    pip_install(PY, a.check)
    for flag, pkgs in PY_OPT.items():
        if getattr(a, flag):
            pip_install(pkgs, a.check)
    hyperframes(a.check)
    if shutil.which("npx"):
        print("\nnpx hyperframes doctor (Docker, whisper-cpp, Kokoro and MusicGen are NOT needed for this skill):")
        code, out = run(["npx", "--yes", "hyperframes", "doctor"], timeout=300)
        print("\n".join("    " + l for l in out.splitlines() if l.strip().startswith(("✓", "✗"))))
    missing = [n for n, ok in results if not ok]
    print("\nready" if not missing else f"\nstill missing: {', '.join(missing)}"
          + ("" if a.check else "  (re-run this script in a new terminal after installs)"))
    sys.exit(0 if not missing else 1)


if __name__ == "__main__":
    main()
