#!/usr/bin/env python3
"""Build the affiliate site into ../docs (served by GitHub Pages).

Usage:  pip install markdown && python3 affiliate/build.py

- Articles live in affiliate/content/*.md, static pages in affiliate/pages/*.md.
  Each file starts with a front-matter block:
      ---
      title: ...
      description: ...
      date: 2026-11-26
      ---
- Affiliate links are written as  [Try Synthesia](go:synthesia)  and point at
  /go/synthesia/, a redirect page generated from affiliate/links.json. Paste your
  affiliate URL into links.json once you're approved and every article updates.
"""
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs"
CONFIG = json.loads((ROOT / "site.json").read_text())
LINKS = json.loads((ROOT / "links.json").read_text())
BASE = CONFIG["base_url"].rstrip("/")


def parse(path):
    text = path.read_text()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    meta.setdefault("slug", path.stem)
    return meta, text


def link_target(slug):
    if slug not in LINKS:
        raise SystemExit(f"Unknown affiliate slug 'go:{slug}' - add it to links.json")
    return f"{BASE}/go/{slug}/"


def render_md(text):
    # Internal links are written site-relative, e.g. [guide](/best-ai-voice-generators/)
    text = re.sub(r"\]\((/[^)\s]*)\)", lambda m: f"]({BASE}{m.group(1)})", text)
    text = re.sub(r"\]\(go:([a-z0-9-]+)\)", lambda m: f"]({link_target(m.group(1))})", text)
    text = re.sub(r'href="go:([a-z0-9-]+)"', lambda m: f'href="{link_target(m.group(1))}"', text)
    body = markdown.markdown(text, extensions=["tables", "toc", "attr_list"])
    # Outbound affiliate links: sponsored + nofollow, open in new tab.
    body = re.sub(
        rf'<a href="({re.escape(BASE)}/go/[^"]+)"',
        r'<a href="\1" rel="sponsored nofollow" target="_blank"',
        body,
    )
    return body


def page(title, description, body, path, is_article=False, date=None):
    site = CONFIG["name"]
    full_title = title if title == site else f"{title} | {site}"
    canonical = f"{CONFIG['domain']}{BASE}{path}"
    disclosure = (
        f'<p class="disclosure">Some links on this page are affiliate links. If you buy through them '
        f'we may earn a commission at no extra cost to you. <a href="{BASE}/disclosure/">Learn more</a>.</p>'
        if is_article else ""
    )
    meta_date = f'<p class="date">Updated {date}</p>' if date else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="{'article' if is_article else 'website'}">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{BASE}/style.css">
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="{BASE}/">{html.escape(site)}</a>
<nav><a href="{BASE}/">Guides</a><a href="{BASE}/about/">About</a></nav>
</div></header>
<main class="wrap">
{disclosure}
{'<article>' if is_article else ''}
{meta_date if is_article else ''}
{body}
{'</article>' if is_article else ''}
</main>
<footer class="site"><div class="wrap">
<p>&copy; {dt.date.today().year} {html.escape(site)} &middot;
<a href="{BASE}/disclosure/">Affiliate disclosure</a> &middot;
<a href="{BASE}/privacy/">Privacy</a> &middot; <a href="{BASE}/about/">About</a></p>
</div></footer>
</body>
</html>
"""


def redirect_page(slug, info):
    url = info.get("affiliate") or info["url"]
    u = html.escape(url, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url={u}">
<title>Redirecting to {html.escape(info['name'])}</title>
<link rel="canonical" href="{u}">
</head><body>
<p>Taking you to <a href="{u}" rel="sponsored nofollow">{html.escape(info['name'])}</a>...</p>
<script>location.replace({json.dumps(url)});</script>
</body></html>
"""


def write(rel, content):
    dest = OUT / rel.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("")

    urls = []
    articles = []
    for f in sorted((ROOT / "content").glob("*.md")):
        meta, text = parse(f)
        if meta.get("draft") == "true":
            continue
        path = f"/{meta['slug']}/"
        write(path + "index.html",
              page(meta["title"], meta["description"], render_md(text), path, True, meta.get("date")))
        articles.append(meta)
        urls.append((path, meta.get("date")))

    for f in sorted((ROOT / "pages").glob("*.md")):
        meta, text = parse(f)
        path = f"/{meta['slug']}/"
        write(path + "index.html", page(meta["title"], meta["description"], render_md(text), path))
        urls.append((path, None))

    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    cards = "\n".join(
        f'<a class="card" href="{BASE}/{a["slug"]}/"><h2>{html.escape(a["title"])}</h2>'
        f'<p>{html.escape(a["description"])}</p><span>Read the guide &rarr;</span></a>'
        for a in articles
    )
    home = (
        f'<section class="hero"><h1>{html.escape(CONFIG["tagline"])}</h1>'
        f'<p>{html.escape(CONFIG["intro"])}</p></section>\n<div class="cards">{cards}</div>'
    )
    write("/index.html", page(CONFIG["name"], CONFIG["intro"], home, "/"))
    urls.insert(0, ("/", None))

    for slug, info in LINKS.items():
        write(f"/go/{slug}/index.html", redirect_page(slug, info))

    today = dt.date.today().isoformat()
    sm = "\n".join(
        f"<url><loc>{CONFIG['domain']}{BASE}{p}</loc><lastmod>{d or today}</lastmod></url>" for p, d in urls
    )
    write("/sitemap.xml",
          f'<?xml version="1.0" encoding="UTF-8"?>\n'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    write("/robots.txt",
          f"User-agent: *\nDisallow: {BASE}/go/\nSitemap: {CONFIG['domain']}{BASE}/sitemap.xml\n")

    missing = [s for s, i in LINKS.items() if not i.get("affiliate")]
    print(f"Built {len(articles)} articles, {len(LINKS)} redirect links into {OUT}")
    if missing:
        print(f"Links still pointing at the plain site (no commission yet): {', '.join(missing)}")


if __name__ == "__main__":
    main()
