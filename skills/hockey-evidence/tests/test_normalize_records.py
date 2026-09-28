from scripts.normalize_records import normalize_record


def test_normalize_record_canonicalizes_doi_title_authors_and_ids():
    raw = {
        "doi": "https://doi.org/10.1000/ABC.1.",
        "title": "  Effects  of\n Skating\u00a0Load  ",
        "authors": ["Doe, Jane", {"family": "Müller", "given": "Ánne"}],
        "pmid": " PMID: 12345 ",
        "openalex_id": "https://openalex.org/W123",
        "source": "pubmed",
    }
    result = normalize_record(raw)
    assert result["identifiers"]["doi"] == "10.1000/abc.1"
    assert result["bibliography"]["title"] == "Effects of Skating Load"
    assert result["bibliography"]["authors"] == ["Doe, Jane", "Müller, Ánne"]
    assert result["identifiers"]["pmid"] == "12345"
    assert result["identifiers"]["openalex"] == "W123"
    assert result["provenance"]


def test_normalize_record_keeps_missing_fields_unknown():
    result = normalize_record({})
    assert result["identifiers"]["doi"] is None
    assert result["bibliography"]["title"] is None
    assert result["bibliography"]["authors"] == []
    assert result["review_status"] == "bibliographic_only"


def test_normalize_record_accepts_www_doi_url():
    assert normalize_record({"doi": "https://www.doi.org/10.1000/WWW"})["identifiers"]["doi"] == "10.1000/www"
