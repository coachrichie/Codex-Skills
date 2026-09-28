"""Pure normalization helpers for literature metadata."""

from __future__ import annotations

import re
import unicodedata
from typing import Any


def _first(raw: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in raw and raw[name] not in (None, ""):
            return raw[name]
    return None


def normalize_doi(value: Any) -> str | None:
    if value is None:
        return None
    doi = str(value).strip()
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    doi = re.sub(r"^https?://(?:www\.)?(?:dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = doi.strip().rstrip(".,;)")
    return doi.casefold() or None


def normalize_title(value: Any) -> str | None:
    if value is None:
        return None
    text = unicodedata.normalize("NFC", str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def normalize_authors(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    result: list[str] = []
    for author in value:
        if isinstance(author, dict):
            family = author.get("family") or author.get("last")
            given = author.get("given") or author.get("first")
            author = ", ".join(str(x).strip() for x in (family, given) if x)
        text = normalize_title(author)
        if text:
            result.append(text)
    return result


def _source_id(value: Any, prefix: str) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    text = re.sub(rf"^{prefix}:\s*", "", text, flags=re.I)
    text = text.rstrip("/").split("/")[-1]
    return text or None


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic canonical study record without inferred values."""
    identifiers_raw = raw.get("identifiers") if isinstance(raw.get("identifiers"), dict) else {}
    bibliography_raw = raw.get("bibliography") if isinstance(raw.get("bibliography"), dict) else {}
    source = _first(raw, "source", "source_name")
    identifiers = {
        "doi": normalize_doi(_first(raw, "doi", "DOI") or identifiers_raw.get("doi")),
        "pmid": _source_id(_first(raw, "pmid", "PMID") or identifiers_raw.get("pmid"), "pmid"),
        "openalex": _source_id(_first(raw, "openalex", "openalex_id", "OpenAlex") or identifiers_raw.get("openalex"), "openalex"),
        "crossref": _source_id(_first(raw, "crossref", "crossref_id") or identifiers_raw.get("crossref"), "crossref"),
    }
    title = normalize_title(_first(raw, "title", "article_title") or bibliography_raw.get("title"))
    authors = normalize_authors(_first(raw, "authors", "author") or bibliography_raw.get("authors"))
    provenance = list(raw.get("provenance", [])) if isinstance(raw.get("provenance"), list) else []
    if source:
        provenance.append({"source": str(source), "fields": [
            "identifiers.doi", "identifiers.pmid", "identifiers.openalex", "identifiers.crossref",
            "bibliography.title", "bibliography.authors", "bibliography.year", "bibliography.journal",
        ]})
    result = {
        "identifiers": identifiers,
        "bibliography": {
            "title": title,
            "authors": authors,
            "year": _first(raw, "year", "publication_year") or bibliography_raw.get("year"),
            "journal": _first(raw, "journal", "container_title") or bibliography_raw.get("journal"),
        },
        "sport_context": raw.get("sport_context", None),
        "methods": raw.get("methods", None),
        "findings": raw.get("findings", None),
        "limitations": raw.get("limitations", None),
        "review_status": raw.get("review_status", "bibliographic_only"),
        "transferability": raw.get("transferability", None),
        "provenance": provenance,
    }
    return result
