"""Small, dependency-free metadata source adapters for the hockey evidence updater."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

SOURCE_URLS = {
    "pubmed": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=100&term={query}",
    "crossref": "https://api.crossref.org/works?rows=100&query.bibliographic={query}",
    "openalex": "https://api.openalex.org/works?per-page=100&search={query}",
}


def build_queries(topics=None, languages=None):
    topics = topics or [
        "ice hockey wearable physiology",
        "ice hockey skating biomechanics acceleration",
        "ice hockey heart rate training load recovery",
        "inline hockey wearable physiology",
        "inline hockey skating biomechanics",
        "speed skating wearable biomechanics acceleration",
        "speed skating heart rate fatigue recovery",
    ]
    # Explicit query specs keep source provenance while accepting the plan's topic API.
    return [{"source": source, "query": topic} for topic in topics for source in SOURCE_URLS]


def _default_transport(url, headers, timeout):
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:  # nosec B310 - fixed HTTPS endpoints above
        body = response.read().decode("utf-8")
        return {"status": response.status, "payload": json.loads(body)}


def run_source(source, query, *, transport=None, timeout=20):
    """Run one bounded source request. Transport is injectable for deterministic tests."""
    if source not in SOURCE_URLS:
        raise ValueError(f"unsupported source: {source}")
    transport = transport or _default_transport
    url = SOURCE_URLS[source].format(query=quote_plus(query))
    started = datetime.now(timezone.utc).isoformat()
    try:
        response = transport(url, {"Accept": "application/json", "User-Agent": "hockey-evidence/1.0"}, timeout)
        status = response.get("status", 200)
        return {"source": source, "query": query, "started_at": started, "status": status,
                "complete": 200 <= status < 300, "payload": response.get("payload", {}) if status < 400 else {},
                "error": None if status < 400 else f"HTTP {status}"}
    except Exception as exc:  # source failures are data, not fatal updater errors
        return {"source": source, "query": query, "started_at": started, "status": None,
                "complete": False, "payload": {}, "error": f"{type(exc).__name__}: {exc}"}


def extract_records(result):
    """Extract conservative bibliographic candidates; never invent study fields."""
    payload = result.get("payload") or {}
    source = result["source"]
    if source == "crossref":
        items = payload.get("message", {}).get("items", [])
    elif source == "openalex":
        items = payload.get("results", [])
    else:
        ids = payload.get("esearchresult", {}).get("idlist", [])
        return [{"identifiers": {"pmid": str(pmid)}, "bibliography": {}, "review_status": "bibliographic_only",
                 "provenance": [{"source": source, "query": result["query"]}]} for pmid in ids]
    records = []
    for item in items:
        ids = {}
        if item.get("DOI") or item.get("doi"):
            ids["doi"] = (item.get("DOI") or item.get("doi")).lower().replace("https://doi.org/", "")
        if item.get("id"):
            ids["openalex"] = item["id"]
        title = item.get("title") or []
        date = item.get("published-online") or item.get("published-print") or item.get("issued") or {}
        year = date.get("date-parts", [[None]])[0][0] if isinstance(date, dict) else None
        records.append({"identifiers": ids, "bibliography": {"title": title[0] if isinstance(title, list) and title else title, "year": year},
                         "review_status": "bibliographic_only", "provenance": [{"source": source, "query": result["query"]}]})
    return records
