#!/usr/bin/env python3
"""Build the template's pages from the content in site/data/content/*.json.

Every word lives in the JSON files; this generator holds layout only. Any text in [square brackets]
is a placeholder for the owner and is shown as one (class "ph"), never as a real value.
Five designs, each built around its own idea (design.b's brief), plus /designs/ with all five side by side.
Run from the repository root:  python3 tools/designs/build.py
Then refresh the chooser's screenshots:  node tools/designs/shots.mjs  (needs the built _site)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
BASE = "https://moving-van.business.template.sovereignweb.site"
CUR = ' aria-current="page"'
REPO = "https://github.com/SovereignWebsite/Site__Template__Business__Moving-Van"


def esc(s):
    return html.escape(str(s), quote=True)


def ph(s):
    """Escape text and mark every [placeholder] so it can never pass for a real value."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', esc(s))


def head(c, path, title, css):
    t, d = esc(title), esc(c["site"]["description"])
    url = f"{BASE}{path}"
    img = f"{BASE}/assets/share/card-1200x630.jpg"
    links = "\n".join(f'<link rel="stylesheet" href="/assets/{x}">' for x in ["family-credit.css", "base.css"] + css)
    return f"""<!doctype html>
<html lang="{esc(c['lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(c['site']['title'])}">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(c['site']['title'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
{links}
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


def shot(c, d, cls=""):
    alt = c["chooser"]["shot_alt"].format(n=d["number"], name=d["name"])
    return (f'<img class="{cls}" src="/assets/designs/{esc(d["slug"])}.png" width="640" height="400" '
            f'alt="{esc(alt)}" loading="lazy">')


def chooser(c, current):
    ch = c["chooser"]
    items = []
    for d in c["designs"]:
        cur = d["slug"] == current
        items.append(
            f'<li><a href="{esc(d["path"])}"{CUR if cur else ""}>{shot(c, d)}'
            f'<span class="num">{d["number"]}</span> <strong>{esc(d["name"])}</strong>'
            f'{" <em>(" + esc(ch["current"]) + ")</em>" if cur else ""}<span class="line">{esc(d["line"])}</span></a></li>')
    return (f'<details class="chooser"><summary>{esc(ch["button"])}</summary>'
            f'<div class="chooser-panel"><p class="chooser-h">{esc(ch["heading"])}</p><ul>{"".join(items)}</ul>'
            f'<p><a href="/designs/"{CUR if current == "all" else ""}>{esc(ch["all"])}</a></p></div></details>')


def page(c, slug, path, title, css, main, quote_href="#quote"):
    return (head(c, path, title, css) + f"""<body class="d-{esc(slug)}">
<a class="skip" href="#main">Skip to content</a>
<aside class="demo-band" aria-label="Demo notice">{esc(c["demo_band"])}</aside>
{FAMILY}<header class="top">
  <a class="name" href="/">{ph(c['site']['name'])}</a>
  <nav class="own" aria-label="This site">
    {chooser(c, slug)}
    <a class="btn small" href="{quote_href}">{esc(c['nav']['quote'])}</a>
  </nav>
</header>
<main id="main">
{main}
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


def title_for(c, d):
    if d["path"] == "/":
        return c["site"]["title"]
    return f'{c["site"]["name"]}: {d["name"]} (design {d["number"]}, template)'


def quote_fields(c):
    out = []
    for f in c["quote"]["fields"]:
        lab = f'<label for="{esc(f["id"])}">{esc(f["label"])}</label>'
        if f["type"] == "select":
            opts = "".join(f"<option>{esc(o)}</option>" for o in f["options"])
            ctl = f'<select id="{esc(f["id"])}" name="{esc(f["id"])}">{opts}</select>'
        elif f["type"] == "textarea":
            ctl = f'<textarea id="{esc(f["id"])}" name="{esc(f["id"])}" rows="3"></textarea>'
        else:
            ctl = f'<input id="{esc(f["id"])}" name="{esc(f["id"])}" type="{esc(f["type"])}">'
        out.append(f'<div class="field">{lab}{ctl}</div>')
    return "".join(out)


