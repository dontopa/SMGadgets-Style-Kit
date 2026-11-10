# Generates index.html, compositions/*.html and cues.json from the tables below. Edit here, re-run,
# then run sfx.py to rebuild the effects track.
import html, json, math, pathlib

END = 69.9          # speech end plus end card
OUTRO = 65.6        # end card fades in here
PLACE = "Taman Batu Caves"

CAPTIONS = [
    (0.05, 1.15, "Assalamualaikum abang akak"),
    (1.2, 4.55, "abang akak saya dah ready stock iPad terlalu banyak abang akak"),
    (4.6, 7.65, "abang akak cakap dengan saya, abang akak cari iPad model apa"),
    (7.7, 9.45, "saya ready stock yang mana"),
    (9.5, 11.75, "student ataupun kerja"),
    (11.8, 13.65, "untuk ofis ataupun nak bagi dekat anak"),
    (13.7, 16.45, "inilah abang akak, sesuai untuk kegunaan korang"),
    (16.5, 19.75, "saya ready stock iPad Air 2 64GB"),
    (19.8, 22.25, "iPad 5th Generation 32GB"),
    (22.3, 24.65, "iPad 7th Generation 32GB"),
    (24.7, 26.75, "iPad mini 64GB"),
    (26.8, 29.75, "iPad mini 5, 256GB"),
    (29.8, 32.05, "64GB pun saya ready stock abang akak"),
    (32.1, 34.25, "nak cari yang baru"),
    (34.3, 37.55, "satu tahun waranti, seal box lagi, saya ready stock iPad A16"),
    (37.6, 39.25, "yang ini satu tahun waranti"),
    (39.3, 43.15, "so iPad dekat sini memang sesuai untuk student nak masuk belajar"),
    (43.2, 46.55, "nak guna untuk harian pun boleh, ofis pun boleh"),
    (46.6, 48.95, "nak guna Microsoft pun tak ada masalah abang akak"),
    (49.0, 52.15, "nak tengok YouTube ke, nak tengok Netflix ke untuk anak, tak ada masalah"),
    (52.2, 55.25, "nak main game pun memang cukup-cukup padu abang akak"),
    (55.3, 58.95, "so kalau abang akak berminat, boleh terus contact saya Aidil daripada SM Gadgets"),
    (59.0, 60.75, "atau nak lagi senang abang akak"),
    (60.8, 63.65, f"walk in terus ke SM Gadgets HQ {PLACE}"),
    (63.7, 64.25, "okay abang akak"),
    (64.3, 65.5, "Assalamualaikum"),
]

# start, end, lines, sub, sub reveal time
TITLES = [
    (0.0, 4.55, ["iPAD READY STOCK"], "terlalu banyak", 2.6),
    (32.1, 39.25, ["iPAD A16"], "seal box · 1 tahun waranti", 34.3),
    (59.0, 60.75, ["WALK-IN TERUS"], "SM Gadgets HQ", 59.4),
]

# start, end, [(time, text)]
TICKS = [
    (16.5, 19.75, [(17.6, "iPad Air 2 64GB")]),
    (19.8, 22.25, [(19.9, "iPad 5th Gen 32GB")]),
    (22.3, 24.65, [(22.4, "iPad 7th Gen 32GB")]),
    (24.7, 32.05, [(25.0, "iPad mini 5 64GB · 256GB")]),
]

# start, end, name, line, price, count-from time, badge, shape
PRICES = []

# start, end, heading, [(time, emoji, label)]
ICONS = [
    (39.3, 52.15, "SESUAI UNTUK", [(41.8, "🎓", "Student"), (43.8, "💼", "Harian<br>& ofis"), (49.3, "📺", "YouTube<br>& Netflix")]),
]

MAP = (60.8, 65.5)

# (role, time) for sfx.py; roles are in audio/kit.json
CUES = []
def cue(role, at):
    CUES.append((role, round(at, 3)))


