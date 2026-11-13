#!/usr/bin/env python3
"""Render a LinkedIn carousel (PDF document post, 1080x1350 pages) in Hussain's house style.

Usage: python3 scripts/render_carousel.py carousel.json out_dir/
Writes out_dir/carousel.pdf and out_dir/cover.png (thumbnail = page 1).

carousel.json:
{
  "lang": "en" | "ar",             # optional, ar = right-to-left Arabic
  "title": "Document title shown by LinkedIn (max ~60 chars)",
  "sources": "Short source list for the last page",
  "slides": [                       # 6-9 slides
    {"type": "cover",  "eyebrow": "...", "title": "...", "highlight": "...", "sub": "..."},
    {"type": "stat",   "eyebrow": "...", "number": "$1.0B", "label": "...", "note": "..."},
    {"type": "bars",   "eyebrow": "...", "title": "...", "bars": [{"label": "...", "value": 56, "display": "56%", "highlight": true}]},
    {"type": "points", "eyebrow": "...", "title": "...", "points": ["...", "..."]},     # max 4 points
    {"type": "end",    "eyebrow": "...", "text": "...", "question": "..."}
  ]
}
"""
import html, json, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_card import chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "templates" / "fonts"
e = lambda s: html.escape(str(s))

CSS = """
@font-face{font-family:Inter;font-weight:400;src:url('FONTS/Inter-Regular.ttf')}
@font-face{font-family:Inter;font-weight:500;src:url('FONTS/Inter-Medium.ttf')}
@font-face{font-family:Inter;font-weight:600;src:url('FONTS/Inter-SemiBold.ttf')}
@font-face{font-family:Inter;font-weight:700;src:url('FONTS/Inter-Bold.ttf')}
@page{size:1080px 1350px;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#F8F7F4;font-family:Inter,sans-serif;color:#0F172A;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;page-break-after:always;padding:110px 96px 0}
.s.dark{background:#0F172A;color:#F8F7F4}
.rule{width:64px;height:5px;background:#B8960F}
.eye{margin-top:30px;font-size:26px;letter-spacing:.2em;color:#B8960F;font-weight:600;text-transform:uppercase}
h1{margin-top:34px;font-size:84px;line-height:1.08;font-weight:700;letter-spacing:-.02em}
h1 span{color:#B8960F}
h2{margin-top:30px;font-size:58px;line-height:1.12;font-weight:700;letter-spacing:-.015em}
.sub{margin-top:44px;font-size:34px;line-height:1.4;color:#475569}
.dark .sub{color:#CBD5E1}
.num{margin-top:150px;font-size:210px;line-height:1;font-weight:700;color:#B8960F;letter-spacing:-.03em}
.lab{margin-top:40px;font-size:50px;line-height:1.2;font-weight:600}
.note{margin-top:40px;font-size:32px;line-height:1.45;color:#475569}
.chart{margin-top:80px}
.row{margin-top:46px}
.name{font-size:32px;font-weight:500}
.barw{margin-top:14px;display:flex;align-items:center;gap:22px}
.bar{height:46px;background:#0F172A;border-radius:3px}
.bar.hl{background:#B8960F}
.val{font-size:34px;font-weight:700}
ol{margin-top:70px;list-style:none;counter-reset:p}
ol li{counter-increment:p;position:relative;padding-left:96px;margin-top:52px;font-size:38px;line-height:1.35}
ol li:before{content:counter(p,decimal-leading-zero);position:absolute;left:0;top:0;font-weight:700;color:#B8960F;font-size:38px}
.big{margin-top:120px;font-size:68px;line-height:1.15;font-weight:600;letter-spacing:-.01em}
.q{margin-top:70px;font-size:40px;line-height:1.35;color:#B8960F;font-weight:600}
.swipe{position:absolute;right:96px;bottom:180px;font-size:30px;font-weight:600;color:#B8960F;letter-spacing:.08em}
.foot{position:absolute;left:96px;right:96px;bottom:84px;display:flex;justify-content:space-between;align-items:flex-end;font-size:26px}
.foot .who{display:flex;align-items:center;gap:20px;font-weight:600}
.foot .who i{display:block;width:48px;height:2px;background:currentColor}
.foot .pg{color:#94A3B8;font-weight:500}
.src{position:absolute;left:96px;right:96px;bottom:150px;font-size:22px;line-height:1.5;color:#94A3B8}
"""

