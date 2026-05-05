"""
fetcher.py
Fetches API responses and flattens them into dot-notation paths.
e.g. { user: { profile: { name: "John" } } }
  -> { "user.profile.name": "John", ... }
"""

import httpx
from typing import Any


def fetch(url: str, method: str = "GET", headers: dict = None) -> dict:
    """Fetch a JSON response from an API endpoint."""
    with httpx.Client(timeout=10.0) as client:
        response = client.request(method, url, headers=headers or {})
        response.raise_for_status()
        return response.json()


def flatten(data: Any, prefix: str = "") -> dict[str, Any]:
    """
    Recursively flatten a nested JSON object into dot-notation paths.

    Example:
        flatten({"user": {"name": "John", "age": 30}})
        -> {"user.name": "John", "user.age": 30}
    """
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                result.update(flatten(value, full_key))
            else:
                result[full_key] = value

    elif isinstance(data, list):
        # For arrays, index each item (e.g. "items.0.name")
        for i, item in enumerate(data):
            full_key = f"{prefix}.{i}" if prefix else str(i)
            if isinstance(item, (dict, list)):
                result.update(flatten(item, full_key))
            else:
                result[full_key] = item

    else:
        result[prefix] = data

    return result


def fetch_and_flatten(url: str, method: str = "GET", headers: dict = None) -> dict[str, Any]:
    """Convenience: fetch an endpoint and return its flattened dot-paths."""
    raw = fetch(url, method, headers)
    return flatten(raw)