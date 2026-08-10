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

These are the live tokens from `assets/css/styles.css`. Keep them in sync — if
the site palette changes, update both.

```css
--plum:          #3d2545;   /* primary dark, backgrounds, body text */
--violet:        #5a3870;   /* gradient partner to plum */
--gold:          #f0b86e;   /* accent — the only true highlight colour */
--lavender-mist: #f5eff8;   /* light text on dark */
--ghost-white:   #faf8fc;   /* light backgrounds */
--muted-plum:    #6b4a7a;   /* secondary text */
--soft-lilac:    #c8a8d8;
--light-lilac:   #e8d5f0;
--medium-purple: #9b6bb0;
```

Type: **Space Grotesk** for headings (300–700), **Inter** for body (300–600).
Both are embedded as base64 in the starter templates, so rendering works with no
network access. Don't swap them for a Google Fonts `<link>` — the renderer runs
offline and you'll silently get Times New Roman.

### Design rules

- **Gold is a highlight, not a background.** One gold element per graphic, on the
  single thing that matters. Gold everywhere means nothing is emphasised.
- **Dark plum ground, light text** is the house look. Light-ground variants exist
  in the starters for contrast within a carousel — alternate deliberately, not
  randomly.
- **Type scale is aggressive.** These are read at thumbnail size on a phone. Hero
  text at 72–110px on a 1080px canvas. If it looks too big on your screen, it's
  probably right.
- **Fewer than 30 words per graphic.** An infographic that needs a paragraph
  should be a post instead.
- **Generous margins** — 80–100px on a 1080 canvas. Social UI crops edges.
- Never centre long text. Left-align anything over one line.

## Checking your work

Render, then **Read the PNG**. Look for: text overflowing its container, fonts
that fell back to a serif (means the base64 embed broke), gold used more than
once, and whether the hero line is legible when you imagine it at 1/4 size.
