"""
parser.py
Scans TypeScript files for @Expects('dot.path') annotations
and extracts them into a structured list.
"""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Binding:
    """Represents a single @Expects annotation found in a TS file."""
    file: str
    line: int
    field: str
    path: str  # dot-notation path e.g. "user.profile.name"
    expected_type: Optional[str] = None  # e.g. "string", "number"


# Matches: @Expects('some.dot.path')
EXPECTS_PATTERN = re.compile(r"@Expects\(['\"]([^'\"]+)['\"]\)")

# Matches the field declaration on the next non-empty line
# e.g. "displayName: string;" or "postCount: number"
FIELD_PATTERN = re.compile(r"(\w+)\s*[?!]?\s*:\s*(\w+)")


def parse_file(filepath: str) -> list[Binding]:
    """Parse a single TS file and return all @Expects bindings found."""
    bindings = []
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    lines = path.read_text().splitlines()

    for i, line in enumerate(lines):
        match = EXPECTS_PATTERN.search(line)
        if not match:
            continue

        dot_path = match.group(1)

        # Look ahead for the field declaration (skip blank lines)
        field_name = None
        field_type = None
        for j in range(i + 1, min(i + 4, len(lines))):
            field_match = FIELD_PATTERN.search(lines[j])
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2)
                break

        bindings.append(Binding(
            file=str(filepath),
            line=i + 1,
            field=field_name or "unknown",
            path=dot_path,
            expected_type=field_type,
        ))

    return bindings


def parse_directory(directory: str) -> list[Binding]:
    """Recursively scan a directory for TS/TSX files and parse all of them."""
    all_bindings = []
    base = Path(directory)

    for ts_file in base.rglob("*.ts"):
        all_bindings.extend(parse_file(str(ts_file)))
    for tsx_file in base.rglob("*.tsx"):
        all_bindings.extend(parse_file(str(tsx_file)))

    return all_bindings