#!/usr/bin/env python3
"""Build the template's pages from the content in site/data/content/*.json.

Every word lives in the JSON files; this generator holds layout only. Any text in [square brackets]
is a placeholder for the owner and is shown as one (class "ph"), never as a real value.
Run from the repository root:  python3 tools/designs/build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
BASE = "https://moving-van.business.sovereignweb.site"
REPO = "https://github.com/SovereignWebsite/Site__Template__Business__Moving-Van"


def esc(s):
    return html.escape(str(s), quote=True)


def ph(s):
    """Escape text and mark every [placeholder] so it can never pass for a real value."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', esc(s))


def head(c, path, css):
    t, d = esc(c["site"]["title"]), esc(c["site"]["description"])
    url = f"{BASE}{path}"
    img = f"{BASE}/assets/share/card-1200x630.jpg"
    return f"""<!doctype html>
<html lang="{esc(c['lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{t}">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="/assets/family-credit.css">
<link rel="stylesheet" href="{css}">
</head>
"""


FAMILY = """<details class="family-credit">
  <summary>Sovereign Website</summary>
  <ul>
    <li><a href="/start/">Start here</a></li>
    <li><a href="/agents/">Use with your AI</a></li>
    <li class="family-gap"><a href="/admin/">How this site was made</a></li>
    <li><a href="https://sovereignwebsite.ai/">Sovereign Website</a></li>
    <li><a href="https://sovereignwebsite.org/">Principles</a></li>
    <li><a href="https://sovereignwebsite.site/">Hosted</a></li>
    <li><a href="https://hub.sovereignweb.site/">Hub</a></li>
    <li><a href="https://agents.sovereignweb.site/">Agents</a></li>
    <li><a href="https://vault.sovereignwebsite.site/">Vault</a></li>
    <li><a href="https://agenticcells.ai/">AgentiCCells</a></li>
    <li><a href="https://riskmandate.ai/">RiskMandate</a></li>
    <li><a href="https://newsroom.sgit.ai/">Newsroom</a></li>
  </ul>
</details>
"""


def van_svg(v):
    """The side of the van: the firm's name on the panel, the load space drawn as three bands to scale."""
    x0, w, y0, row = 60, 470, 140, 30
    bands = []
    for i, load in enumerate(sorted(v["loads"], key=lambda l: -l["share"])):
        y = y0 + i * (row + 6)
        bw = round(w * load["share"])
        inside = bw >= 170  # a short band puts its label beside it, so the text never spills over the colour
        bands.append(
            f'<rect class="load load-{esc(load["id"])}" x="{x0}" y="{y}" width="{bw}" height="{row}" rx="4"/>'
            f'<text class="load-label{"" if inside else " beside"}" x="{x0 + 10 if inside else x0 + bw + 10}" y="{y + 22}">{esc(load["label"])}</text>'
        )
    return f"""<svg class="van" viewBox="0 0 800 318" role="img" aria-labelledby="van-t van-d">
<title id="van-t">{esc(v['title'])}</title>
<desc id="van-d">{esc(v['desc'])}</desc>
<rect class="body" x="30" y="30" width="530" height="225" rx="14"/>
<rect class="ph-box" x="135" y="50" width="320" height="82" rx="8"/>
<text class="panel-name" x="295" y="86" text-anchor="middle">{esc(v['panel_name'])}</text>
<text class="panel-line" x="295" y="118" text-anchor="middle">{esc(v['panel_line'])}</text>
{''.join(bands)}
<path class="cab" d="M560 255 V95 h110 q22 0 36 22 l44 70 q8 13 8 28 V255 Z"/>
<path class="window" d="M585 115 h78 q12 0 19 11 l36 58 h-133 Z"/>
<rect class="bumper" x="560" y="240" width="210" height="15" rx="6"/>
<circle class="wheel" cx="160" cy="278" r="30"/><circle class="hub" cx="160" cy="278" r="12"/>
<circle class="wheel" cx="660" cy="278" r="30"/><circle class="hub" cx="660" cy="278" r="12"/>
<line class="road" x1="0" y1="312" x2="800" y2="312"/>
</svg>"""


