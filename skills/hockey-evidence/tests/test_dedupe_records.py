from scripts.dedupe_records import dedupe_records
from scripts.normalize_records import normalize_record


def test_exact_doi_matches_merge_provenance_and_source_ids():
    records = [
        normalize_record({"doi": "10.1000/X", "title": "A Study", "pmid": "1", "source": "pubmed"}),
        normalize_record({"doi": "https://doi.org/10.1000/x", "title": "A study", "openalex_id": "W2", "source": "openalex"}),
    ]
    retained, flags = dedupe_records(records)
    assert len(retained) == 1
    assert flags == []
    assert retained[0]["identifiers"]["pmid"] == "1"
    assert retained[0]["identifiers"]["openalex"] == "W2"
    assert {p["source"] for p in retained[0]["provenance"]} == {"pubmed", "openalex"}


def test_title_only_collision_is_retained_and_flagged():
    records = [
        normalize_record({"title": "Repeated skating study", "authors": ["One"], "source": "a"}),
        normalize_record({"title": "Repeated skating study", "authors": ["Two"], "source": "b"}),
    ]
    retained, flags = dedupe_records(records)
    assert len(retained) == 2
    assert flags and flags[0]["reason"] == "title_collision"


def test_same_doi_conflicting_title_and_status_is_flagged():
    records = [
        normalize_record({"doi": "10.1000/X", "title": "Original", "review_status": "abstract_only", "source": "a"}),
        normalize_record({"doi": "10.1000/X", "title": "Changed", "review_status": "full_text_reviewed", "source": "b"}),
    ]
    retained, flags = dedupe_records(records)
    assert len(retained) == 1
    reasons = {flag["reason"] for flag in flags}
    assert "doi_conflict" in reasons
    assert {flag["field"] for flag in flags if flag["reason"] == "doi_conflict"} == {"title", "review_status"}


def test_merged_fields_have_field_specific_provenance():
    records = [
        normalize_record({"doi": "10.1000/X", "title": "A Study", "source": "pubmed"}),
        normalize_record({"doi": "10.1000/X", "year": 2020, "source": "crossref"}),
    ]
    retained, _ = dedupe_records(records)
    provenance = retained[0]["provenance"]
    assert any(item.get("source") == "crossref" and "bibliography.year" in item.get("fields", []) for item in provenance)
