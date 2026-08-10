# Voice profile

The single highest-leverage file in the studio. Every post depends on it.

A voice profile is **not** "friendly, professional, approachable." Those words
describe nothing and constrain nothing. A usable profile records habits specific
enough that a stranger could forge the writing.

## Building it from scratch

You need 5–10 real posts the user is happy with. Ask for them if they aren't in
`studio/voice/samples/`. If the user has never posted, ask them to voice-note or
free-write three answers to "what do you actually believe about X that most
people in your field don't" — unedited speech is closer to voice than edited
writing.

Save each raw sample to `studio/voice/samples/NN-slug.md` before analysing.

Then work through these dimensions **with evidence**. Every claim in the profile
needs a quote from the samples backing it. No quote, no rule.

1. **Sentence rhythm** — average length, and more importantly the *pattern*. Many
   strong voices run long-long-short. Count actual sentences; don't eyeball it.
2. **Opening move** — how do posts start? Question, flat declarative, number,
   scene, confession? Is there a consistent tic?
3. **Vocabulary** — words used repeatedly that others wouldn't. Also: register.
   Contractions or not? Swearing? Jargon, and which jargon?
4. **Punctuation habits** — em dashes, ellipses, one-line paragraphs, ALL CAPS,
   colons before a list. These are fingerprints.
5. **Point of view** — "I" vs "you" vs "we". Ratio matters. A voice that says
   "you" a lot reads as coaching; "I" a lot reads as memoir.
6. **Argument shape** — do they lead with the claim then justify, or walk you
   there and reveal? Do they concede the other side?
7. **Emotional register** — warm, blunt, wry, urgent. Where do they let heat in?
8. **Endings** — question to the reader, hard stop, CTA, callback to the hook?
9. **Formatting** — line-break density, emoji use (and *which*), lists vs prose.
10. **Never-does list** — the constraints. Often the most useful section. E.g.
    "never opens with a greeting", "never uses 'game-changer'", "never more than
    two emoji".

## The file format

Write to `studio/voice/voice-profile.md`:

```markdown
# Voice profile — <name>
_Derived from N samples. Last updated YYYY-MM-DD._

## In one line
<A sentence a ghostwriter could act on.>

## Rhythm
<Rule.> — e.g. "Sentences average 11 words. Opens with two short punches, then
one long sentence that carries the argument."
> "Quote from a sample showing it."

## Vocabulary
...
## Punctuation & formatting
...
## Point of view
...
## Argument shape
...
## Endings
...

## Never
- <constraint>
- <constraint>

## What has actually worked
<Filled in over time from calendar performance logs. Empty at first — that's fine.>
```

## Applying it

Before writing, read the profile and hold the **Never** list hardest — violations
there are what make a post feel "not mine" even when the reader can't say why.

After drafting, self-check against the profile line by line. If a draft breaks a
rule deliberately, say so and why, rather than silently drifting.

## Keeping it alive

The profile is a living file, not a one-time setup:

- When the user rewrites something you drafted, **diff their version against
  yours**. Their edits are the most reliable voice signal you will ever get.
  Fold the pattern in and note the date.
- When a post performs unusually well or badly, update *What has actually
  worked* from the calendar log — with the specific structural reason, not the
  topic.
- Re-derive from scratch roughly every 30 new posts. Voices drift.
