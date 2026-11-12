#!/usr/bin/env python3
"""Push an engagement pack (engage/<date>.md) to the phone via ntfy.
One notification per comment: tap opens the post, the body is the comment to copy.
One notification for connects (tap opens the first profile; all profile links in the body).
Usage: ntfy_pack.py engage/<date>.md [--dry-run]"""
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPIC = json.loads((ROOT / "config.json").read_text())["ntfy_topic"]
URL_RE = r"https?://\S+"


def push(title, body, click=None, prio="default", dry=False):
    if dry:
        print(f"--- {title}\n{body}\n[click] {click}\n"); return
    h = {"Title": title.encode("utf-8"), "Priority": prio, "Tags": "speech_balloon"}
    if click:
        h["Click"] = click
    req = urllib.request.Request(f"https://ntfy.sh/{TOPIC}", data=body.encode("utf-8"), headers=h, method="POST")
    urllib.request.urlopen(req, timeout=20).read()
    time.sleep(1)


def parse(md):
    sec, comments, connects, replies = None, [], [], []
    for line in md.splitlines():
        if line.startswith("## "):
            sec = line[3:].strip().lower(); continue
        if sec and sec.startswith("comments"):
            m = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
            if m:
                comments.append({"head": m.group(2), "url": (re.findall(URL_RE, m.group(2)) or [None])[-1], "text": ""})
            elif line.strip().lower().startswith("comment:") and comments:
                comments[-1]["text"] = line.split(":", 1)[1].strip()
        elif sec and sec.startswith("connects"):
            m = re.match(r"^\s*\d+\.\s+(.*)$", line)
            if m:
                connects.append(m.group(1))
        elif sec and sec.startswith("replies") and line.strip():
            replies.append(line.strip())
    return comments, connects, replies


def main():
    path = Path(sys.argv[1]); dry = "--dry-run" in sys.argv
    comments, connects, replies = parse(path.read_text())
    date = path.stem
    push(f"LinkedIn pack {date}", f"{len(comments)} comments + {len(connects)} connects ready. Tap each one, paste, post. "
         "Or tell Claude on the Mac: post the pack.", dry=dry)
    for i, c in enumerate(comments, 1):
        who = re.split(r"\s\|\s", c["head"])[0]
        push(f"Comment {i}/{len(comments)}: {who}"[:120], c["text"], click=c["url"], dry=dry)
    if connects:
        first = (re.findall(URL_RE, connects[0]) or [None])[0]
        push(f"Connects {date}", "\n".join(connects), click=first, dry=dry)
    if replies:
        push(f"Replies on your post {date}", "\n".join(replies), dry=dry)
    print(f"pushed {len(comments)} comments, {len(connects)} connects, {len(replies)} reply lines")


if __name__ == "__main__":
    main()