def quote_section(c, before_fields=""):
    """The one action. In the demo the form sends nothing: no action, and its button is disabled."""
    q = c["quote"]
    contact = "".join(f"<li>{ph(x)}</li>" for x in q["contact"])
    return f"""<section id="quote" class="quote-sec" aria-labelledby="quote-h">
  <h2 id="quote-h">{esc(q['heading'])}</h2>
  <p class="demo-note" role="note">{esc(q['demo_note'])}</p>
  <form class="quote">
    {before_fields}{quote_fields(c)}
    <button type="button" disabled>{esc(q['button'])}</button>
  </form>
  <h3>{esc(q['contact_heading'])}</h3>
  <ul class="contact">{contact}</ul>
</section>"""


def services_list(c):
    s = c["services"]
    items = "".join(f'<li><h3>{esc(i["title"])}</h3><p>{ph(i["text"])}</p></li>' for i in s["items"])
    return f"""<section id="services" aria-labelledby="services-h">
  <h2 id="services-h">{esc(s['heading'])}</h2>
  <ul class="cards">{items}</ul>
  <p>{ph(s['price_line'])}</p>
  <p>{ph(s['cover_note'])}</p>
</section>"""


def how_section(c):
    h = c["how"]
    steps = "".join(f"<li>{ph(x)}</li>" for x in h["steps"])
    return f"""<section id="how" aria-labelledby="how-h">
  <h2 id="how-h">{esc(h['heading'])}</h2>
  <ol class="steps">{steps}</ol>
</section>"""


# Design 1: The van ---------------------------------------------------------------------------------------------

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
    v = c["van"]
    loads = "".join(
        f'<li><span class="swatch load-{esc(l["id"])}" aria-hidden="true"></span><strong>{esc(l["label"])}</strong>: {ph(l["note"])}</li>'
        for l in v["loads"])
    return f"""<section class="hero" aria-labelledby="hero-h">
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
{services_list(c)}
{how_section(c)}
{quote_section(c)}"""


# Design 2: Moving day ------------------------------------------------------------------------------------------

def design_day(c):
    m = c["moving_day"]
    steps = []
    for i, s in enumerate(m["steps"], 1):
        cta = f'<p><a class="btn" href="#quote">{esc(c["hero"]["cta"])}</a></p>' if s.get("cta") else ""
        steps.append(f"""<li class="day-step">
  <h2><span class="day-n" aria-hidden="true">{i}</span> {esc(s['name'])}</h2>
  <dl><div><dt>{esc(m['we'])}</dt><dd>{ph(s['we'])}</dd></div><div><dt>{esc(m['you'])}</dt><dd>{ph(s['you'])}</dd></div></dl>
  {cta}
</li>""")
    return f"""<section class="hero" aria-labelledby="hero-h">
  <p class="kicker">{ph(m['kicker'])}</p>
  <h1 id="hero-h">{esc(m['heading'])}</h1>
  <p class="lead">{ph(m['lead'])}</p>
</section>
<ol class="day">{''.join(steps)}</ol>
<section class="day-small" aria-label="{esc(c['services']['heading'])}">
  <p>{ph(c['services']['price_line'])} {ph(c['services']['cover_note'])}</p>
</section>
{quote_section(c)}"""


# Design 3: The boxes -------------------------------------------------------------------------------------------

def design_boxes(c):
    b = c["boxes"]
    boxes = "".join(f"""<li><details class="box">
  <summary><span class="stamp">{esc(i['label'])}</span><span class="box-title">{esc(i['title'])}</span></summary>
  <p>{ph(i['text'])}</p>
</details></li>""" for i in b["items"])
    return f"""<section class="hero" aria-labelledby="hero-h">
  <p class="kicker">{ph(b['kicker'])}</p>
  <h1 id="hero-h">{esc(b['heading'])}</h1>
  <p class="lead">{ph(b['lead'])}</p>
</section>
<ul class="stack">{boxes}</ul>
<p class="cover">{ph(c['services']['cover_note'])}</p>
{how_section(c)}
{quote_section(c)}"""