AR_CSS = """
@font-face{font-family:PlexAr;font-weight:400;src:url('FONTS/IBMPlexSansArabic-Regular.ttf')}
@font-face{font-family:PlexAr;font-weight:500;src:url('FONTS/IBMPlexSansArabic-Medium.ttf')}
@font-face{font-family:PlexAr;font-weight:600;src:url('FONTS/IBMPlexSansArabic-SemiBold.ttf')}
@font-face{font-family:PlexAr;font-weight:700;src:url('FONTS/IBMPlexSansArabic-Bold.ttf')}
html,body{direction:rtl;font-family:PlexAr,Inter,sans-serif}
.eye,.swipe{letter-spacing:0}
h1,h2,.big,.lab{letter-spacing:0;line-height:1.35}
ol li{padding-left:0;padding-right:96px}
ol li:before{left:auto;right:0}
.swipe{right:auto;left:96px}
.num,.val,.bar,.foot .pg{direction:ltr}
"""


def slide(sl, i, n, c):
    t = sl["type"]
    ar = c.get("lang") == "ar"
    eye = f'<div class="rule"></div><div class="eye">{e(sl.get("eyebrow", ""))}</div>'
    if t == "cover":
        h = e(sl["title"]) + (f'<br><span>{e(sl["highlight"])}</span>' if sl.get("highlight") else "")
        body = f'{eye}<h1>{h}</h1>' + (f'<div class="sub">{e(sl["sub"])}</div>' if sl.get("sub") else "")
        body += f'<div class="swipe">{"اسحب ←" if ar else "Swipe →"}</div>'
    elif t == "stat":
        body = (f'{eye}<div class="num">{e(sl["number"])}</div><div class="lab">{e(sl["label"])}</div>'
                + (f'<div class="note">{e(sl["note"])}</div>' if sl.get("note") else ""))
    elif t == "bars":
        mx = max(float(b["value"]) for b in sl["bars"]) or 1
        rows = "".join(
            f'<div class="row"><div class="name">{e(b["label"])}</div><div class="barw">'
            f'<div class="bar{" hl" if b.get("highlight") else ""}" style="width:{max(8, int(640 * float(b["value"]) / mx))}px"></div>'
            f'<div class="val">{e(b["display"])}</div></div></div>' for b in sl["bars"][:6])
        body = f'{eye}<h2>{e(sl["title"])}</h2><div class="chart">{rows}</div>'
    elif t == "points":
        body = f'{eye}<h2>{e(sl["title"])}</h2><ol>' + "".join(f"<li>{e(p)}</li>" for p in sl["points"][:4]) + "</ol>"
    elif t == "end":
        body = (f'{eye}<div class="big">{e(sl["text"])}</div>'
                + (f'<div class="q">{e(sl["question"])}</div>' if sl.get("question") else ""))
        if c.get("sources"):
            body += f'<div class="src">{"المصادر" if ar else "Sources"}: {e(c["sources"])}</div>'
    else:
        sys.exit(f"unknown slide type {t}")
    dark = " dark" if t in ("cover", "end") else ""
    foot = f'<div class="foot"><div class="who"><i></i>Hussain Nasser</div><div class="pg">{i}/{n}</div></div>'
    return f'<section class="s{dark}">{body}{foot}</section>'


def build(c):
    css = (CSS + (AR_CSS if c.get("lang") == "ar" else "")).replace("FONTS", FONTS.as_uri())
    n = len(c["slides"])
    pages = "".join(slide(sl, i + 1, n, c) for i, sl in enumerate(c["slides"]))
    return f'<!doctype html><html lang="{c.get("lang", "en")}"><head><meta charset="utf-8"><style>{css}</style></head><body>{pages}</body></html>'


def render(spec, out_dir):
    c = json.loads(Path(spec).read_text())
    if not 4 <= len(c["slides"]) <= 10:
        sys.exit("a carousel needs 4-10 slides")
    out = Path(out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    (tmp / "c.html").write_text(build(c))
    pdf = out / "carousel.pdf"
    subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", (tmp / "c.html").as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # cover thumbnail: render page 1 alone as PNG
    one = dict(c, slides=c["slides"][:1])
    (tmp / "p1.html").write_text(build(one).replace("<body>", '<body style="width:1080px;height:1350px;overflow:hidden">'))
    png = out / "cover.png"
    subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--virtual-time-budget=3000", "--window-size=1080,1350",
                    f"--screenshot={png}", (tmp / "p1.html").as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not pdf.exists() or pdf.stat().st_size < 10000 or not png.exists():
        sys.exit("render failed")
    shutil.rmtree(tmp, ignore_errors=True)
    print(pdf); print(png)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(sys.argv[1], sys.argv[2])
