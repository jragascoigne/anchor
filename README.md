# Anchor
 
> A CLI tool that detects API schema drift
<img width="642" height="211" alt="Screenshot 2026-05-05 at 19 41 07" src="https://github.com/user-attachments/assets/619f6a44-b619-493b-af88-beb4668d9977" />
 
---
 
## What is this?
 
Anchor is a CLI tool that checks whether the data your frontend expects actually exists in your API response.
 
You annotate your TypeScript components with `@Expects` comments. Anchor hits your API, compares the response against your annotations, and tells you exactly what's missing or mismatched (with suggestions for what you probably meant).
 
Think of it as a spell checker for your API bindings.
 
---
 
## Install
 
```bash
git clone https://github.com/jragascoigne/anchor.git
cd anchor
pip3 install -e .
```
 
Add the `anchor` command to your PATH if needed (pip will tell you where it installed the script).
 
---
 
## Usage
 
**1. Add `@Expects` annotations to your TypeScript files**
 
```typescript
// UserCard.tsx
 
// @Expects('user.profile.name')
const displayName: string = '';
 
// @Expects('user.stats.postCount')
const postCount: number = 0;
 
// @Expects('user.email')
const email: string = '';
```
 
**2. Configure your endpoints in `anchor.config.json`**
 
```json
{
  "endpoints": [
    {
      "name": "getUser",
      "url": "https://your-api.com/user",
      "method": "GET"
    }
  ],
  "watch": ["./src"]
}
```
 
**3. Run**
 
```bash
anchor check
```
 
---
 
## Config options
 
| Key | Description |
|---|---|
| `endpoints` | List of API endpoints to check against |
| `endpoints[].name` | A label for the endpoint (used in output) |
| `endpoints[].url` | The full URL to fetch |
| `endpoints[].method` | HTTP method — `GET`, `POST`, etc. |
| `watch` | List of directories to scan for `@Expects` annotations |
 
---
 
## How it works
 
1. **Parses** your TypeScript files for `@Expects('dot.path')` annotations
2. **Fetches** your API endpoints and flattens the JSON response into dot-notation paths
3. **Diffs** your expected paths against the real response
4. **Reports** any missing paths or type mismatches, with fuzzy suggestions for close matches
---
 
## Use in CI
 
Anchor exits with code `1` if any issues are found, making it a natural fit for CI pipelines.
 
```yaml
# .github/workflows/anchor.yml
name: Anchor check
 
on: [push, pull_request]
 
jobs:
  anchor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -e .
      - run: anchor check
```
 
---
 
## Project structure
 
```
anchor/
├── anchor/
│   ├── cli.py          # Entry point — the anchor check command
│   ├── parser.py       # Scans TS files for @Expects annotations
│   ├── fetcher.py      # Fetches API responses, flattens to dot-paths
│   ├── checker.py      # Diffs expected paths vs real response
│   └── reporter.py     # Formats and prints the output
├── example/            # Demo component with @Expects annotations
├── anchor.config.json  # Endpoint and watch config
└── setup.py
```
 
---
 
## Made with
 
- [Python](https://python.org) — CLI and core logic
- [Click](https://click.palletsprojects.com) — CLI framework
- [httpx](https://www.python-httpx.org) — API fetching
- [difflib](https://docs.python.org/3/library/difflib.html) — fuzzy path suggestions (stdlib)
---

by [John Gascoigne](https://www.github.com/jragascoigne)
