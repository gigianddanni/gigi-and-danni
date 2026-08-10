#!/usr/bin/env python3
"""One-off: build a self-contained brand CSS with base64 woff2 fonts."""
import base64, re, urllib.request, sys

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
URL = ("https://fonts.googleapis.com/css2?"
       "family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;600&display=swap")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


css = get(URL)

# Split into (preceding-subset-comment, @font-face block) pairs.
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
out = []
seen = set()
for subset, block in blocks:
    if subset != "latin":
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
    key = (fam, weight)
    if key in seen:
        continue
    seen.add(key)
    src = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    b64 = base64.b64encode(get(src, binary=True)).decode("ascii")
    out.append(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
        "font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}"
        % (fam, weight, b64)
    )
    print(f"embedded {fam} {weight} ({len(b64)//1024} KB b64)", file=sys.stderr)

if len(out) < 5:
    sys.exit(f"expected 5 faces, got {len(out)}")

header = ("/* Gigi & Danni brand fonts — Space Grotesk + Inter, latin subset,\n"
          "   embedded as base64 so infographic rendering works with no network.\n"
          "   Regenerate with .claude/skills/content-studio/scripts/embed_fonts.py */\n")
print(header + "\n".join(out))
