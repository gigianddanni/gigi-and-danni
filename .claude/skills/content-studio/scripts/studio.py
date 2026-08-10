#!/usr/bin/env python3
"""Content Studio store — swipe file and content calendar.

Keeps studio/swipe/swipes.json and studio/calendar/posts.json consistent so
they can be edited by command rather than by hand-patching JSON.

    studio.py swipe add --author X --text "..." --why "..." --tags hook,story
    studio.py swipe list [--tag hook] [--search pricing]
    studio.py post add --title "..." --date 2026-08-14 --platform linkedin
    studio.py post list [--status draft] [--upcoming]
    studio.py post status <id> ready
    studio.py post log <id> --likes 120 --comments 14
    studio.py stats
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import textwrap

STATUSES = ("idea", "draft", "ready", "posted", "parked")


def repo_root() -> str:
    path = os.path.abspath(os.path.dirname(__file__))
    while path != "/":
        if os.path.isdir(os.path.join(path, ".git")) or \
           os.path.isdir(os.path.join(path, "studio")):
            return path
        path = os.path.dirname(path)
    return os.getcwd()


ROOT = repo_root()
SWIPES = os.path.join(ROOT, "studio", "swipe", "swipes.json")
POSTS = os.path.join(ROOT, "studio", "calendar", "posts.json")


def load(path: str, key: str) -> dict:
    if not os.path.exists(path):
        return {key: []}
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        sys.exit(f"{path} is not valid JSON ({exc}). Fix it before continuing "
                 f"— refusing to overwrite and lose data.")
    data.setdefault(key, [])
    return data


def save(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def next_id(items: list) -> int:
    return max((int(i.get("id", 0)) for i in items), default=0) + 1


def today() -> str:
    return dt.date.today().isoformat()


def parse_tags(raw: str | None) -> list:
    return [t.strip().lower() for t in (raw or "").split(",") if t.strip()]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "untitled"


def check_date(value: str) -> str:
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        sys.exit(f"--date must be YYYY-MM-DD, got {value!r}")
    return value


def wrap(text: str, width: int = 76, indent: str = "     ") -> str:
    flat = " ".join(text.split())
    return textwrap.fill(flat, width=width, initial_indent=indent,
                         subsequent_indent=indent)


# --------------------------------------------------------------------- swipe

def swipe_add(args) -> None:
    data = load(SWIPES, "swipes")
    text = args.text
    if text == "-":
        text = sys.stdin.read()
    entry = {
        "id": next_id(data["swipes"]),
        "author": args.author or "unknown",
        "url": args.url or "",
        "text": text.strip(),
        "why": args.why.strip(),
        "tags": parse_tags(args.tags),
        "saved_at": today(),
    }
    data["swipes"].append(entry)
    save(SWIPES, data)
    print(f"saved swipe #{entry['id']} — {entry['author']} "
          f"[{', '.join(entry['tags']) or 'untagged'}]")


def swipe_list(args) -> None:
    items = load(SWIPES, "swipes")["swipes"]
    if args.tag:
        items = [s for s in items if args.tag.lower() in s.get("tags", [])]
    if args.search:
        needle = args.search.lower()
        items = [s for s in items
                 if needle in (s.get("text", "") + s.get("why", "") +
                               s.get("author", "")).lower()]
    if not items:
        print("no matching swipes")
        return
    for s in items:
        print(f"\n#{s['id']}  {s['author']}  [{', '.join(s.get('tags', []))}]  "
              f"{s.get('saved_at', '')}")
        if s.get("url"):
            print(f"     {s['url']}")
        print(textwrap.fill(" ".join(s["why"].split()), width=76,
                            initial_indent="  WHY ", subsequent_indent="      "))
        if args.full and s.get("text"):
            print(wrap(s["text"], indent="      "))
    print(f"\n{len(items)} swipe(s)")


# ---------------------------------------------------------------------- post

def post_add(args) -> None:
    data = load(POSTS, "posts")
    entry = {
        "id": next_id(data["posts"]),
        "title": args.title,
        "date": check_date(args.date) if args.date else "",
        "platform": args.platform,
        "status": args.status,
        "template": args.template or "",
        "hook": args.hook or "",
        "notes": args.notes or "",
        "draft": f"studio/drafts/{slugify(args.title)}.md",
        "created_at": today(),
        "posted_at": "",
        "metrics": {},
    }
    data["posts"].append(entry)
    save(POSTS, data)
    print(f"added post #{entry['id']} — {entry['title']} "
          f"({entry['status']}, {entry['date'] or 'no date'})")
    print(f"draft file: {entry['draft']}")


def find_post(data: dict, post_id: int) -> dict:
    for p in data["posts"]:
        if int(p["id"]) == post_id:
            return p
    sys.exit(f"no post with id {post_id}")


def post_status(args) -> None:
    data = load(POSTS, "posts")
    post = find_post(data, args.id)
    post["status"] = args.new_status
    if args.new_status == "posted" and not post.get("posted_at"):
        post["posted_at"] = today()
    save(POSTS, data)
    print(f"#{post['id']} {post['title']} → {args.new_status}"
          + (f" (posted {post['posted_at']})" if post.get("posted_at") else ""))


def post_log(args) -> None:
    data = load(POSTS, "posts")
    post = find_post(data, args.id)
    metrics = post.setdefault("metrics", {})
    for field in ("likes", "comments", "reposts", "views"):
        value = getattr(args, field)
        if value is not None:
            metrics[field] = value
    if args.note:
        metrics["note"] = args.note
    metrics["logged_at"] = today()
    if post.get("status") != "posted":
        post["status"] = "posted"
        post.setdefault("posted_at", today())
    save(POSTS, data)
    print(f"logged #{post['id']} {post['title']}: "
          + ", ".join(f"{k}={v}" for k, v in metrics.items()
                      if k not in ("note", "logged_at")))


def post_list(args) -> None:
    items = load(POSTS, "posts")["posts"]
    if args.status:
        items = [p for p in items if p.get("status") == args.status]
    if args.upcoming:
        now = today()
        items = [p for p in items
                 if p.get("status") != "posted" and
                 (not p.get("date") or p["date"] >= now)]
    items.sort(key=lambda p: (p.get("date") or "9999-99-99", int(p["id"])))
    if not items:
        print("nothing matches")
        return
    for p in items:
        metrics = p.get("metrics") or {}
        engagement = ""
        if metrics:
            engagement = "  " + " ".join(
                f"{k[0]}{v}" for k, v in metrics.items()
                if k in ("likes", "comments", "reposts"))
        print(f"#{p['id']:<3} {p.get('date') or '————-——-——':<10} "
              f"{p.get('status', ''):<7} {p.get('platform', ''):<9} "
              f"{p['title']}{engagement}")
        if args.verbose and p.get("notes"):
            print(wrap(p["notes"], indent="       "))
    print(f"\n{len(items)} post(s)")


def stats(args) -> None:
    posts = load(POSTS, "posts")["posts"]
    swipes = load(SWIPES, "swipes")["swipes"]

    by_status = {}
    for p in posts:
        by_status[p.get("status", "?")] = by_status.get(p.get("status", "?"), 0) + 1

    print("PIPELINE")
    for status in STATUSES:
        if by_status.get(status):
            print(f"  {status:<7} {by_status[status]}")
    print(f"  {'total':<7} {len(posts)}")
    print(f"\nSWIPE FILE: {len(swipes)} saved")

    posted = [p for p in posts if (p.get("metrics") or {}).get("likes") is not None]
    if not posted:
        print("\nNo performance logged yet — log results with `post log <id>` "
              "so the studio can learn what works.")
        return

    def engagement(p):
        m = p.get("metrics", {})
        return sum(m.get(k, 0) for k in ("likes", "comments", "reposts"))

    print(f"\nPERFORMANCE ({len(posted)} logged)")
    avg = sum(engagement(p) for p in posted) / len(posted)
    print(f"  average engagement: {avg:.0f}")

    for label, field in (("template", "template"), ("hook", "hook")):
        groups = {}
        for p in posted:
            key = p.get(field) or "—"
            groups.setdefault(key, []).append(engagement(p))
        if len(groups) > 1:
            print(f"\n  by {label}:")
            for key, values in sorted(groups.items(),
                                      key=lambda kv: -sum(kv[1]) / len(kv[1])):
                print(f"    {key:<14} {sum(values) / len(values):>7.0f} avg "
                      f"(n={len(values)})")

    if len(posted) < 10:
        noun = "post" if len(posted) == 1 else "posts"
        print(f"\n  Only {len(posted)} logged {noun} — treat these as anecdotes, "
              "not patterns.")

    print("\n  Top 3:")
    for p in sorted(posted, key=engagement, reverse=True)[:3]:
        print(f"    {engagement(p):>5}  #{p['id']} {p['title']}")


# ---------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sw = sub.add_parser("swipe", help="inspiration library").add_subparsers(
        dest="sub", required=True)

    a = sw.add_parser("add", help="save a post as inspiration")
    a.add_argument("--text", required=True, help="post text, or - for stdin")
    a.add_argument("--why", required=True,
                   help="the transferable mechanism — not 'good post'")
    a.add_argument("--author")
    a.add_argument("--url")
    a.add_argument("--tags", help="comma separated")
    a.set_defaults(func=swipe_add)

    l = sw.add_parser("list", help="browse saved inspiration")
    l.add_argument("--tag")
    l.add_argument("--search")
    l.add_argument("--full", action="store_true", help="include full post text")
    l.set_defaults(func=swipe_list)

    po = sub.add_parser("post", help="content calendar").add_subparsers(
        dest="sub", required=True)

    pa = po.add_parser("add", help="add a post to the calendar")
    pa.add_argument("--title", required=True)
    pa.add_argument("--date", help="YYYY-MM-DD")
    pa.add_argument("--platform", default="linkedin")
    pa.add_argument("--status", default="idea", choices=STATUSES)
    pa.add_argument("--template", help="template number or name")
    pa.add_argument("--hook", help="hook category used")
    pa.add_argument("--notes")
    pa.set_defaults(func=post_add)

    pl = po.add_parser("list", help="show the pipeline")
    pl.add_argument("--status", choices=STATUSES)
    pl.add_argument("--upcoming", action="store_true",
                    help="unposted, dated today or later")
    pl.add_argument("--verbose", "-v", action="store_true")
    pl.set_defaults(func=post_list)

    ps = po.add_parser("status", help="move a post through the pipeline")
    ps.add_argument("id", type=int)
    ps.add_argument("new_status", choices=STATUSES)
    ps.set_defaults(func=post_status)

    pg = po.add_parser("log", help="record how a post performed")
    pg.add_argument("id", type=int)
    pg.add_argument("--likes", type=int)
    pg.add_argument("--comments", type=int)
    pg.add_argument("--reposts", type=int)
    pg.add_argument("--views", type=int)
    pg.add_argument("--note")
    pg.set_defaults(func=post_log)

    st = sub.add_parser("stats", help="pipeline and performance overview")
    st.set_defaults(func=stats)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
