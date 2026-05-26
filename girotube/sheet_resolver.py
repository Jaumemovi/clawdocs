"""
Helpers to make the Girotube YouTube sync use the Google Sheet as the
single source of truth for playlist IDs, and to refuse to write when
the OAuth token belongs to the wrong YouTube account.

Drop this file into ~/.openclaw/workspace/ and import from the cron:

    from sheet_resolver import (
        load_canonical_playlists,
        load_config,
        assert_youtube_owner,
        WrongYoutubeAccountError,
    )

Requires gspread, google-auth, google-api-python-client (already used).
"""
from __future__ import annotations

import os
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "1p_VAArPDYneFkDFk8qsyhz7-LXXUnvagPJRp6zoxrj4"
SHEET_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class WrongYoutubeAccountError(RuntimeError):
    """Raised when the OAuth token does not belong to the expected channel."""


def _open(sa_credentials_path: Optional[str] = None):
    path = sa_credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS not set and no path passed. "
            "Point it at the Service Account JSON used to read the Sheet."
        )
    creds = Credentials.from_service_account_file(path, scopes=SHEET_SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def load_canonical_playlists(sa_credentials_path: Optional[str] = None) -> dict:
    """Return {playlist_name: youtube_playlist_id} from the 'Playlists' tab.

    Rows without a YouTube playlist ID (e.g. Ciència, pending creation)
    are omitted, so callers can detect missing IDs by `name not in result`.
    """
    rows = _open(sa_credentials_path).worksheet("Playlists").get_all_records()
    out = {}
    for r in rows:
        name = (r.get("Playlist") or "").strip()
        pid = (r.get("YouTube playlist ID") or "").strip()
        if name and pid:
            out[name] = pid
    return out


def load_config(sa_credentials_path: Optional[str] = None) -> dict:
    """Return the Config tab as {clau: valor}."""
    rows = _open(sa_credentials_path).worksheet("Config").get_all_records()
    return {
        (r.get("Clau") or "").strip(): (r.get("Valor") or "").strip()
        for r in rows
        if r.get("Clau")
    }


def assert_youtube_owner(youtube_service, expected_channel_id: str) -> str:
    """Verify the OAuth token belongs to `expected_channel_id`.

    Calls channels().list(mine=True). Returns the actual channel id on
    success; raises WrongYoutubeAccountError otherwise. The cron should
    call this once, right after building the YouTube service, before any
    write (insert/delete/update).
    """
    resp = youtube_service.channels().list(part="id,snippet", mine=True).execute()
    items = resp.get("items") or []
    if not items:
        raise WrongYoutubeAccountError(
            "YouTube API returned no channel for the current OAuth token."
        )
    actual = items[0]["id"]
    title = items[0].get("snippet", {}).get("title", "?")
    if actual != expected_channel_id:
        raise WrongYoutubeAccountError(
            f"OAuth token belongs to channel {actual} ({title!r}), "
            f"expected {expected_channel_id}. "
            f"Re-authorize with the correct YouTube account before running the sync."
        )
    return actual
