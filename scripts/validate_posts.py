#!/usr/bin/env python3
"""Validate Jekyll post front matter and filenames.

Rules enforced on every file in `_posts/`:
  1. Filename follows the `YYYY-MM-DD-slug.md` convention Jekyll requires.
  2. The file opens with a YAML front matter block (`---` ... `---`).
  3. Required keys are present and non-empty: title, categories, tags, description.
  4. If a `date:` key is present, its date portion matches the filename date.

`categories`/`tags` may be either a YAML scalar or a list — Jekyll accepts both,
so the format is not constrained here.

Exits non-zero (and prints every problem) when any post fails, so CI blocks it.
"""

from __future__ import annotations

import glob
import os
import re
import sys

import yaml

POSTS_GLOB = "_posts/*.md"
REQUIRED_KEYS = ("title", "categories", "tags", "description")
FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-.+\.md$")
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(\n|$)", re.DOTALL)


def is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


def validate(path: str) -> list[str]:
    base = os.path.basename(path)
    errors: list[str] = []

    name_match = FILENAME_RE.match(base)
    if not name_match:
        errors.append("filename must match YYYY-MM-DD-slug.md")

    text = open(path, encoding="utf-8").read()
    fm_match = FRONT_MATTER_RE.match(text)
    if not fm_match:
        errors.append("missing YAML front matter block (--- ... ---) at the top")
        return errors

    try:
        front = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError as exc:
        errors.append(f"front matter is not valid YAML: {exc}")
        return errors

    if not isinstance(front, dict):
        errors.append("front matter must be a mapping of keys to values")
        return errors

    for key in REQUIRED_KEYS:
        if key not in front:
            errors.append(f"missing required key: {key}")
        elif is_empty(front[key]):
            errors.append(f"required key is empty: {key}")

    if "date" in front and name_match:
        fm_date = str(front["date"])[:10]
        file_date = name_match.group(1)
        if fm_date != file_date:
            errors.append(f"date ({fm_date}) does not match filename date ({file_date})")

    return errors


def main() -> int:
    paths = sorted(glob.glob(POSTS_GLOB))
    if not paths:
        print(f"No posts found matching {POSTS_GLOB}", file=sys.stderr)
        return 1

    failures = 0
    for path in paths:
        errors = validate(path)
        if errors:
            failures += 1
            print(f"::error file={path}::{'; '.join(errors)}")
            print(f"✗ {path}")
            for err in errors:
                print(f"    - {err}")

    total = len(paths)
    if failures:
        print(f"\n{failures}/{total} post(s) failed front matter validation.")
        return 1

    print(f"✓ All {total} posts passed front matter validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
