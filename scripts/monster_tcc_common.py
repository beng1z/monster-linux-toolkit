#!/usr/bin/env python3
from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path

DEST = "com.tuxedocomputers.tccd"
OBJECT_PATH = "/com/tuxedocomputers/tccd"
INTERFACE = "com.tuxedocomputers.tccd"

CONFIG_DIR = Path.home() / ".config" / "monster-tcc"
CONFIG_PATH = CONFIG_DIR / "cycle-order.json"


def _busctl_call(method: str, *signature_and_args: str) -> str:
    cmd = ["busctl", "--system", "call", DEST, OBJECT_PATH, INTERFACE, method, *signature_and_args]
    return subprocess.check_output(cmd, text=True).strip()


def _parse_single_string(output: str) -> str:
    parts = shlex.split(output)
    if len(parts) < 2 or parts[0] != "s":
        raise RuntimeError(f"Unexpected busctl output: {output}")
    return parts[1]


def _parse_single_bool(output: str) -> bool:
    parts = shlex.split(output)
    if len(parts) < 2 or parts[0] != "b":
        raise RuntimeError(f"Unexpected busctl output: {output}")
    return parts[1].lower() == "true"


def notify(summary: str, body: str) -> None:
    try:
        subprocess.run(["notify-send", summary, body], check=False)
    except FileNotFoundError:
        pass


def get_profiles() -> list[dict]:
    return json.loads(_parse_single_string(_busctl_call("GetProfilesJSON")))


def get_active_profile() -> dict:
    return json.loads(_parse_single_string(_busctl_call("GetActiveProfileJSON")))


def set_profile_by_id(profile_id: str) -> bool:
    return _parse_single_bool(_busctl_call("SetTempProfileById", "s", profile_id))


def _read_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text())


def _write_config(payload: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def merge_profiles_with_config(profiles: list[dict]) -> list[dict]:
    config = _read_config()
    configured_entries = config.get("profiles", [])
    by_id = {profile.get("id"): profile for profile in profiles if profile.get("id")}

    merged = []
    seen = set()

    for entry in configured_entries:
        profile_id = entry.get("id")
        profile = by_id.get(profile_id)
        if not profile or profile_id in seen:
            continue
        merged.append({
            "id": profile_id,
            "name": profile.get("name", profile_id),
            "description": profile.get("description", ""),
            "enabled": bool(entry.get("enabled", True)),
        })
        seen.add(profile_id)

    for profile in profiles:
        profile_id = profile.get("id")
        if not profile_id or profile_id in seen:
            continue
        merged.append({
            "id": profile_id,
            "name": profile.get("name", profile_id),
            "description": profile.get("description", ""),
            "enabled": True,
        })
        seen.add(profile_id)

    return merged


def load_cycle_profiles() -> list[dict]:
    return merge_profiles_with_config(get_profiles())


def save_cycle_profiles(entries: list[dict]) -> None:
    payload = {
        "profiles": [
            {
                "id": entry["id"],
                "enabled": bool(entry.get("enabled", True)),
            }
            for entry in entries
        ]
    }
    _write_config(payload)


def get_enabled_cycle_profiles() -> list[dict]:
    return [entry for entry in load_cycle_profiles() if entry.get("enabled", True)]


def cycle_to_next_profile() -> dict:
    profiles = get_enabled_cycle_profiles()
    active = get_active_profile()

    if not profiles:
        raise RuntimeError("No enabled profiles in cycle order")

    active_id = active.get("id")
    active_index = next((i for i, profile in enumerate(profiles) if profile.get("id") == active_id), -1)
    next_profile = profiles[(active_index + 1) % len(profiles)]
    next_id = next_profile.get("id")

    if not next_id:
        raise RuntimeError("Next profile has no id")
    if not set_profile_by_id(next_id):
        raise RuntimeError(f"Failed to switch to profile {next_id}")

    return next_profile
