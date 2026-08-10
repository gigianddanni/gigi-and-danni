# Swipe file

Kleo's research feature scraped LinkedIn to surface top creators' best posts.
That is exactly what got its extension a cease-and-desist in 2025. This does the
same job legally: the user pastes what they already saw, and the studio keeps the
part that's actually reusable.

## What makes an entry worth saving

A swipe entry is worthless as a copy of someone's words. It's valuable as a
**captured mechanism**. The `--why` field is the entry; the text is just evidence.

Good `--why`:
- "Opens with a number that contradicts the reader's assumption, then spends the
  whole post earning it back."
- "Lists four failures before the win, so the win reads as earned rather than
  boastful."
- "Second person the entire way through — never says 'I' once, so it reads as
  advice rather than a flex."

Useless `--why`:
- "Great hook" / "Really good post" / "Went viral"

If you can't articulate a transferable mechanism, ask the user what made them
stop scrolling. Their answer usually *is* the mechanism.

## Saving

```bash
python3 .claude/skills/content-studio/scripts/studio.py swipe add \
  --author "Jane Doe" \
  --url "https://..." \
  --text "full post text" \
  --why "opens with a concession, which buys permission for the strong claim" \
  --tags hook,contrarian,story
```

`--url` and `--author` are optional but worth keeping — attribution matters if a
post ever gets referenced publicly.

## Tag vocabulary

Keep tags few and structural, so they stay searchable. Prefer:

`hook` `story` `contrarian` `listicle` `teardown` `data` `vulnerability`
`case-study` `offer` `objection` `carousel` `format`

Add a topic tag only when it's genuinely a topic the user posts about often.

## Retrieving

```bash
python3 .claude/skills/content-studio/scripts/studio.py swipe list --tag hook
python3 .claude/skills/content-studio/scripts/studio.py swipe list --search "pricing"
```

When drafting a post, pull relevant swipes and **use the mechanism, never the
words**. Borrowing structure is craft; borrowing sentences is plagiarism and will
read as off-voice anyway.

If a mechanism keeps proving useful, promote it into
`references/templates.md` as a named template so it stops being a lookup.
