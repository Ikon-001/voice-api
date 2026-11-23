import time
import wave
from pathlib import Path

files = sorted(Path(".").glob("*.wav")) + sorted(Path("samples").glob("*.wav"))
for p in files:
    with wave.open(str(p)) as w:
        secs = w.getnframes() / w.getframerate()
    stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime))
    print(f"{p.as_posix():48s} {stamp}  {secs:5.2f}s")
