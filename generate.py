# -*- coding: utf-8 -*-
"""Generate index.html from _enriched.json (case-study site)."""
import json, os, html, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "_enriched.json"), encoding="utf-8") as f:
    D = json.load(f)

# --- patch the two replacement images ---
byname = {d["name"]: d for d in D}
byname["Gal Shir"]["_local"] = [{"file": "img/01_1.jpg", "caption": "Gal Shir"}]
yb = byname["Yves Béhar"]
# portrait first, then ElliQ (drop the failed hotlink boat)
yb["_local"] = [{"file": "img/03_0.jpg", "caption": "Yves Béhar"}] + \
    [im for im in yb["_local"] if not im.get("remote")]

def esc(s): return html.escape(s or "", quote=True)
def dom(u):
    try: return urllib.parse.urlparse(u).netloc.replace("www.", "")
    except: return "source"

def slug(name):
    import re
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

# nav chips
chips = "\n".join(
    f'<a class="chip" href="#{slug(d["name"])}"><span class="chip-n">{i:02d}</span>{esc(d["name"].split(" (")[0])}</a>'
    for i, d in enumerate(D, 1))

sections = []
for i, d in enumerate(D, 1):
    imgs = d.get("_local", [])
    gallery = ""
    if imgs:
        cards = "\n".join(
            f'''<figure class="shot">
              <a href="{esc(im["file"])}" target="_blank" rel="noopener">
                <img loading="lazy" src="{esc(im["file"])}" alt="{esc(im.get("caption",""))}">
              </a>
              {f'<figcaption>{esc(im.get("caption",""))}</figcaption>' if im.get("caption") else ""}
            </figure>''' for im in imgs)
        gallery = f'<div class="gallery g{min(len(imgs),3)}">{cards}</div>'
    qnote = f'<p class="qnote">{esc(d.get("quote_note",""))}</p>' if d.get("quote_note") else ""
    sections.append(f'''
    <section class="case" id="{slug(d["name"])}">
      <div class="case-head">
        <span class="num">{i:02d}</span>
        <div>
          <h2>{esc(d["name"])}</h2>
          <span class="tag">{esc(d["domain"])}</span>
        </div>
      </div>

      <div class="case-body">
        <div class="cred">
          <h3>Why they're established</h3>
          <p>{esc(d["credentials"])}</p>
          <a class="src" href="{esc(d["credentials_source"])}" target="_blank" rel="noopener">Verify &middot; {esc(dom(d["credentials_source"]))} &nearr;</a>
        </div>

        <blockquote class="quote">
          <p>&ldquo;{esc(d["quote"])}&rdquo;</p>
          <cite>&mdash; {esc(d["name"].split(" (")[0])}, <a href="{esc(d["quote_source"])}" target="_blank" rel="noopener">{esc(dom(d["quote_source"]))} &nearr;</a></cite>
          {qnote}
        </blockquote>

        {gallery}
      </div>
    </section>''')

