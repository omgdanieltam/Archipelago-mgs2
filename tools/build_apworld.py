"""Package worlds/mgs2/ as a distributable mgs2.apworld.

Lives in tools/ of the Archipelago fork. An .apworld is a zip whose entries are
paths relative to `worlds/`, so the world folder name is the top-level directory
inside the archive. The manifest is rewritten during packaging to add the
container-format fields the loader requires (worlds/Files.py, worlds/__init__.py).

Usage (from the repo root):

    python tools/build_apworld.py                      # -> dist/mgs2.apworld
    python tools/build_apworld.py --expect 0.0.3       # also fail unless both version fields say 0.0.3
    python tools/build_apworld.py --check-only --expect 0.0.3
    python tools/build_apworld.py --print-version     # just the version (fails if the two fields differ)

Deliberately NOT setting maximum_ap_version: a world distributed on its own wants
to keep working across AP updates, and the loader refuses anything whose
maximum_ap_version is below the running core.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile

AP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # tools -> repo root
WORLD_NAME = "mgs2"
WORLD_DIR = os.path.join(AP_ROOT, "worlds", WORLD_NAME)
MANIFEST_PATH = os.path.join(WORLD_DIR, "archipelago.json")
CONFIG_PATH = os.path.join(WORLD_DIR, "Config", "Config.py")

# The container format version this archive claims (APWorldContainer); the loader
# rejects anything higher than its handler.
COMPATIBLE_VERSION = 7

SKIP_DIRS = {"__pycache__", ".git", ".idea", ".vscode"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".orig", ".rej", ".log")
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_RELATIVE = {"mgs2_spawn_catalogue.md"}   # development-only files


def read_versions() -> tuple[str, str]:
    """(archipelago.json world_version, Config.APWORLD_VERSION)."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest_version = json.load(f).get("world_version", "")
    with open(CONFIG_PATH, encoding="utf-8-sig") as f:
        match = re.search(r'^APWORLD_VERSION\s*=\s*["\']([^"\']+)["\']', f.read(), re.M)
    return manifest_version, match.group(1) if match else ""


def check_versions(expect: str | None) -> str:
    manifest_version, config_version = read_versions()
    problems = []
    if not manifest_version:
        problems.append("archipelago.json has no world_version")
    if not config_version:
        problems.append("Config/Config.py has no APWORLD_VERSION")
    if manifest_version and config_version and manifest_version != config_version:
        problems.append(f"archipelago.json says {manifest_version} but Config.py says {config_version}")
    if expect is not None and (manifest_version != expect or config_version != expect):
        problems.append(f"expected {expect}; bump both files and commit before releasing")
    if problems:
        raise SystemExit("version check failed:\n  " + "\n  ".join(problems))
    print(f"version {config_version}: archipelago.json and Config.py agree")
    return config_version


def should_skip(relative_path: str, filename: str) -> bool:
    if filename in SKIP_NAMES or filename.endswith(SKIP_SUFFIXES):
        return True
    return relative_path.replace(os.sep, "/") in {f"{WORLD_NAME}/{p}" for p in SKIP_RELATIVE}


def build(out_dir: str) -> str:
    sys.path.insert(0, AP_ROOT)
    from Utils import __version__ as ap_version  # noqa: E402
    from worlds.Files import container_version  # noqa: E402

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)
    if "game" not in manifest:
        raise SystemExit('archipelago.json must define "game"')

    manifest["compatible_version"] = COMPATIBLE_VERSION
    manifest["version"] = container_version
    manifest.pop("maximum_ap_version", None)

    os.makedirs(out_dir, exist_ok=True)
    # The filename stem MUST equal the top-level folder inside the zip: the loader
    # imports worlds.<stem>. Keep the version out of the filename.
    out_path = os.path.join(out_dir, f"{WORLD_NAME}.apworld")
    if os.path.exists(out_path):
        os.remove(out_path)

    written: list[str] = []
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for dirpath, dirnames, filenames in os.walk(WORLD_DIR):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for filename in sorted(filenames):
                absolute = os.path.join(dirpath, filename)
                relative = os.path.join(WORLD_NAME, os.path.relpath(absolute, WORLD_DIR)).replace(os.sep, "/")
                if relative.endswith("archipelago.json") or should_skip(relative, filename):
                    continue
                zf.write(absolute, relative)
                written.append(relative)
        zf.writestr(f"{WORLD_NAME}/archipelago.json", json.dumps(manifest, indent=1))
        written.append(f"{WORLD_NAME}/archipelago.json")

    print(f"built {out_path}  ({os.path.getsize(out_path):,} bytes, {len(written)} files)")
    print(f"built against AP {ap_version}, container_version {container_version}")
    print(json.dumps(manifest, indent=2))
    for path in written:
        print(f"  {path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=os.path.join(AP_ROOT, "dist"), help="output directory (default: dist/)")
    parser.add_argument("--expect", help="fail unless both version fields equal this")
    parser.add_argument("--check-only", action="store_true", help="only run the version check")
    parser.add_argument("--print-version", action="store_true",
                        help="check that both version fields agree, then print only the version")
    args = parser.parse_args()
    if args.print_version:
        manifest_version, config_version = read_versions()
        if not manifest_version or manifest_version != config_version:
            check_versions(None)          # exits with the explanation
        print(config_version)
        sys.exit(0)
    check_versions(args.expect)
    if not args.check_only:
        build(args.out)
