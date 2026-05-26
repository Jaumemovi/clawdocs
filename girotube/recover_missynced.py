"""
Re-add videos that the approved_only_sync mistakenly wrote to the wrong
account's playlists (PLzPacBemLhu...). Reads ../recovery/recovery_list.json
and inserts each video into the canonical playlist (PLcc...).

Run this ONCE, after re-authorizing the OAuth token with the YouTube
account that owns the canonical PLcc... playlists.

    python recover_missynced.py ../recovery/recovery_list.json --dry-run
    python recover_missynced.py ../recovery/recovery_list.json --skip-news

Requires the Config tab in the Sheet to have a key
`youtube_owner_channel_id` set to the channel ID (UC...) that owns
the canonical playlists. The script refuses to run otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sheet_resolver import (
    WrongYoutubeAccountError,
    assert_youtube_owner,
    load_canonical_playlists,
    load_config,
)


def _load_youtube_oauth_credentials():
    """Reuse the cron's existing OAuth loader."""
    from youtube_api import load_credentials  # type: ignore
    return load_credentials(interactive=False)


def playlist_contains(youtube, playlist_id: str, video_id: str) -> bool:
    page_token = None
    while True:
        resp = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        ).execute()
        for it in resp.get("items", []):
            if it.get("contentDetails", {}).get("videoId") == video_id:
                return True
        page_token = resp.get("nextPageToken")
        if not page_token:
            return False


def add_video(youtube, playlist_id: str, video_id: str) -> None:
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    ).execute()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("recovery_json", type=Path)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be added, write nothing.")
    ap.add_argument("--skip-news", action="store_true",
                    help="Skip Notícies (those are stale replaced_today entries).")
    args = ap.parse_args()

    data = json.loads(args.recovery_json.read_text())

    cfg = load_config()
    owner = cfg.get("youtube_owner_channel_id")
    if not owner:
        print(
            "FATAL: Config!youtube_owner_channel_id is empty. "
            "Add a row to the Config tab with Clau=youtube_owner_channel_id "
            "and Valor=<your UC... channel ID> before running.",
            file=sys.stderr,
        )
        return 2

    creds = _load_youtube_oauth_credentials()
    youtube = build("youtube", "v3", credentials=creds)
    try:
        assert_youtube_owner(youtube, owner)
    except WrongYoutubeAccountError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 3
    print(f"OAuth OK: writing as channel {owner}\n")

    canon = load_canonical_playlists()

    added = present = failed = 0
    for pl_name, info in data.items():
        if args.skip_news and pl_name.lower().startswith("not"):
            print(f"-- Skipping {pl_name} (--skip-news)")
            continue
        target = info.get("canonical_playlist_id") or canon.get(pl_name)
        if not target:
            print(f"!! No target playlist ID for {pl_name}, skipping")
            continue
        print(f"[{pl_name}] target={target}  candidates={info['count']}")
        for v in info["videos_to_readd"]:
            vid = v["video_id"]
            title = (v.get("title") or "")[:70]
            if args.dry_run:
                print(f"  DRY  add {vid}  {title}")
                continue
            try:
                if playlist_contains(youtube, target, vid):
                    print(f"  skip {vid} (already in playlist)")
                    present += 1
                    continue
                add_video(youtube, target, vid)
                print(f"  add  {vid}  {title}")
                added += 1
                time.sleep(0.5)
            except HttpError as exc:
                print(f"  FAIL {vid}: {exc}")
                failed += 1
        print()

    print(f"Done. added={added} already_present={present} failed={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
