"""Deterministic, conservative record deduplication."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

try:
    from .normalize_records import normalize_record
except ImportError:  # direct script/test path
    from normalize_records import normalize_record


def _title_key(record: dict[str, Any]) -> str | None:
    title = record.get("bibliography", {}).get("title")
    return title.casefold() if title else None


def _doi_key(record: dict[str, Any]) -> str | None:
    return record.get("identifiers", {}).get("doi")


def _merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(a)
    added_fields: list[str] = []
    for key, value in b.get("identifiers", {}).items():
        if value and not result["identifiers"].get(key):
            result["identifiers"][key] = value
            added_fields.append(f"identifiers.{key}")
    for key, value in b.get("bibliography", {}).items():
        if value and not result["bibliography"].get(key):
            result["bibliography"][key] = value
            added_fields.append(f"bibliography.{key}")
    for key in ("sport_context", "methods", "findings", "limitations", "transferability"):
        if result.get(key) is None and b.get(key) is not None:
            result[key] = b[key]
    if b.get("provenance"):
        source = b["provenance"][-1].get("source", "unknown")
        result["provenance"] = result.get("provenance", []) + [{"source": source, "fields": added_fields}]
    return result


def dedupe_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    retained: list[dict[str, Any]] = []
    flags: list[dict[str, Any]] = []
    doi_index: dict[str, int] = {}
    title_index: dict[str, list[int]] = {}
    for position, raw in enumerate(records):
        record = normalize_record(raw)
        doi = _doi_key(record)
        if doi and doi in doi_index:
            index = doi_index[doi]
            existing = retained[index]
            if _title_key(existing) != _title_key(record):
                flags.append({"reason": "doi_conflict", "field": "title", "doi": doi})
            if existing.get("review_status") != record.get("review_status"):
                flags.append({"reason": "doi_conflict", "field": "review_status", "doi": doi})
            retained[index] = _merge(retained[index], record)
            continue
        title = _title_key(record)
        if title and title in title_index:
            flags.append({"reason": "title_collision", "title": title, "record_positions": title_index[title] + [position]})
        index = len(retained)
        retained.append(record)
        if doi:
            doi_index[doi] = index
        if title:
            title_index.setdefault(title, []).append(position)
    return retained, flags