# Design 4: The inventory ---------------------------------------------------------------------------------------

def design_inventory(c):
    inv = c["inventory"]

    def boxes(items, prefix, cls):
        return "".join(f'<li><input type="checkbox" class="{cls}" id="{prefix}-{i}" name="{prefix}-{i}">'
                       f'<label for="{prefix}-{i}">{esc(x)}</label></li>' for i, x in enumerate(items, 1))

    checklist = f"""<fieldset class="rooms"><legend>{esc(inv['rooms_legend'])}</legend><ul>{boxes(inv['rooms'], 'room', 'room')}</ul></fieldset>
    <fieldset class="extras"><legend>{esc(inv['extras_legend'])}</legend><ul>{boxes(inv['extras'], 'extra', 'extra')}</ul></fieldset>
    <p class="tally">{esc(inv['summary'])} <span class="count"></span></p>
    <p class="no-price">{ph(inv['no_price'])}</p>
    """
    return f"""<section class="hero" aria-labelledby="hero-h">
  <p class="kicker">{ph(inv['kicker'])}</p>
  <h1 id="hero-h">{esc(inv['heading'])}</h1>
  <p class="lead">{ph(inv['lead'])}</p>
</section>
{quote_section(c, checklist)}"""


# Design 5: The card --------------------------------------------------------------------------------------------

def design_card(c):
    k, q = c["card"], c["quote"]
    facts = "".join(f"<li>{ph(x)}</li>" for x in k["facts"])
    contact = "".join(f"<li>{ph(x)}</li>" for x in q["contact"])
    return f"""<article class="card" aria-labelledby="card-h">
  <h1 id="card-h">{ph(k['heading'])}</h1>
  <p class="card-sub">{ph(k['sub'])}</p>
  <ul class="facts">{facts}</ul>
  <p class="call">{esc(k['call'])}</p>
  <ul class="card-contact">{contact}</ul>
  <p class="demo-note" role="note">{esc(c['demo_band'])}</p>
</article>
<p class="print-note">{esc(k['print'])}</p>"""


# All five, side by side ----------------------------------------------------------------------------------------

def designs_page(c):
    ch = c["chooser"]
    cards = "".join(f"""<li><a href="{esc(d['path'])}">{shot(c, d, 'big')}
  <span class="num">{d['number']}</span> <strong>{esc(d['name'])}</strong><span class="line">{esc(d['line'])}</span></a></li>"""
                    for d in c["designs"])
    return f"""<section class="hero" aria-labelledby="hero-h">
  <h1 id="hero-h">{esc(ch['all_heading'])}</h1>
  <p class="lead">{esc(ch['all_lead'])}</p>
</section>
<ul class="all-five">{cards}</ul>"""


DESIGNS = {
    "van": (design_van, ["van.css"]),
    "moving-day": (design_day, ["moving-day.css"]),
    "boxes": (design_boxes, ["boxes.css"]),
    "inventory": (design_inventory, ["inventory.css"]),
    "card": (design_card, ["card.css"]),
}


def write(path, text):
    f = SITE / path.strip("/") / "index.html" if path != "/" else SITE / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    print(f"built {f.relative_to(ROOT)}")


def main():
    c = json.loads((SITE / "data/content/en.json").read_text())
    for d in c["designs"]:
        fn, css = DESIGNS[d["slug"]]
        quote_href = "/#quote" if d["slug"] == "card" else "#quote"
        write(d["path"], page(c, d["slug"], d["path"], title_for(c, d), css, fn(c), quote_href))
    t = f'{c["site"]["name"]}: {c["chooser"]["all_heading"]} (template)'
    write("/designs/", page(c, "all", "/designs/", t, ["designs.css"], designs_page(c), "/#quote"))


if __name__ == "__main__":
    main()
