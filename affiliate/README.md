# Practical AI Tools: affiliate site

An affiliate content site in the **AI tools** niche. Articles are written in Markdown and
built into a static site in `/docs`, which GitHub Pages serves for free.

| File | What it is |
|---|---|
| `content/*.md` | Articles (front matter: title, description, date; `draft: true` hides one) |
| `pages/*.md` | About, disclosure and privacy pages |
| `links.json` | **Every affiliate link in one place.** Paste approved links into `"affiliate"` |
| `site.json` | Site name, tagline, domain, base path |
| `build.py` | Builds everything into `/docs` |
| `PROGRAMS.md` | Which affiliate programs to join, in order |
| `SOCIAL.md` | 10 short-form video scripts to drive traffic |

In articles, link to a tool with `[Try Fliki](go:fliki)`. It becomes `/go/fliki/`, which
redirects to your affiliate link (or the plain site until you're approved).

## Build

```bash
pip install markdown
python3 affiliate/build.py
```

## Go-live checklist (owner)

1. **Turn on GitHub Pages:** repo **Settings → Pages → Build and deployment → Deploy from a branch**,
   choose the branch this is merged into (e.g. `main`) and the **/docs** folder. The site appears
   at https://ronnie-recky.github.io/orsopapi/ within a few minutes.
2. **Set up a payout account:** PayPal or Payoneer.
3. **Apply to the programs** in `PROGRAMS.md`, top to bottom.
4. **Register in Google Search Console** (free), add the site, and submit `sitemap.xml` so Google
   starts indexing it.
5. **Make a TikTok / YouTube Shorts account** for the site and start posting from `SOCIAL.md`.
6. Send approved affiliate links to Claude, or paste them into `links.json`.

## Later: own domain (~$10–15/yr)
Buy a domain, add it under Settings → Pages → Custom domain, then set `"domain"` to it and
`"base_url"` to `""` in `site.json` and rebuild. A real domain improves approval rates and trust.

## Rules we follow
- No fake reviews or invented "we tested it" claims. Describe features honestly and say when
  a free option is enough.
- Affiliate disclosure at the top of every article (automatic) and on social posts (#ad).
- Re-check prices and features when updating an article. They change often.
