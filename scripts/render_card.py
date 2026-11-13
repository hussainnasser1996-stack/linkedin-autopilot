#!/usr/bin/env python3
"""Render a LinkedIn card (2160x2160 PNG) in Hussain's house style from a JSON spec.

Usage: python3 scripts/render_card.py card.json out.png

Card types (field "type"):
  statement  - eyebrow + one big sentence                       (Post-01 style)
  bars       - eyebrow + title (+ gold highlight) + horizontal bars
               + optional 3-column stage strip + sources        (Post-23 style)
  compare    - eyebrow + title + two columns of short items      (Post-14 style)
See examples/ for one JSON per type.
Optional "lang": "ar" renders right-to-left in IBM Plex Sans Arabic (bundled in templates/fonts).
"""
import html, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "templates" / "fonts"
e = lambda s: html.escape(str(s))

BASE_CSS = """
@font-face{font-family:Inter;font-weight:400;src:url('FONTS/Inter-Regular.ttf')}
@font-face{font-family:Inter;font-weight:500;src:url('FONTS/Inter-Medium.ttf')}
@font-face{font-family:Inter;font-weight:600;src:url('FONTS/Inter-SemiBold.ttf')}
@font-face{font-family:Inter;font-weight:700;src:url('FONTS/Inter-Bold.ttf')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:2160px;height:2160px;background:#F8F7F4;font-family:Inter,sans-serif;color:#0F172A;overflow:hidden}
.w{position:absolute;inset:0;padding:192px 192px 0}
.rule{width:96px;height:6px;background:#B8960F}
.eye{margin-top:44px;font-size:44px;letter-spacing:.22em;color:#B8960F;font-weight:500;text-transform:uppercase}
h1{margin-top:40px;font-size:112px;line-height:1.08;font-weight:700;letter-spacing:-.02em}
h1 span{color:#B8960F}
.big{position:absolute;left:192px;right:192px;top:50%;transform:translateY(-50%);font-size:128px;line-height:1.1;font-weight:600;letter-spacing:-.015em}
.big span{color:#B8960F}
.chart{margin-top:110px}
.row{display:grid;grid-template-columns:440px 1fr;align-items:center;height:118px}
.name{font-size:46px;font-weight:500}
.barw{display:flex;align-items:center;gap:30px}
.bar{height:62px;background:#0F172A;border-radius:4px}
.bar.hl{background:#B8960F}
.val{font-size:46px;font-weight:600}
.tag{margin-top:22px;font-size:30px;letter-spacing:.14em;color:#64748B;font-weight:600;text-transform:uppercase}
.stages{margin-top:110px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:48px}
.st{border-top:6px solid #0F172A;padding-top:34px}
.st.gap{border-top:6px dashed #B8960F}
.st h3{font-size:34px;letter-spacing:.16em;font-weight:700;text-transform:uppercase}
.st p{margin-top:18px;font-size:44px;line-height:1.25}
.st.gap h3,.st.gap p{color:#B8960F}
.cols{position:absolute;left:192px;right:192px;top:880px;display:grid;grid-template-columns:1fr 1fr;gap:96px}
.col{border-top:4px solid #B8960F;padding-top:56px}
.col h3{font-size:44px;letter-spacing:.14em;font-weight:700;text-transform:uppercase}
.col li{list-style:none;margin-top:58px;font-size:48px}
.foot{position:absolute;left:192px;right:192px;bottom:170px;display:flex;justify-content:space-between;align-items:flex-end}
.sig .l{width:80px;height:2px;background:#0F172A}
.sig div+div{margin-top:30px;font-size:44px}
.src{font-size:28px;color:#64748B;text-align:right;line-height:1.5;max-width:900px}
"""

