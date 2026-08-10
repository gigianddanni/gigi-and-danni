#!/usr/bin/env python3
"""Render an infographic HTML file to PNG using headless Chromium.

    python3 render.py studio/infographics/foo.html --preset portrait
    python3 render.py studio/infographics/deck.html --preset carousel

Carousel mode renders one PNG per `<section class="slide">`.
No dependencies beyond a Chromium/Chrome binary.
"""
from __future__ import annotations

import argparse
import glob
import os
import platform
import re
import shutil
import subprocess
import sys

PRESETS = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "story": (1080, 1920),
    "landscape": (1200, 630),
    "carousel": (1080, 1350),
}

# Pin the canvas to exact pixels.
#
# Two headless quirks make this necessary. The screenshot is exactly
# --window-size, but window.innerHeight is smaller (1263 vs 1350 at the time of
# writing), so a 100vh canvas leaves an unpainted strip along the bottom. And
# `overflow: hidden` on html/body clips the document back to that short
# viewport, which reintroduces the strip — so it is deliberately not set here.
# Clipping belongs on .canvas/.slide, which carry an exact height.
SIZE_CSS = """
<style>
  html, body { width: __W__px !important; height: __H__px !important;
               margin: 0 !important; }
  .canvas, .slide { width: __W__px !important; height: __H__px !important;
                    overflow: hidden !important; }
</style>
"""

# Injected per slide so only that slide survives to the screenshot.
SLIDE_JS = """
<script>
(function () {
  var keep = __INDEX__;
  var run = function () {
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    slides.forEach(function (el, i) {
      if (i !== keep && el.parentNode) el.parentNode.removeChild(el);
    });
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
</script>
"""


def find_chromium() -> tuple[str, bool]:
    """Locate a browser binary. Returns (path, is_headless_shell).

    chrome-headless-shell is strongly preferred. In it the viewport equals
    --window-size exactly, so the screenshot is fully painted. Regular Chrome's
    new headless mode reserves ~87 CSS px of window chrome, so the viewport is
    shorter than the screenshot buffer and an unpainted strip is left along the
    bottom edge. Everything still renders, it just needs trimming afterwards.
    """
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or "/opt/pw-browsers",
             os.path.expanduser("~/.cache/ms-playwright")]

    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env, "headless_shell" in env or "headless-shell" in env

    shell_patterns = ["*headless_shell*/chrome-linux/headless_shell",
                      "*headless_shell*/chrome-mac/chrome-headless-shell",
                      "*headless-shell*/**/chrome-headless-shell"]
    for root in roots:
        for pat in shell_patterns:
            hits = sorted(glob.glob(os.path.join(root, pat), recursive=True))
            if hits:
                return hits[-1], True
    for name in ("chrome-headless-shell", "headless_shell"):
        found = shutil.which(name)
        if found:
            return found, True

    full_patterns = ["chromium-*/chrome-linux/chrome",
                     "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
                     "chromium/chrome-linux/chrome"]
    for root in roots:
        for pat in full_patterns:
            hits = sorted(glob.glob(os.path.join(root, pat)))
            if hits:
                return hits[-1], False

    for name in ("chromium", "chromium-browser", "google-chrome",
                 "google-chrome-stable", "chrome"):
        found = shutil.which(name)
        if found:
            return found, False

    if platform.system() == "Darwin":
        for app in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Chromium.app/Contents/MacOS/Chromium"):
            if os.path.exists(app):
                return app, False

    sys.exit("No Chromium/Chrome binary found. Set CHROME_PATH to point at one, "
             "or install chrome-headless-shell (npx playwright install "
             "chromium-headless-shell).")


def count_slides(html: str) -> int:
    """Count real slide sections.

    Comments are stripped first so that commented-out slides — and prose that
    merely mentions `<section class="slide">`, as the starter template does —
    don't inflate the count and produce blank trailing PNGs. This matches what
    querySelectorAll('.slide') sees at render time.
    """
    without_comments = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    return len(re.findall(r"""<section[^>]*\bclass\s*=\s*["'][^"']*\bslide\b""",
                          without_comments, re.I))


def inject(html: str, snippet: str) -> str:
    """Insert a snippet just before </body>, falling back to appending."""
    match = re.search(r"</body\s*>", html, re.I)
    if match:
        return html[: match.start()] + snippet + html[match.start():]
    return html + snippet


def prepare(html: str, src_path: str, size: tuple[int, int],
            slide_index: int | None, suffix: str) -> str:
    """Write a temp copy beside the source so relative asset paths still work."""
    payload = SIZE_CSS.replace("__W__", str(size[0])).replace("__H__", str(size[1]))
    if slide_index is not None:
        payload += SLIDE_JS.replace("__INDEX__", str(slide_index))
    directory = os.path.dirname(os.path.abspath(src_path)) or "."
    tmp = os.path.join(directory, f".render-{suffix}.tmp.html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(inject(html, payload))
    return tmp


def shoot(chrome: str, html_path: str, out_path: str, size: tuple[int, int],
          scale: int) -> None:
    width, height = size
    cmd = [
        chrome,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        f"--force-device-scale-factor={scale}",
        f"--window-size={width},{height}",
        "--virtual-time-budget=5000",
        f"--screenshot={out_path}",
        f"file://{os.path.abspath(html_path)}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
        sys.exit("Chromium produced no image.\n"
                 f"exit={proc.returncode}\n{proc.stderr[-2000:]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="path to the source HTML file")
    ap.add_argument("--preset", default="portrait", choices=sorted(PRESETS))
    ap.add_argument("--out", help="output PNG path (default: alongside the HTML)")
    ap.add_argument("--scale", type=int, default=2,
                    help="device pixel ratio, default 2 for retina-sharp text")
    args = ap.parse_args()

    if not os.path.exists(args.html):
        sys.exit(f"No such file: {args.html}")

    chrome, is_shell = find_chromium()
    if not is_shell:
        print("warning: using full Chrome — its headless mode reserves window "
              "chrome, so the bottom ~87px of each PNG may be unpainted.\n"
              "         Install the shell for exact output: "
              "npx playwright install chromium-headless-shell",
              file=sys.stderr)
    size = PRESETS[args.preset]
    html = open(args.html, encoding="utf-8").read()
    base = args.out[:-4] if args.out and args.out.endswith(".png") else \
        (args.out or os.path.splitext(args.html)[0])

    if args.preset != "carousel":
        out = base + ".png"
        src = prepare(html, args.html, size, None, "single")
        try:
            shoot(chrome, src, out, size, args.scale)
        finally:
            if os.path.exists(src):
                os.remove(src)
        print(f"{out}  {size[0] * args.scale}x{size[1] * args.scale}")
        return

    slides = count_slides(html)
    if slides == 0:
        sys.exit("Carousel preset needs at least one <section class=\"slide\">.")

    written = []
    for i in range(slides):
        src = prepare(html, args.html, size, i, f"slide-{i}")
        out = f"{base}-{i + 1:02d}.png"
        try:
            shoot(chrome, src, out, size, args.scale)
        finally:
            if os.path.exists(src):
                os.remove(src)
        written.append(out)

    for path in written:
        print(f"{path}  {size[0] * args.scale}x{size[1] * args.scale}")
    print(f"{len(written)} slides")


if __name__ == "__main__":
    main()