def t(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def clip(i, cid, a, b, inner, cls=""):
    return (f'<div id="{cid}" class="clip" data-start="{t(a)}" data-duration="{t(b - a)}" '
            f'data-track-index="{i}"><div class="in {cls}" id="{cid}-in">{inner}</div></div>')


js, body = [], []
def card_motion(cid, a, b):
    js.append(f'pop("#{cid}-in",{t(a)},{t(b)});')


for n, (a, b, lines, sub, st) in enumerate(TITLES):
    cid = f"title{n}"
    pills = "".join(f"<div><span class=pill>{html.escape(l)}</span></div>" for l in lines)
    body.append(clip(1, cid, a, b, f'{pills}<span class=sub id="{cid}-s">{html.escape(sub)}</span>', "title"))
    card_motion(cid, a + (0.1 if a else 0), b)
    js.append(f'item("#{cid}-s",{t(st)});')
    cue("whoosh.short", a + .25) if a else cue("pop", .05)
    cue("pop", st)

for n, (a, b, rows) in enumerate(TICKS):
    cid = f"ticks{n}"
    inner = "".join(f'<div class=tick id="{cid}-{k}"><i>✓</i>{html.escape(x)}</div>' for k, (_, x) in enumerate(rows))
    body.append(clip(2, cid, a, b, inner, "ticks"))
    js.append(f'fadeOut("#{cid}-in",{t(b)});')
    for k, (tt, _) in enumerate(rows):
        js.append(f'item("#{cid}-{k}",{t(tt)});')
        cue("pop", tt)

for n, (a, b, name, line, price, ct, badge, shape) in enumerate(PRICES):
    cid = f"price{n}"
    inner = (f'<div class="dev {shape}"><b></b></div><div class=info><h3>{name}</h3><p>{line}</p>'
             f'<h2 id="{cid}-n">RM0</h2></div><em>{badge}</em>')
    body.append(clip(3, cid, a, b, inner, "card price"))
    card_motion(cid, a, b)
    js.append(f'count("#{cid}-n",{price},{t(ct)});')
    cue("whoosh.short", a + .2)
    for k in range(8):  # ticks follow the power2.out count, equal value steps
        cue("tick.crisp", ct + .8 * (1 - math.sqrt(1 - k / 8)))
    cue("click.confirm", ct + .8)

for n, (a, b, head, items) in enumerate(ICONS):
    cid = f"icons{n}"
    inner = f"<h4>{head}</h4><hr><div class=row>" + "".join(
        f'<div class=ic id="{cid}-{k}"><span>{e}</span><small>{l}</small></div>' for k, (_, e, l) in enumerate(items)
    ) + "</div>"
    body.append(clip(3, cid, a, b, inner, "card icons"))
    card_motion(cid, a, b)
    cue("whoosh.short", a + .2)
    for k, (tt, _, _) in enumerate(items):
        js.append(f'item("#{cid}-{k}",{t(tt)});')
        cue("pop", tt)

a, b = MAP
body.append(clip(1, "map", a, b, f"<h5>Google Map/ Waze:</h5><p>📍 SM Gadgets HQ - {PLACE}</p>", "map"))
card_motion("map", a, b)
cue("whoosh.short", a + .2)

OVERLAY_CSS = """
#overlays{position:absolute;inset:0;font-family:Poppins,sans-serif}
#overlays .clip{position:absolute;inset:0}
.in{position:absolute;left:0;right:0}
.title{top:345px;text-align:center;line-height:1.28}
.pill{display:inline-block;background:#c93b26;color:#fff;font-weight:800;font-size:52px;padding:2px 24px;border-radius:14px;
 box-shadow:0 4px 14px rgba(0,0,0,.18);margin-bottom:6px}
.sub{display:inline-block;margin-top:12px;background:rgba(255,255,255,.86);color:#333;font-weight:600;font-style:italic;font-size:28px;
 padding:6px 22px;border-radius:24px}
.ticks{top:1470px;display:flex;flex-direction:column;align-items:center;gap:16px}
.tick{display:flex;align-items:center;gap:14px;background:rgba(240,238,235,.88);color:#222;font-weight:700;font-size:32px;
 padding:9px 28px 9px 12px;border-radius:40px;box-shadow:0 6px 20px rgba(0,0,0,.14);backdrop-filter:blur(14px)}
.tick i{width:44px;height:44px;border-radius:50%;background:#c93b26;color:#fff;font-style:normal;font-size:27px;display:grid;place-items:center}
.card{left:190px;right:190px;top:1108px;min-height:260px;background:rgba(240,238,235,.84);border-radius:30px;backdrop-filter:blur(20px);
 box-shadow:0 10px 34px rgba(0,0,0,.14);color:#222}
.price{left:165px;right:165px;display:flex;align-items:center;gap:34px;padding:28px 38px}
.dev{flex:none;width:150px;height:200px;background:#26282d;border-radius:22px;padding:11px;}
.dev.mini{width:128px}
.dev.lap{position:relative;width:196px;height:128px;border-radius:12px;padding:7px;margin-bottom:12px}
.dev.lap:after{content:"";position:absolute;left:-13px;right:-13px;bottom:-12px;height:12px;background:#a4a7ad;border-radius:0 0 10px 10px}
.dev b{display:block;height:100%;border-radius:12px;background:linear-gradient(160deg,#6f9be8,#7a66d0 70%,#8a6fcf)}
.info h3{font-size:44px;font-weight:700;line-height:1.1}
.info p{font-size:28px;font-weight:600;color:#666;margin-top:8px}
.info h2{font-size:82px;font-weight:800;color:#c93b26;line-height:1.15}
.price em{position:absolute;right:26px;top:-14px;background:#c93b26;color:#fff;font-style:normal;font-weight:700;font-size:29px;
 padding:5px 18px;border-radius:20px}
.icons{padding:26px 36px 30px;text-align:center}
.icons h4{font-size:32px;font-weight:800}
.icons hr{width:96px;height:6px;border:0;border-radius:3px;background:#c93b26;margin:10px auto 22px}
.row{display:flex;justify-content:center;gap:58px}
.ic{width:170px;text-align:center}
.ic span{font-size:88px;line-height:1.1;display:block}
.ic small{display:block;font-size:28px;font-weight:700;line-height:1.2;margin-top:8px}
.ball{display:block;width:100px;height:100px;margin:6px auto 0;border-radius:50%}
.rose{background:radial-gradient(circle at 34% 30%,#fff3ea,#eec6ad 45%,#c99477)}
.silver{background:radial-gradient(circle at 34% 30%,#fff,#e2e4e6 45%,#aeb2b6)}
.map{left:60px;right:60px;top:220px;background:#fff;padding:40px 56px;color:#333;box-shadow:0 10px 34px rgba(0,0,0,.14)}
.map h5{font-size:48px;font-weight:700;margin-bottom:26px}
.map p{font-size:37px;font-weight:500}
#veil{inset:0;bottom:0;background:rgba(18,18,20,.72);backdrop-filter:blur(26px);color:#fff;text-align:center}
.end{position:absolute;left:0;right:0;top:690px}
.end img{width:760px;display:block;margin:0 auto}
.end .a{font-size:62px;font-weight:700;margin-top:84px}
.end .b{display:inline-block;background:#c93b26;font-size:38px;font-weight:700;padding:10px 40px;border-radius:44px;margin-top:22px}
.end .c{font-size:32px;font-weight:600;margin-top:30px;color:#e6e6e6}
.star{position:absolute;color:#fff;line-height:1}
"""

STARS = [(180, 640, 54), (900, 620, 44), (120, 800, 34), (955, 790, 50), (760, 590, 30), (340, 590, 36), (560, 830, 28)]
stars = "".join(f'<span class=star id="s{i}" style="left:{x}px;top:{y}px;font-size:{s}px">✦</span>' for i, (x, y, s) in enumerate(STARS))
end = (f'<div id="veil" class="in">{stars}<div class=end><img src="assets/smg-logo-white.png" alt="SM Gadgets">'
       '<div class=a id="e1">iPad Ready Stock</div><div class=b id="e2">Walk-in SM Gadgets HQ</div>'
       '<div class=c id="e3">iPad Air 2 • iPad 5 • iPad 7 • iPad mini 5 • iPad A16</div></div></div>')
body.append(f'<div id="outro" class="clip" data-start="{t(OUTRO)}" data-duration="{t(END - OUTRO)}" data-track-index="4">{end}</div>')
for i in range(len(STARS)):
    js.append(f'tl.fromTo("#s{i}",{{opacity:0,scale:.3,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(2)"}},{t(OUTRO + .5 + i * .07)});')
for i, d in enumerate((.45, .6, .75)):
    js.append(f'tl.fromTo("#e{i + 1}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t(OUTRO + d)});')
cue("whoosh.long", OUTRO + .3)
cue("hit", OUTRO + .6)
js.append(f'tl.fromTo("#veil",{{opacity:0}},{{opacity:1,duration:.6,ease:"power1.out"}},{t(OUTRO)});')

OVERLAY_JS = """
const tl=gsap.timeline({paused:true});
const pop=(s,a,b)=>{tl.fromTo(s,{opacity:0,scale:.92,y:18},{opacity:1,scale:1,y:0,duration:.35,ease:"power2.out"},a);fadeOut(s,b)};
const fadeOut=(s,b)=>tl.to(s,{opacity:0,duration:.25,ease:"power2.in"},b-.27);
const item=(s,a)=>tl.fromTo(s,{opacity:0,scale:.7},{opacity:1,scale:1,duration:.32,ease:"back.out(1.8)"},a);
const fmt=n=>"RM"+Math.round(n).toLocaleString("en-US");
const count=(s,v,a)=>{const o={v:0},e=document.querySelector(s);tl.to(o,{v,duration:.8,ease:"power2.out",onUpdate(){e.textContent=fmt(o.v)}},a)};
"""
overlays = (f'<template><style>{OVERLAY_CSS}</style><div id="root" data-composition-id="overlays" data-width="1080" data-height="1920" '
            f'data-layout-allow-overlap>{"".join(body)}</div>'
            f'<script>{OVERLAY_JS}{"".join(js)}window.__timelines=window.__timelines||{{}};window.__timelines["overlays"]=tl;</script></template>')
overlays = overlays.replace('#overlays', '#root')

caps, cjs = [], []
for n, (a, b, text) in enumerate(CAPTIONS):
    caps.append(f'<div id="c{n}" class="clip cap" data-start="{t(a)}" data-duration="{t(b - a)}" data-track-index="5">{html.escape(text)}</div>')
captions = ('<template><style>#root{position:absolute;inset:0}'
            '.cap{position:absolute;left:190px;right:190px;bottom:280px;text-align:center;color:#fff;font:700 42px/1.22 Inter,sans-serif;text-wrap:balance;'
            'text-shadow:0 0 3px #000,0 0 3px #000,0 2px 7px rgba(0,0,0,.95),0 0 14px rgba(0,0,0,.65)}</style>'
            f'<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{"".join(caps)}</div>'
            '<script>window.__timelines=window.__timelines||{};window.__timelines["captions"]=gsap.timeline({paused:true});</script></template>')

index = f"""<!doctype html>
<html lang="ms"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1920px}}
#footage{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
#logo{{position:absolute;left:70px;top:92px;width:310px;filter:drop-shadow(0 0 2px #fff) drop-shadow(0 0 2px #fff) drop-shadow(0 0 7px #fff) drop-shadow(0 0 12px rgba(255,255,255,.85))}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
<video id="footage" class="clip" src="assets/footage.mp4" data-start="0" data-duration="{END}" data-track-index="0" data-has-audio="true"></video>
<img id="logo" class="clip" src="assets/smg-logo.png" alt="SM Gadgets" data-start="0" data-duration="{OUTRO + .7}" data-track-index="1">
<audio id="sfx" class="clip" src="assets/sfx.wav" data-start="0" data-duration="{END}" data-track-index="4"></audio>
<div id="overlays" data-composition-id="overlays" data-composition-src="compositions/overlays.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>
</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>
"""

root = pathlib.Path(__file__).parent
(root / "compositions").mkdir(exist_ok=True)
(root / "index.html").write_text(index, encoding="utf8")
(root / "compositions/overlays.html").write_text(overlays, encoding="utf8")
(root / "compositions/captions.html").write_text(captions, encoding="utf8")
(root / "cues.json").write_text(json.dumps({"end": END, "cues": sorted(CUES, key=lambda c: c[1])}), encoding="utf8")
print("ok", len(CAPTIONS), "captions", len(CUES), "cues")