AR_CSS = """
@font-face{font-family:PlexAr;font-weight:400;src:url('FONTS/IBMPlexSansArabic-Regular.ttf')}
@font-face{font-family:PlexAr;font-weight:500;src:url('FONTS/IBMPlexSansArabic-Medium.ttf')}
@font-face{font-family:PlexAr;font-weight:600;src:url('FONTS/IBMPlexSansArabic-SemiBold.ttf')}
@font-face{font-family:PlexAr;font-weight:700;src:url('FONTS/IBMPlexSansArabic-Bold.ttf')}
html,body{direction:rtl;font-family:PlexAr,Inter,sans-serif}
.eye,.tag,.st h3,.col h3{letter-spacing:0}
h1,.big{letter-spacing:0;line-height:1.3}
.src{text-align:left}
.val,.bar{direction:ltr}
.row{grid-template-columns:600px 1fr}
"""


def title_html(c):
    t = e(c["title"])
    if c.get("highlight"):
        t += "<br><span>" + e(c["highlight"]) + "</span>"
    return f"<h1>{t}</h1>"


def body_statement(c):
    text = e(c["text"])
    for h in c.get("highlight_words", []):
        text = text.replace(e(h), f"<span>{e(h)}</span>", 1)
    return f'<div class="w"><div class="rule"></div><div class="eye">{e(c["eyebrow"])}</div></div><div class="big">{text}</div>'


def body_bars(c):
    bars = c["bars"]
    mx = max(float(b["value"]) for b in bars) or 1
    rows = "".join(
        f'<div class="row"><div class="name">{e(b["label"])}</div><div class="barw">'
        f'<div class="bar{" hl" if b.get("highlight") else ""}" style="width:{int((1000 if c.get('lang')=='ar' else 1100)*float(b["value"])/mx)}px"></div>'
        f'<div class="val">{e(b["display"])}</div></div></div>'
        for b in bars)
    tag = f'<div class="tag">{e(c["bars_caption"])}</div>' if c.get("bars_caption") else ""
    stages = ""
    if c.get("stages"):
        stages = '<div class="stages">' + "".join(
            f'<div class="st{" gap" if s.get("gap") else ""}"><h3>{e(s["h"])}</h3><p>{e(s["p"])}</p></div>'
            for s in c["stages"][:3]) + "</div>"
    return (f'<div class="w"><div class="rule"></div><div class="eye">{e(c["eyebrow"])}</div>'
            f'{title_html(c)}<div class="chart">{rows}{tag}</div>{stages}</div>')


def body_compare(c):
    cols = "".join(
        f'<div class="col"><h3>{e(col["h"])}</h3><ul>' + "".join(f"<li>{e(i)}</li>" for i in col["items"][:5]) + "</ul></div>"
        for col in c["columns"][:2])
    return (f'<div class="w"><div class="rule"></div><div class="eye">{e(c["eyebrow"])}</div>'
            f'{title_html(c)}</div><div class="cols">{cols}</div>')


BODIES = {"statement": body_statement, "bars": body_bars, "compare": body_compare}


def build_html(c):
    lab = "المصادر" if c.get("lang") == "ar" else "Sources"
    src = f'<div class="src">{lab}: {e(c["sources"])}</div>' if c.get("sources") else "<div></div>"
    css = (BASE_CSS + (AR_CSS if c.get("lang") == "ar" else "")).replace("FONTS", FONTS.as_uri())
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'{BODIES[c["type"]](c)}'
            f'<div class="foot"><div class="sig"><div class="l"></div><div>Hussain Nasser</div></div>{src}</div>'
            f'</body></html>')


def chrome():
    for p in [os.environ.get("CHROME_PATH"), "/usr/bin/google-chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome"), shutil.which("chromium")]:
        if p and Path(p).exists():
            return p
    sys.exit("Chrome not found")


def render(spec_path, out_path):
    c = json.loads(Path(spec_path).read_text())
    if c["type"] not in BODIES:
        sys.exit(f"unknown card type {c['type']}")
    tmp = Path(tempfile.mkdtemp())
    page = tmp / "card.html"
    page.write_text(build_html(c))
    out = Path(out_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--virtual-time-budget=3000",
                    "--window-size=2160,2160", f"--screenshot={out}", page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not out.exists() or out.stat().st_size < 20000:
        sys.exit("render failed or blank image")
    print(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(sys.argv[1], sys.argv[2])
