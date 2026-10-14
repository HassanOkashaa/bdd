"""Helpers for URL strings without validation or normalization."""

from collections.abc import Iterable


def deduplicate_urls(urls: Iterable[str]) -> list[str]:
    """Return a new list of exact URL strings in first-seen order."""
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result
