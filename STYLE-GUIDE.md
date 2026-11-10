# SM Gadgets — Video Edit Style Guide (for Claude)

Read all of this before editing. The user will give you a raw SM Gadgets video (vertical, a seller
talking about gadgets in Malay). Edit it in this exact house style. **No reference video needed** —
this guide + the `template/` folder is the reference.

## Folder contents

```
STYLE-GUIDE.md        ← this file
template/
  build.py            ← generates the whole edit from tables (captions, titles, cards, cues)
  sfx.py              ← mixes sound effects into assets/sfx.wav from cues.json
  package.json        ← hyperframes@0.9.16 render/preview scripts
  hyperframes.json
  assets/smg-logo.png, smg-logo-white.png
  audio/kit.json, audio/kit/*.wav   ← ready-rendered sound-effect kit
```

`build.py` currently holds a finished example (iPad ready stock). Replace its tables for each new video.

## Tools needed

- **HyperFrames** (HTML → MP4 renderer): `npx hyperframes@0.9.16 render`. Needs Node + Chrome.
- **ffmpeg / ffprobe**
- **faster-whisper** (Python) for the transcript, language `ms`.
- **earshot** (github.com/Leonxlnx/earshot) — only `sfx.py` imports it (`earshot.forge.kit`).
  Run `sfx.py` with earshot's Python venv. The kit wavs are already rendered, no models needed.
- Python with numpy + soundfile.

## Workflow per video

1. **New folder per video** — copy `template/` to `project-XXXX/`.
2. **Check the footage**
   - `ffprobe` → `color_transfer`. If iPhone HDR (`arib-std-b67`), tonemap to bt709 when making footage.mp4:
     `-vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"`
   - If there's a burned-in camera watermark at the bottom (DJI Osmo Pocket), crop it off:
     `crop=1030:1830:25:0,scale=1080:1920`
   - Output must be 1080×1920. Save as `assets/footage.mp4`.
3. **Transcribe** with faster-whisper (word timestamps). Fix known mishearings:
   - Brand is always **"SM Gadgets"** (exact spelling).
   - HQ is **Taman Batu Caves** (Whisper often hears "Batu Kew").
   - Seller name is usually **Aidil**.
4. **Fill the tables in `build.py`** from the transcript:
   - `CAPTIONS` — (start, end, text). Every spoken line, short chunks, original Malay wording.
   - `TITLES` — red pill title at top + white italic sub that pops in later. Use for the opening hook,
     new section/product, and the "WALK-IN TERUS / SM Gadgets HQ" line.
   - `TICKS` — grey pills with red ✓ (bottom area) when the seller lists models/specs.
   - `PRICES` — price card with device mockup, price counts up from RM0. `shape` = `""` (tablet),
     `"mini"`, or `"lap"` (laptop). Leave empty if no price said.
   - `ICONS` — "SESUAI UNTUK" card with 2–3 emoji + labels when seller lists use cases.
   - `MAP` — (start, end) during "walk in terus ke SM Gadgets HQ…". Shows Google Map/Waze card.
   - `END` = speech end + ~4 s, `OUTRO` = when end card fades in (right after the sign-off).
   - Edit the end card texts in the `end = ...` line (product name, model list).
5. `python build.py` → writes index.html, compositions/, cues.json.
6. `sfx.py` (earshot venv) → writes `assets/sfx.wav`. If it asserts on peak, lower `GAIN_DB`.
7. `npx hyperframes@0.9.16 check` then `npx hyperframes@0.9.16 render`.
8. **Final audio remix** (the renderer lowers the voice ~2 dB, so redo the audio):
   ```
   ffmpeg -i render.mp4 -i assets/footage.mp4 -i assets/sfx.wav -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0,alimiter=limit=0.79[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
   ```
   Mute anything spoken after the sign-off (Assalamualaikum) — e.g. `volume=0:enable='gt(t,OUTRO)'` on the footage audio.
9. Deliver only the full-quality render. **No smaller phone copy.** Name it like
   `SM_Gadgets_<Product>.mp4`.

## Look (do not change)

| Element | Style |
|---|---|
| Brand red | `#c93b26` |
| Font | Poppins (overlays), Inter 700 42px (captions) |
| Logo | top-left, white glow, whole video until end card |
| Captions | white, black shadow, bottom 280px, centered |
| Titles | red pill 52px bold at top (~345px) + white italic sub |
| Ticks | frosted grey pill, red round ✓, near bottom (~1470px) |
| Cards | frosted grey, radius 30, pop in (scale .92→1, 0.35 s) |
| Map card | white card at top, "Google Map/ Waze:" + 📍 SM Gadgets HQ - Taman Batu Caves |
| End card | dark blurred veil, white logo, stars ✦ pop, headline, red pill "Walk-in SM Gadgets HQ", model list |
| SFX | pop on each item, short whoosh on card enter, tick+ding on price count, long whoosh + hit on end card |

## Rules

- Keep the seller's wording in captions; just fix spelling.
- Don't redesign — same layout, colours, motions every video. Only content changes.
- If something in the video doesn't fit a table (e.g. no price), leave that table empty.
- Ask the user if a product name/price is unclear in the audio rather than guessing.
