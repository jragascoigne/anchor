"""
reporter.py
Formats CheckResults into clean, readable CLI output.
Returns an exit code (0 = all clear, 1 = issues found).
"""

from anchor.checker import CheckResult

# ANSI colour codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def report(results: list[CheckResult], endpoint_name: str) -> int:
    """Print a formatted report. Returns 1 if any issues found, else 0."""

    print(f"\n{BOLD}Anchor{RESET} — checking {CYAN}{endpoint_name}{RESET}\n")

    ok = [r for r in results if r.status == "ok"]
    missing = [r for r in results if r.status == "missing"]
    mismatches = [r for r in results if r.status == "type_mismatch"]

    # Print OK results
    for r in ok:
        print(f"  {GREEN}✓{RESET}  {r.binding.path:<40} {DIM}→ ok ({r.actual_type}){RESET}")

    # Print missing paths
    for r in missing:
        print(f"  {RED}✗{RESET}  {r.binding.path:<40} {RED}NOT FOUND{RESET}")
        if r.suggestions:
            for s in r.suggestions:
                print(f"       {DIM}did you mean: {s}?{RESET}")

    # Print type mismatches
    for r in mismatches:
        print(
            f"  {YELLOW}⚠{RESET}  {r.binding.path:<40} "
            f"{YELLOW}TYPE MISMATCH{RESET} "
            f"{DIM}(expected {r.binding.expected_type}, got {r.actual_type}){RESET}"
        )

    # Summary line
    total = len(results)
    issues = len(missing) + len(mismatches)
    print()

    if issues == 0:
        print(f"  {GREEN}{BOLD}All clear.{RESET} {total}/{total} bindings matched.\n")
        return 0
    else:
        print(
            f"  {RED}{BOLD}{issues} issue(s) found.{RESET} "
            f"{len(ok)}/{total} bindings matched.\n"
        )
        return 1