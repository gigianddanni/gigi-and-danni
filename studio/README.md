# Content Studio

A self-hosted alternative to tools like [Kleo](https://kleo.so) ($99/mo), built
as a Claude Code skill instead of an app.

**Why there's no API key, no server, and no subscription:** you're already
talking to Claude. A tool like Kleo mostly sells a wrapper that pipes your text
to an AI and stores your stuff. The AI part you already have. What's actually
missing is *memory and structure* — your voice, your swipe file, your calendar —
and that's just files plus instructions.

So the app is a folder, and the interface is conversation.

## Using it

Just ask, in plain language. The skill loads automatically:

- *"Build my voice profile"* — the setup step. **Do this first.**
- *"Write me a LinkedIn post about pricing"*
- *"Save this post to my swipe file"* (paste it)
- *"What's on my calendar this week?"*
- *"Make an infographic about the operator vs chatbot difference"*
- *"This post got 143 likes and 22 comments"* — logs it, so the studio learns

## What's where

```
studio/
  voice/voice-profile.md    the voice rules — everything depends on this
  voice/samples/            raw past posts the profile was derived from
  swipe/swipes.json         saved inspiration + why each one worked
  calendar/posts.json       pipeline: idea → draft → ready → posted
  drafts/                   full post bodies, one file each
  infographics/             .html sources + rendered .png
  dashboard.html            visual overview
```

The skill itself lives in `.claude/skills/content-studio/`.

## The dashboard

Browsers block `fetch` on `file://`, so serve it:

```bash
python3 -m http.server 8000 --directory studio
# then open http://localhost:8000/dashboard.html
```

## Infographics

Copy a starter, edit the content, render:

```bash
cp .claude/skills/content-studio/assets/starter-single.html studio/infographics/my-graphic.html
python3 .claude/skills/content-studio/scripts/render.py studio/infographics/my-graphic.html --preset portrait
```

Presets: `square` (1080×1080), `portrait` (1080×1350), `story` (1080×1920),
`landscape` (1200×630), `carousel` (one PNG per `<section class="slide">`).
Output is 2× for sharp text. Fonts are embedded as base64, so rendering works
offline.

**Rendering needs `chrome-headless-shell`.** It ships with Playwright and is
found automatically. Regular Chrome also works, but its headless mode reserves
window chrome, which leaves the bottom ~87px of each PNG unpainted. If you see
that strip:

```bash
npx playwright install chromium-headless-shell
```

## Rebranding

Colours, fonts and spacing live in **one file**:

```
.claude/skills/content-studio/assets/brand-tokens.css
```

Edit it and every future graphic follows. `brand.css` contains no hardcoded
colours, so nothing else needs touching there.

Two other files carry the palette and have to be updated by hand to match,
because CSS can't be shared across them — both say so in a comment:

- `assets/css/styles.css` — the public website (the real brand definition)
- `studio/dashboard.html` — inline, since it's served from `studio/`

If the fonts change, edit the family list at the top of `embed_fonts.py` and
regenerate `brand-fonts.css` (command in the file's header comment).

## Two things this deliberately doesn't do

**It doesn't scrape LinkedIn.** Kleo's original extension overlaid and scraped
the feed, reached 70,000+ users, and got a cease-and-desist from LinkedIn in
2025 for it. Swipe entries here are saved by paste. Slower, and it can't get
your account restricted.

**It doesn't auto-post.** Drafts get copied out by hand. You read the thing
before it goes out under your name.

## The part that compounds

Log real numbers when a post lands. `stats` shows which templates and hooks
actually work for you, and durable findings get folded back into the voice
profile. That loop is the whole point — it's the thing a subscription can't do
for you, because it needs *your* results.

Three posts is an anecdote. Wait for ten before believing a pattern.
