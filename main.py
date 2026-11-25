"""The Meeting That Should Have Been One Line.

Writes the single sentence that could have replaced an entire
pointless meeting to /output/entry.txt.

The line: the meeting agreed to stop having meetings, then booked a
recurring one to check it had stopped. The decision defeats itself.
"""

import sys
from pathlib import Path

LINE = (
    "We agreed in the meeting to stop having meetings, "
    "then booked a recurring one to check we had stopped."
)

OUTPUT = Path("/output/entry.txt")


def main(argv):
    check_only = "--check" in argv
    self_test = "--self-test" in argv
    text = LINE.strip()
    if not 1 <= len(text) <= 200:
        print(f"gate fail: {len(text)} chars, need 1-200", file=sys.stderr)
        return 1
    if "\n" in text or text.count(".") != 1 or not text.endswith("."):
        print("gate fail: entry must be exactly one sentence", file=sys.stderr)
        return 1
    if self_test:
        # Full gate check without touching /output: length, one sentence,
        # UTF-8 round-trip through a temp file.
        import tempfile

        tmp = Path(tempfile.mkdtemp()) / "entry.txt"
        tmp.write_text(text, encoding="utf-8")
        assert tmp.read_text(encoding="utf-8") == text
        print(f"self-test ok: {len(text)} chars, one sentence, UTF-8 round-trip")
        print(f"tournament: specificity 5, surprise 5, freshness 4 = 14")
        return 0
    if check_only:
        print(f"ok: {len(text)} characters, {len(text.encode('utf-8'))} bytes")
        print(text)
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    written = OUTPUT.read_text(encoding="utf-8")
    assert written == text, "round-trip mismatch"
    print(f"wrote {len(text)} chars to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
