# Affiliate programs to join (in this order)

**Do these only after the site is live** (see README.md, step 1). Most programs review your
site before approving you, and an empty or missing site gets rejected.

When you apply, use:
- **Website:** https://ronnie-recky.github.io/orsopapi/
- **How you'll promote:** "Comparison guides and tutorials about AI tools on my website, plus
  short-form video on TikTok/YouTube Shorts."
- **Payout method:** PayPal or Payoneer (set one up first if you don't have it; both work from Uganda).

Commission figures below are what affiliate directories reported in late 2026. **Check the real
terms on each program's page before relying on them.** Find each program by searching
"<tool name> affiliate program" and only sign up on a page hosted on the tool's own domain
(or the network it sends you to).

| # | Program | Official site | Reported commission | Where it's used on our site |
|---|---|---|---|---|
| 1 | Systeme.io | systeme.io | ~60% lifetime recurring | Online business guide |
| 2 | Fliki | fliki.ai | ~30% recurring | Video + voice guides |
| 3 | ElevenLabs | elevenlabs.io | ~22% for 12 months | Voice guide, business guide |
| 4 | InVideo AI | invideo.io | check | Video guide, business guide |
| 5 | HeyGen | heygen.com | check | Video guide |
| 6 | Kit | kit.com | ~50% for 12 months | Online business guide |
| 7 | Frase | frase.io | ~30% for 12 months | Writing guide, business guide |
| 8 | Synthesia | synthesia.io | ~25% for 12 months | Video guide |
| 9 | Jasper | jasper.ai | ~25–30% recurring | Writing guide |
| 10 | Writesonic | writesonic.com | ~20% recurring | Writing guide |
| 11 | Murf AI | murf.ai | check | Voice guide |
| 12 | Canva | canva.com | check | Online business guide |
| 13 | Hostinger | hostinger.com | check | Online business guide |

## When you're approved

Send Claude your affiliate link for that tool, or paste it yourself into `affiliate/links.json`:

```json
"fliki": { "name": "Fliki", "url": "https://fliki.ai/", "affiliate": "PASTE-YOUR-LINK-HERE" },
```

Then rebuild (`python3 affiliate/build.py`) and push. Every button for that tool on every page
starts earning straight away.

## If you get rejected
That's normal early on. Re-apply after the site has 10–15 articles and some traffic. Most
programs let you re-apply after 30 days.
