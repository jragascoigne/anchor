"""
checker.py
Diffs @Expects annotations against a live API response 
and reports mismatches with suggestions.
"""

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Any, Optional

from anchor.parser import Binding


@dataclass
class CheckResult:
    binding: Binding
    status: str          # "ok", "missing", "type_mismatch"
    actual_value: Any = None
    actual_type: Optional[str] = None
    suggestions: list = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


# Map Python types to TS type names for comparison
PYTHON_TO_TS_TYPE = {
    str: "string",
    int: "number",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
}


def infer_ts_type(value: Any) -> str:
    return PYTHON_TO_TS_TYPE.get(type(value), "unknown")


def check_bindings(
    bindings: list[Binding],
    flat_response: dict[str, Any],
) -> list[CheckResult]:
    """
    Compare each binding's expected dot-path against the flattened API response.
    Returns a CheckResult for every binding.
    """
    results = []
    all_paths = list(flat_response.keys())

    for binding in bindings:
        if binding.path in flat_response:
            actual_value = flat_response[binding.path]
            actual_type = infer_ts_type(actual_value)

            # Type mismatch check
            if binding.expected_type and binding.expected_type != actual_type:
                results.append(CheckResult(
                    binding=binding,
                    status="type_mismatch",
                    actual_value=actual_value,
                    actual_type=actual_type,
                ))
            else:
                results.append(CheckResult(
                    binding=binding,
                    status="ok",
                    actual_value=actual_value,
                    actual_type=actual_type,
                ))
        else:
            # Path not found — try fuzzy matching for suggestions
            suggestions = get_close_matches(binding.path, all_paths, n=3, cutoff=0.5)
            results.append(CheckResult(
                binding=binding,
                status="missing",
                suggestions=suggestions,
            ))

    return results