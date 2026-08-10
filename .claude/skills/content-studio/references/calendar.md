# Content calendar

`studio/calendar/posts.json` is the pipeline. Every post moves through:

`idea` → `draft` → `ready` → `posted`

(`parked` exists for ideas deliberately shelved — better than deleting, since
parked ideas are the cheapest source of future posts.)

## Commands

Always get the real date first — never assume it:
```bash
date +%F
```

```bash
# What's coming up
python3 .claude/skills/content-studio/scripts/studio.py post list --upcoming

# Everything at a given stage
python3 .claude/skills/content-studio/scripts/studio.py post list --status draft

# Add
python3 .claude/skills/content-studio/scripts/studio.py post add \
  --title "What a missed call actually costs a tradie" \
  --date 2026-08-14 --platform linkedin --template 8 --hook number \
  --notes "receptionist ROI angle — pair with the 30s stat graphic"

# Move a stage
python3 .claude/skills/content-studio/scripts/studio.py post status 7 ready

# Log results after publishing (this is the part that compounds)
python3 .claude/skills/content-studio/scripts/studio.py post log 7 \
  --likes 143 --comments 22 --reposts 4 --note "carousel version outperformed text"

# Aggregate view
python3 .claude/skills/content-studio/scripts/studio.py stats
```

Setting a post to `posted` stamps `posted_at` automatically.

## Draft bodies

The JSON holds metadata only. Full text goes in `studio/drafts/<slug>.md`, which
`post add` links via the `draft` field. Keep them separate — it makes drafts
diffable in git and keeps the JSON readable.

## Cadence and mix

Don't let the calendar become a guilt machine. Two well-made posts a week beats
five thin ones, and a thin post trains the voice profile on the wrong data.

Common working numbers among people who've actually grown on LinkedIn — Lara
Acosta (Kleo's founder) among them — are **3–5 posts a week** on an **80/20
split: 80% educational, 20% personal or inspirational**. Treat that as a
starting shape to test, not a law. Danni's own logged performance overrides it
the moment there's enough data to say otherwise.

The 80/20 matters more than the frequency. All-educational reads as a
newsletter nobody subscribed to; all-personal gives the reader no reason to
follow. When planning a week, aim for a mix rather than five of the same
template: one selling post, one authority post, one connection post is a
healthy shape.

## Why logging matters

This is the loop that a subscription tool can't do for you and the reason the
studio gets better over time:

1. Log real numbers when the user reports them.
2. Run `stats` periodically to see which templates and hooks actually land.
3. Feed durable findings into the **What has actually worked** section of
   `studio/voice/voice-profile.md` — with the structural reason, not the topic.

Be honest about sample size. Three posts is an anecdote. Resist declaring a
pattern until it has shown up across roughly ten posts, and say so when the
data is still thin rather than presenting noise as insight.
