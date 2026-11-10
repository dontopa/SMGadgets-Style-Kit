# Mixes cues.json (from build.py) into assets/sfx.wav using the rendered kit in audio/kit.
# Run with earshot's venv: D:\tools\earshot\.venv\Scripts\python.exe sfx.py
import json, pathlib
import numpy as np, soundfile as sf
from earshot.forge import kit

GAIN_DB = 2.0  # master trim on top of each role's level_db in audio/kit.json
SR = 48000

root = pathlib.Path(__file__).parent
lock = json.loads((root / "audio/kit/kit.lock.json").read_text())
data = json.loads((root / "cues.json").read_text())
out = np.zeros((int(data["end"] * SR) + 1, 2))
seen = {}
for name, at in data["cues"]:
    role = lock["roles"][name]
    n = seen[name] = seen.get(name, -1) + 1
    take = role["takes"][n % len(role["takes"])]
    a, sr = sf.read(root / "audio/kit" / take["file"], always_2d=True)
    assert sr == SR, take
    if a.shape[1] == 1:
        a = np.repeat(a, 2, 1)
    at0 = int(kit.place(take, role, at) * SR)
    a = a[max(0, -at0):][: len(out) - max(at0, 0)]
    at0 = max(at0, 0)
    out[at0:at0 + len(a)] += a * 10 ** (role["level_db"] / 20)

out *= 10 ** (GAIN_DB / 20)
peak = np.abs(out).max()
assert peak < 1, peak  # lower GAIN_DB if effects stack past full scale
sf.write(root / "assets/sfx.wav", out, SR, subtype="PCM_24")
print("cues", len(data["cues"]), "peak dBFS", round(20 * np.log10(peak), 1))