def design_van(c):
    v, s, h, q = c["van"], c["services"], c["how"], c["quote"]
    loads = "".join(
        f'<li><span class="swatch load-{esc(l["id"])}" aria-hidden="true"></span><strong>{esc(l["label"])}</strong>: {ph(l["note"])}</li>'
        for l in v["loads"])
    services = "".join(f'<li><h3>{esc(i["title"])}</h3><p>{ph(i["text"])}</p></li>' for i in s["items"])
    steps = "".join(f"<li>{ph(x)}</li>" for x in h["steps"])
    fields = []
    for f in q["fields"]:
        lab = f'<label for="{esc(f["id"])}">{esc(f["label"])}</label>'
        if f["type"] == "select":
            opts = "".join(f"<option>{esc(o)}</option>" for o in f["options"])
            ctl = f'<select id="{esc(f["id"])}" name="{esc(f["id"])}">{opts}</select>'
        elif f["type"] == "textarea":
            ctl = f'<textarea id="{esc(f["id"])}" name="{esc(f["id"])}" rows="3"></textarea>'
        else:
            ctl = f'<input id="{esc(f["id"])}" name="{esc(f["id"])}" type="{esc(f["type"])}">'
        fields.append(f'<div class="field">{lab}{ctl}</div>')
    contact = "".join(f"<li>{ph(x)}</li>" for x in q["contact"])
    return (head(c, "/", "/assets/van.css")
            + f"""<body>
<a class="skip" href="#main">Skip to content</a>
<aside class="demo-band" aria-label="Demo notice">{esc(c["demo_band"])}</aside>
{FAMILY}<header class="top">
  <a class="name" href="/">{ph(c['site']['name'])}</a>
  <nav class="own" aria-label="This site">
    <a href="#services">{esc(c['nav']['services'])}</a>
    <a href="#how">{esc(c['nav']['how'])}</a>
    <a class="btn small" href="#quote">{esc(c['nav']['quote'])}</a>
  </nav>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <p class="kicker">{ph(c['hero']['kicker'])}</p>
  <h1 id="hero-h">{esc(c['hero']['heading'])}</h1>
  <p class="lead">{ph(c['hero']['lead'])}</p>
  <figure class="van-fig">
    {van_svg(v)}
    <figcaption>
      <ul class="loads">{loads}</ul>
      <p class="small-print">{ph(v['caption'])}</p>
    </figcaption>
  </figure>
  <p><a class="btn" href="#quote">{esc(c['hero']['cta'])}</a></p>
</section>
<section id="services" aria-labelledby="services-h">
  <h2 id="services-h">{esc(s['heading'])}</h2>
  <ul class="cards">{services}</ul>
  <p>{ph(s['price_line'])}</p>
  <p>{ph(s['cover_note'])}</p>
</section>
<section id="how" aria-labelledby="how-h">
  <h2 id="how-h">{esc(h['heading'])}</h2>
  <ol class="steps">{steps}</ol>
</section>
<section id="quote" aria-labelledby="quote-h">
  <h2 id="quote-h">{esc(q['heading'])}</h2>
  <p class="demo-note" role="note">{esc(q['demo_note'])}</p>
  <form class="quote">
    {''.join(fields)}
    <button type="button" disabled>{esc(q['button'])}</button>
  </form>
  <h3>{esc(q['contact_heading'])}</h3>
  <ul class="contact">{contact}</ul>
</section>
</main>
<footer class="foot">
<nav class="site-links" aria-label="About this site">
  <a href="/start/">Start here</a>
  <a href="/agents/">Use with your AI</a>
  <a href="/admin/">How this site was made</a>
  <a href="/policy/">How this site is governed</a>
</nav>
<p>{esc(c['footer']['about'])} Source: <a href="{REPO}">github.com/SovereignWebsite/Site__Template__Business__Moving-Van</a>.</p>
</footer>
</body>
</html>
""")


def main():
    c = json.loads((SITE / "data/content/en.json").read_text())
    (SITE / "index.html").write_text(design_van(c))
    print("built site/index.html (design 1: The van)")


if __name__ == "__main__":
    main()
