# Infographics

Build an HTML file, render it to PNG with headless Chromium. No design tool, no
subscription, and the output is version-controlled and re-editable.

## Workflow

1. Copy a starter from `assets/` into `studio/infographics/<slug>.html`.
2. Edit the content. Keep the brand tokens.
3. Render:
```bash
python3 .claude/skills/content-studio/scripts/render.py \
  studio/infographics/<slug>.html --preset portrait
```
4. The PNG lands next to the HTML. Show it to the user with the Read tool before
   declaring it done — always look at what you made.

### Presets

| Preset | Size | Use |
|---|---|---|
| `square` | 1080×1080 | LinkedIn / Instagram feed |
| `portrait` | 1080×1350 | Best LinkedIn & IG feed real estate — **default** |
| `story` | 1080×1920 | Stories, Reels covers |
| `landscape` | 1200×630 | Link previews, X |
| `carousel` | 1080×1350 | Multi-slide; see below |

Rendering is at 2× device scale, so text stays sharp.

## Carousels

Put each slide in `<section class="slide">`. With `--preset carousel` the script
renders one PNG per slide, numbered `<slug>-01.png`, `<slug>-02.png`, …

Carousel rules that actually matter:
- Slide 1 is the hook and does nothing else. No logo, no intro.
- One idea per slide. If a slide needs a comma-and, split it.
- 6–10 slides. Past 10, completion rate collapses.
- Last slide is the ask, and only the ask.

## Brand system

**All colours, fonts and canvas padding live in one file:
`assets/brand-tokens.css`.** That is the file to edit when the branding
changes — `brand.css` holds layout and components only and contains no
hardcoded colour values, so a rebrand is a single-file edit.

Read `brand-tokens.css` rather than reproducing values here, so this document
can't drift from what actually renders. When writing an infographic, always
reference tokens (`var(--accent)`), never literal hexes — a graphic with a
hardcoded colour silently survives the next rebrand and looks wrong.

One other place carries a copy of the palette and must be updated by hand to
match: `studio/dashboard.html` (inline, since it's served from `studio/`).
Note that `assets/css/styles.css` in this repo still holds the OLD purple/gold
site — the live gigianddanni.com was rebranded (2026: black/pink, AI
receptionists) and deploys from elsewhere. `brand-tokens.css` follows the live
site, not that file.

Fonts are embedded as base64 in `brand-fonts.css`, so rendering works with no
network access. Don't swap them for a Google Fonts `<link>` — the renderer runs
offline and you'll silently get Times New Roman. If the brand fonts change,
edit the family list at the top of `scripts/embed_fonts.py` and regenerate:

```bash
python3 .claude/skills/content-studio/scripts/embed_fonts.py \
  > .claude/skills/content-studio/assets/brand-fonts.css
```

### Design rules

- **Pink is a highlight, not a background.** One accented element per graphic
  (`class="accent"`), on the single thing that matters. Pink everywhere means
  nothing is emphasised. The exception is the `.pill` CTA button, which is
  solid pink by design — a pill slide should have no other accent.
- **Light blush ground, near-black heavy uppercase headlines** is the house
  look. A `class="dark"` variant exists for contrast within a carousel —
  alternate deliberately, not randomly.
- **Eyebrows are letter-spaced uppercase mono, always pink** — they're the
  site's kicker style and do a lot of the brand recognition.
- **Type scale is aggressive.** These are read at thumbnail size on a phone. Hero
  text at 72–110px on a 1080px canvas. If it looks too big on your screen, it's
  probably right.
- **Fewer than 30 words per graphic.** An infographic that needs a paragraph
  should be a post instead.
- **Generous margins** — 80–100px on a 1080 canvas. Social UI crops edges.
- Never centre long text. Left-align anything over one line.

## Checking your work

Render, then **Read the PNG**. Look for: text overflowing its container, fonts
that fell back to a serif (means the base64 embed broke), pink used on more
than one element, and whether the hero line is legible when you imagine it at
1/4 size.
