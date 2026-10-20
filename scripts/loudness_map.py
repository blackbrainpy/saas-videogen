"""Print a track's loudness per second (dBFS RMS), to pick the section where the
drop or lift lands on a key frame and any built-in silence lands on a pause.

    python loudness_map.py track.mp3 [step_seconds]
"""

import subprocess
import sys

import numpy as np


def main(path: str, step: float = 1.0) -> None:
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "8000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32)
    n = int(8000 * step)
    print(f"{path}: {len(a) / 8000:.1f} s")
    rows = []
    for i in range(0, len(a), n):
        seg = a[i:i + n]
        db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        rows.append(f"{i / 8000:6.1f}s {db:6.1f} " + "#" * max(0, int((db + 60) / 2)))
    print("\n".join(rows))


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1.0)
