#!/usr/bin/env python3
"""Minimal Buffer GraphQL client (https://api.buffer.com).

Auth: in the cloud routine, the environment's network secret adds
`Authorization: Bearer <key>` to requests for api.buffer.com, so no key is
needed here. Locally, set BUFFER_API_KEY.

Commands:
  python3 scripts/buffer.py orgs
  python3 scripts/buffer.py channels <organizationId>
  python3 scripts/buffer.py scheduled <organizationId>          # upcoming posts
  python3 scripts/buffer.py schedule <post.json>               # create a scheduled post

post.json:
  {"channel_id": "...", "text": "...", "image_url": "https://...png",
   # or "document_url": "https://...pdf", "document_title": "...", "thumbnail_url": "https://...png"  (carousel)
   # or "video_url": "https://...mp4", "thumbnail_url": "..."                                       (video)
   "first_comment": "...", "due_at": "2026-11-12T06:00:00.000Z",
   "annotations": [ {id, entity, length, link, localizedName, start, vanityName} ]  # optional company tags
  }
Buffer returns errors inside HTTP 200 (MutationError.message), so this script
checks the body and exits non-zero on any error.
"""
import json, os, sys, urllib.request

API = "https://api.buffer.com"


def gql(query, variables=None):
    headers = {"Content-Type": "application/json"}
    if os.environ.get("BUFFER_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["BUFFER_API_KEY"]
    req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read())
    if body.get("errors"):
        sys.exit("GraphQL error: " + json.dumps(body["errors"]))
    return body["data"]


def orgs():
    print(json.dumps(gql("query { account { organizations { id name } } }"), indent=2))


def channels(org):
    q = "query($o: OrganizationId!){ channels(input:{organizationId:$o}){ id name service type } }"
    print(json.dumps(gql(q, {"o": org}), indent=2))


def delete(post_id):
    q = """mutation($i: DeletePostInput!){ deletePost(input:$i){ __typename ... on MutationError { message } } }"""
    print(json.dumps(gql(q, {"i": {"id": post_id}}), indent=2))


def scheduled(org):
    q = """query($o: OrganizationId!){ posts(first: 20, input:{organizationId:$o, filter:{status:[scheduled]},
           sort:[{field: dueAt, direction: asc}]}){ edges{ node{ id text dueAt status } } } }"""
    print(json.dumps(gql(q, {"o": org}), indent=2))


def schedule(path):
    p = json.load(open(path))
    for k in ("channel_id", "text", "due_at"):
        if not p.get(k):
            sys.exit(f"post.json missing {k}")
    if len(p["text"]) > 3000:
        sys.exit("text over LinkedIn 3000 limit")
    li = {}
    if p.get("first_comment"):
        if len(p["first_comment"]) > 1250:
            sys.exit("first comment over 1250 limit")
        li["firstComment"] = p["first_comment"]
    if p.get("annotations"):
        li["annotations"] = p["annotations"]
    inp = {"text": p["text"], "channelId": p["channel_id"], "schedulingType": "automatic",
           "mode": "customScheduled", "dueAt": p["due_at"]}
    if p.get("draft"):
        inp["saveToDraft"] = True
    inp["aiAssisted"] = True
    if p.get("document_url"):   # carousel = PDF document post
        inp["assets"] = [{"document": {"url": p["document_url"], "title": p.get("document_title", "")[:58],
                                       **({"thumbnailUrl": p["thumbnail_url"]} if p.get("thumbnail_url") else {})}}]
    elif p.get("video_url"):
        inp["assets"] = [{"video": {"url": p["video_url"],
                                    **({"thumbnailUrl": p["thumbnail_url"]} if p.get("thumbnail_url") else {})}}]
    elif p.get("image_url"):
        inp["assets"] = [{"image": {"url": p["image_url"]}}]
    if li:
        inp["metadata"] = {"linkedin": li}
    q = """mutation($i: CreatePostInput!){ createPost(input:$i){
             ... on PostActionSuccess { post { id dueAt status } }
             ... on MutationError { message } } }"""
    res = gql(q, {"i": inp})["createPost"]
    if "message" in res:
        sys.exit("Buffer rejected the post: " + res["message"])
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["help"]
    {"orgs": orgs, "channels": channels, "scheduled": scheduled, "schedule": schedule, "delete": delete}.get(
        cmd, lambda *a: sys.exit(__doc__))(*args)
