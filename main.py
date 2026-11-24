#!/usr/bin/env python3
"""Funniest Time Machine Warning Label — make.fun bounty entry.

Writes exactly one line (no trailing newline) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then reads the
bytes back and re-validates them. Pure Python standard library only.
Deterministic: the same bytes are produced on every run.
"""

import os
import sys

ENTRY_TEXT = (
    "WARNING: Do not press the big red button twice. "
    "Once sends you back in time; twice sends your warranty, "
    "your grandfather, and this entire timeline straight to the void."
)

MIN_LENGTH = 90
MAX_LENGTH = 170


def validate(text):
    """Check the entry text against the competition rules."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if "\n" not in text and "\r" not in text:
        pass
    else:
        raise ValueError("entry must be exactly one line (no newline characters)")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    return True


def main():
    validate(ENTRY_TEXT)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")

    data = ENTRY_TEXT.encode("utf-8")
    with open(output_path, "wb") as handle:
        handle.write(data)

    # Read the bytes back and re-validate exactly what was written.
    with open(output_path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("written bytes differ from the entry text")
    if written.endswith(b"\n") or written.endswith(b"\r"):
        raise ValueError("entry.txt must not end with a newline")
    validate(written.decode("utf-8"))

    print("Wrote %s (%d characters, one line, no trailing newline)"
          % (output_path, len(ENTRY_TEXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
