---
name: content-studio
description: Personal brand content studio for Gigi & Danni — writes posts in Danni's own voice, keeps a swipe file of inspiration, serves hook and template libraries, runs a content calendar with performance tracking, and generates on-brand infographics as PNGs. Use whenever the user wants to write/draft/plan/schedule social content (LinkedIn, Instagram, X, Facebook, Threads), save a post as inspiration or to their swipe file, ask what's scheduled or what to post, build or refine their voice profile, review how posts performed, or make a branded graphic, infographic, quote card, or carousel.
---

# Content Studio

A self-hosted replacement for tools like Kleo. The AI is already here, so this
skill supplies what a subscription app actually sells: **persistent memory,
structure, and a house style.**

All state lives in `studio/` as plain files. Read them, edit them, commit them.

## Directory map

| Path | What it holds |
|---|---|
| `studio/voice/voice-profile.md` | The voice rules. **Read before writing any post.** |
| `studio/voice/samples/` | Raw past posts the profile was derived from |
| `studio/swipe/swipes.json` | Saved inspiration + why each one worked |
| `studio/calendar/posts.json` | The pipeline: ideas → drafts → ready → posted, with results |
| `studio/drafts/` | Full post bodies, one markdown file per post |
| `studio/infographics/` | Rendered PNGs + their source HTML |
| `studio/dashboard.html` | Visual overview — open in a browser |

## The five workflows

Pick the one that matches the request. Each has a reference file with the real
detail — read it when you run that workflow, not before.

### 1. Write a post
**Always** read `studio/voice/voice-profile.md` first. If it is still the
placeholder, run the voice onboarding in `references/voice.md` instead of
guessing — a generic post is worse than no post.

Then: read `references/hooks.md` for openers and `references/templates.md` for
structures. Check `studio/swipe/swipes.json` for anything relevant the user has
saved. Draft 2–3 distinct angles rather than one polished option, and say which
you'd ship.

Save accepted drafts to `studio/drafts/<slug>.md` and add a calendar entry.

### 2. Build or refine the voice profile
Read `references/voice.md`. This is the highest-leverage thing in the studio —
every other output depends on it. Run it properly, not quickly.

### 3. Save to the swipe file
When the user pastes a post they liked, or says "save this":
```bash
python3 .claude/skills/content-studio/scripts/studio.py swipe add \
  --author "Name" --text "..." --why "the structural reason it worked" --tags hook,story
```
The `--why` is the whole point. Record the *transferable mechanism* (e.g.
"opens with a number that contradicts the reader's assumption"), never "good
post". See `references/swipe.md`.

### 4. Run the calendar
```bash
python3 .claude/skills/content-studio/scripts/studio.py post list --upcoming
python3 .claude/skills/content-studio/scripts/studio.py post add --title "..." --date 2026-08-14 --platform linkedin
python3 .claude/skills/content-studio/scripts/studio.py post status <id> ready
python3 .claude/skills/content-studio/scripts/studio.py post log <id> --likes 120 --comments 14
```
Get today's date with `date +%F` — never assume it. See `references/calendar.md`.

**Logging results is what makes this compound.** When the user reports how a post
did, log it, then check whether the pattern belongs in the voice profile.

### 5. Make an infographic
Read `references/infographics.md`. Build an HTML file using the brand system,
then render:
```bash
python3 .claude/skills/content-studio/scripts/render.py studio/infographics/foo.html --preset portrait
```
Presets: `square` (1080×1080), `portrait` (1080×1350), `story` (1080×1920),
`landscape` (1200×630), `carousel` (1080×1350, multi-slide).

## Rules

- **Voice over polish.** A post that sounds like Danni beats a better-written
  post that doesn't. When they conflict, voice wins.
- **No auto-posting.** Nothing here publishes anywhere. Drafts get copied out by
  hand, deliberately. This is a feature — it is also why this skill can't get a
  cease-and-desist the way Kleo's scraper extension did.
- **No scraping LinkedIn.** Swipe entries are saved by paste, by hand. Do not
  write anything that fetches or parses a logged-in LinkedIn feed.
- **Ask before inventing facts.** Never fabricate revenue numbers, client
  results, testimonials, or specifics of Danni's life to make a post land. If a
  template needs a concrete detail, ask for it.
- **Files are the source of truth.** Don't hold state in conversation — write it
  down so the next session picks up where this one left off.
