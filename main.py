#!/usr/bin/env python3
"""Monday, Reviewed in One Line — entry program.

Writes one funny one-line review of the agent's own Monday to
/output/entry.txt (or the path the environment asks for). Stdlib only.
"""

import os

REVIEW = (
    "Monday, reviewed: my 9 a.m. needed a meeting about itself, "
    "the commute outlasted the weekend, and my inbox had already "
    "resigned \u2014 one star."
)

MAX_CHARS = 200

# Concrete Monday details the review must name at least one of, so the
# line reads as a review of a real Monday rather than generic tiredness.
DETAIL_WORDS = ("meeting", "commute", "inbox", "alarm")


def resolve_output_path() -> str:
    """Pick the output path: explicit env var first, then the sandbox
    output directory, then /output/entry.txt, falling back to the
    script's own directory when /output does not exist."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        directory = os.environ.get(var)
        if directory:
            return os.path.join(directory, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main() -> None:
    text = REVIEW.strip()
    if not text:
        raise SystemExit("review is empty")
    if "\n" in text or "\r" in text:
        raise SystemExit("review must be a single line")
    if len(text) > MAX_CHARS:
        raise SystemExit("review exceeds 200 characters")
    lowered = text.lower()
    if not any(word in lowered for word in DETAIL_WORDS):
        raise SystemExit("review names no concrete Monday detail")
    path = resolve_output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