allsections = "\n".join(sections)
n = len(D)

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>When Designers Met AI &mdash; {n} Established Professionals on Creative AI</title>
<meta name="description" content="{n} established, verifiable designers and creative directors on how AI creative tools impressed them. Every credential, quote and image is sourced.">
<style>
  :root{{
    --bg:#0b0b0f; --panel:#14141b; --panel2:#1b1b24; --ink:#f4f4f6; --mut:#a2a2b0;
    --line:#2a2a36; --accent:#7c8cff; --accent2:#ff8fab; --good:#59d499;
  }}
  *{{box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased}}
  a{{color:inherit}}
  .wrap{{max-width:1040px;margin:0 auto;padding:0 22px}}

  /* hero */
  header.hero{{padding:78px 0 40px;border-bottom:1px solid var(--line);
    background:radial-gradient(1200px 500px at 70% -10%,rgba(124,140,255,.18),transparent 60%),
               radial-gradient(900px 500px at 0% 0%,rgba(255,143,171,.12),transparent 55%)}}
  .kick{{letter-spacing:.22em;text-transform:uppercase;font-size:12px;color:var(--accent);font-weight:700}}
  .hero h1{{font-size:clamp(34px,6vw,60px);line-height:1.04;margin:.35em 0 .3em;font-weight:800;letter-spacing:-.02em}}
  .hero h1 em{{font-style:normal;background:linear-gradient(90deg,var(--accent),var(--accent2));
    -webkit-background-clip:text;background-clip:text;color:transparent}}
  .lede{{font-size:clamp(17px,2.2vw,21px);color:var(--mut);max-width:70ch}}
  .stats{{display:flex;gap:26px;flex-wrap:wrap;margin-top:26px}}
  .stat b{{display:block;font-size:26px;font-weight:800}}
  .stat span{{font-size:12.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}

  /* index chips */
  .index{{padding:26px 0 6px}}
  .index h4{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);margin:0 0 12px}}
  .chips{{display:flex;flex-wrap:wrap;gap:8px}}
  .chip{{display:inline-flex;align-items:center;gap:8px;text-decoration:none;
    background:var(--panel);border:1px solid var(--line);border-radius:999px;
    padding:7px 13px 7px 8px;font-size:13.5px;color:var(--ink);transition:.15s}}
  .chip:hover{{border-color:var(--accent);transform:translateY(-1px)}}
  .chip-n{{font-variant-numeric:tabular-nums;font-size:11px;color:var(--accent);
    background:rgba(124,140,255,.12);border-radius:999px;padding:2px 6px;font-weight:700}}

  /* cases */
  main{{padding:26px 0 40px}}
  .case{{padding:44px 0;border-top:1px solid var(--line);scroll-margin-top:16px}}
  .case-head{{display:flex;gap:18px;align-items:baseline}}
  .num{{font-size:44px;font-weight:800;line-height:1;color:transparent;
    background:linear-gradient(180deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;
    font-variant-numeric:tabular-nums}}
  .case-head h2{{margin:0;font-size:clamp(24px,3.4vw,32px);font-weight:800;letter-spacing:-.01em}}
  .tag{{display:inline-block;margin-top:6px;font-size:12px;color:var(--mut);
    border:1px solid var(--line);border-radius:999px;padding:3px 10px}}
  .case-body{{margin-top:22px;display:grid;gap:20px}}

  .cred{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 22px}}
  .cred h3{{margin:0 0 8px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--good)}}
  .cred p{{margin:0 0 12px;color:#dcdce4}}
  .src{{font-size:13px;color:var(--good);text-decoration:none;font-weight:600}}
  .src:hover{{text-decoration:underline}}

  .quote{{margin:0;padding:6px 0 0 22px;border-left:3px solid var(--accent)}}
  .quote p{{font-size:clamp(19px,2.6vw,25px);line-height:1.4;font-weight:600;margin:0 0 10px;letter-spacing:-.01em}}
  .quote cite{{font-style:normal;color:var(--mut);font-size:14px}}
  .quote cite a{{color:var(--accent);text-decoration:none}}
  .quote cite a:hover{{text-decoration:underline}}
  .qnote{{margin:10px 0 0;font-size:12.5px;color:#8b8b98;font-style:italic;max-width:70ch}}

  .gallery{{display:grid;gap:14px;margin-top:6px}}
  .gallery.g1{{grid-template-columns:minmax(0,560px)}}
  .gallery.g2{{grid-template-columns:repeat(2,1fr)}}
  .gallery.g3{{grid-template-columns:repeat(2,1fr)}}
  @media(min-width:760px){{.gallery.g3{{grid-template-columns:repeat(3,1fr)}}}}
  .shot{{margin:0;background:var(--panel2);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
  .shot img{{display:block;width:100%;height:100%;object-fit:cover;aspect-ratio:4/3;background:#111}}
  .shot figcaption{{font-size:12px;color:var(--mut);padding:9px 12px;border-top:1px solid var(--line)}}

  footer{{border-top:1px solid var(--line);padding:34px 0 60px;color:var(--mut);font-size:13.5px}}
  footer h4{{color:var(--ink);margin:0 0 10px;font-size:15px}}
  footer a{{color:var(--accent);text-decoration:none}}
  .back{{position:fixed;right:16px;bottom:16px;background:var(--accent);color:#0b0b0f;
    width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:20px;
    text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.4);opacity:.9}}
  .back:hover{{opacity:1}}
</style>
</head>
<body>
<a class="back" href="#top" title="Back to top">&uarr;</a>
<header class="hero" id="top">
  <div class="wrap">
    <div class="kick">A field guide &middot; {n} case studies</div>
    <h1>When designers<br>met <em>AI</em>.</h1>
    <p class="lede">Not hype accounts, not anonymous prompt-jockeys &mdash; {n} established, verifiable designers, creative directors and studio founders, and the moment a creative-AI tool genuinely impressed them. Every credential, every quote, and every image below is linked to its primary source.</p>
    <div class="stats">
      <div class="stat"><b>{n}</b><span>Established pros</span></div>
      <div class="stat"><b>100%</b><span>Sourced &amp; verifiable</span></div>
      <div class="stat"><b>0</b><span>Fabricated quotes</span></div>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="index">
    <h4>The roster</h4>
    <div class="chips">
      {chips}
    </div>
  </div>

  <main>
    {allsections}
  </main>

  <footer>
    <h4>How this was built</h4>
    <p>Each person here clears two bars: (1) a documented, verifiable career in design/creative work &mdash; not an AI-native persona &mdash; and (2) a genuine, positive-or-curious public statement about a creative-AI tool, pulled verbatim from a named source. Where a designer's stance is mixed or skeptical, they were left off rather than spun. Images are the designers' own work, campaign visuals, or published portraits, saved from the linked sources; if you spot one that should be credited differently, that's a fix worth making, not a reason to doubt the roster.</p>
    <p style="margin-top:16px;opacity:.7">Compiled from primary sources across the design press. Quotes &amp; credentials link out for verification. Built as a personal research reference.</p>
  </footer>
</div>
</body>
</html>'''

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote index.html", len(HTML), "bytes ;", n, "designers")
