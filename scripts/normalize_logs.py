"""Normalize log files by deduplicating repeated lines and headings.

This script attempts to keep the first occurrence of repeated lines and remove duplicated blocks.
It is intentionally conservative: it preserves the initial header and the first chronological entries and removes exact duplicate lines.
Usage: python scripts/normalize_logs.py docs/logs/dev_log.md docs/logs/patch_log.md
"""
import sys
from pathlib import Path


def normalize_file(path: Path):
    content = path.read_text(encoding='utf-8')
    seen = set()
    out_lines = []
    for line in content.splitlines():
        sline = line.strip()
        if not sline:
            # keep blank lines (but avoid duplicates of blank lines)
            if out_lines and out_lines[-1].strip() == '':
                continue
            out_lines.append('')
            continue
        if sline in seen:
            # skip repeated lines verbatim
            continue
        seen.add(sline)
        out_lines.append(line)
    path.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')


def main():
    for p in sys.argv[1:]:
        path = Path(p)
        if not path.exists():
            print(f"File not found: {p}")
            continue
        print(f"Normalizing {p}")
        normalize_file(path)


if __name__ == '__main__':
    main()
