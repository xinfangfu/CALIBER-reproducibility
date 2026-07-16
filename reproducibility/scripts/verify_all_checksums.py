#!/usr/bin/env python3
"""Verify the release package checksum manifest using only the standard library."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=PACKAGE / "checksums/SHA256SUMS.txt")
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    checked = 0
    failures = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        expected, relative = line.split("  ", 1)
        path = PACKAGE / relative
        if not path.is_file():
            failures.append(f"MISSING {relative}")
        else:
            observed = sha256(path)
            if observed != expected:
                failures.append(f"MISMATCH {relative} expected={expected} observed={observed}")
        checked += 1
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: verified {checked} release files from {manifest.name}")


if __name__ == "__main__":
    main()
