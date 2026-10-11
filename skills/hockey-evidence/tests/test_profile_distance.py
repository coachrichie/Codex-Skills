"""Regressions for source transfer and the executable distance reference contract."""
import inspect
import json
from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_topic_index import build_topic_index
import build_topic_index as topic_index_module
from validate_corpus import validate_study


def records():
    return {r["identifiers"]["study_id"]: r for r in (
        json.loads(line) for line in (ROOT / "data/studies.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    )}


def reference():
    path = ROOT / "references/profile-distance.md"
    assert path.is_file(), "The distance-per-push reference must be discoverable"
    return path.read_text(encoding="utf-8")


def examples():
    namespace = {}
    for block in re.findall(r"```python\n(.*?)```", reference(), re.S):
        exec(compile(block, "profile-distance.md", "exec"), namespace)
    return namespace


def test_distance_requests_route_to_reference_and_proposal_renderer():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^]]+\]\(([^)]+)\)", skill)
    assert "references/profile-distance.md" in links
    assert "algorithm-design.md" in re.findall(r"\[[^]]+\]\(([^)]+)\)", reference())
    for trigger in ("distance-per-push", "anthropometry", "height", "weight/BMI", "skating-distance"):
        assert trigger in skill


@pytest.mark.parametrize("height,expected", [
    (None, (125, 225, "default")), (79.9, (125, 225, "default")),
    (250.1, (125, 225, "default")), (float("nan"), (125, 225, "default")),
    (float("inf"), (125, 225, "default")), (True, (125, 225, "default")),
    ("180", (125, 225, "default")), (80, (118, 212, "profile_height")),
    (160, (118, 213, "profile_height")), (180, (125, 225, "profile_height")),
    (200, (132, 238, "profile_height")), (250, (133, 239, "profile_height")),
])
def test_prior_handles_height_bounds_clamps_rounding_and_exact_fallback(height, expected):
    prior = examples()["distance_constants"]
    assert list(inspect.signature(prior).parameters) == ["height_cm"]
    assert prior(height) == expected


def test_fixed_release_and_first_four_boundary_are_executable():
    distance = examples()["push_distance_cm"]
    assert [distance(i, 250) for i in range(1, 7)] == [125, 125, 125, 125, 225, 225]
    assert [distance(i, 250, experimental=True) for i in range(1, 7)] == [133, 133, 133, 133, 239, 239]


def test_gate_contract_preserves_holdout_bootstrap_and_architecture_boundaries():
    contract = json.loads(re.search(r"```json\n(.*?)```", reference(), re.S).group(1))
    assert contract["release_default"] == "fixed"
    assert contract["height_proxy"] == "leg_length"
    assert contract["distance_multiplier_inputs"] == ["height_cm"]
    assert contract["source_storage"] == "in_memory_only"
    assert contract["wrist_accuracy_validated"] is False
    assert contract["surface_selector_added"] is False
    assert contract["gps_required"] is False
    assert contract["upload_behavior_added"] is False
    assert contract["automatic_calibration_activation"] is False
    assert contract["layers"] == ["scientific_baseline", "local_known_distance_calibration"]
    assert contract["beta_out_of_scope"] == ["global_model_training", "server_upload", "gps"]
    assert contract["validation"] == {
        "split": "held_out_player_grouped", "evaluate": ["ice", "inline", "combined"],
        "min_skaters_per_surface": 12, "straight_runs": 3, "straight_run_m": [20, 30],
        "hockey_like_sequences": 1, "min_mae_reduction_percent": 5,
        "bootstrap": {"replicates": 10000, "unit": "player", "paired": True,
                      "seed": 20261010, "rng": "NumPy Generator(PCG64)",
                      "percentiles": [2.5, 97.5], "method": "linear", "ci_lower_mae_fixed_minus_profile_gt": 0},
        "max_absolute_bias_worsening_m": 1, "max_absolute_bias_worsening_percentage_points": 2,
    }


def test_new_studies_are_valid_source_linked_and_review_scope_is_bounded():
    corpus = records()
    expected = {
        "hockey-budarick-2020": ("abstract_only", "10.1080/14763141.2018.1503323", "ice_hockey"),
        "bandy-pojskic-2025": ("abstract_only", None, "bandy"),
        "bandy-vanden-tillaar-2025": ("abstract_only", "10.3390/biomechanics5020037", "bandy"),
        "inline-speed-wu-2025": ("abstract_only", "10.3390/app15147994", "inline_speed_skating"),
    }
    assert set(expected) <= corpus.keys()
    for study_id, (status, doi, sport) in expected.items():
        rec = corpus[study_id]
        assert validate_study(rec) == []
        assert rec["review_status"] == status
        assert rec["identifiers"].get("doi") == doi
        assert rec["sport_context"]["sports"] == [sport]
        assert rec["methods"]["review_scope"]
        assert rec["findings"] and rec["limitations"]
        assert all(f["source_url"].startswith("https://") for f in rec["findings"])
        assert all(p.get("url", "").startswith("https://") for p in rec["provenance"])
    conference = corpus["bandy-pojskic-2025"]
    assert conference["identifiers"]["urn"] == "urn:nbn:se:lnu:diva-141180"
    assert conference["bibliography"]["publication_type"] == "refereed_conference_abstract"
    assert conference["provenance"][-1]["identifier_verified"] is False
    assert conference["methods"]["participants"] == 32
    assert conference["findings"][0]["measurements"] == {
        "leg_length_partial_r": [0.40, 0.49], "p_lt": 0.05,
        "controlled_for": "BMI", "BMI_acceleration_velocity_partial_r": 0.40,
        "BMI_controlled_for": "leg_length",
    }


def test_full_text_upgrades_preserve_seed_provenance_and_do_not_transfer_wrist_accuracy():
    corpus = records()
    for study_id in ("hockey-allisse-2023", "hockey-skating-khandan-2022"):
        rec = corpus[study_id]
        assert rec["review_status"] == "full_text_reviewed"
        assert rec["methods"]["full_text_reviewed"] is True
        assert rec["methods"]["review_scope"]
        assert len([p for p in rec["provenance"] if p["accessed"] == "2026-09-28"]) == 2
        assert any(p["accessed"] == "2026-10-11" for p in rec["provenance"])
        assert all(f["source_url"] for f in rec["findings"])
    skating = corpus["hockey-skating-khandan-2022"]
    assert skating["methods"]["sensor_locations"] == ["pelvis", "left_shank", "right_shank", "left_skate", "right_skate"]
    assert skating["findings"][0]["measurements"] == {
        "pelvis_stride_length_relative_error_percent": [2, 6], "rest_before_after_s_min": 3,
        "synthetic_ice_trial_m": 14, "speed_m_s": [0.88, 2.63],
    }
    assert skating["transferability"]["sensor_compatibility"] == "low"


@pytest.mark.parametrize("study_id,source,access_status", [
    ("bandy-pojskic-2025", "DiVA conference repository copy", "failed"),
    ("bandy-pojskic-2025", "ResearchGate deposit locator", "unverified"),
    ("bandy-vanden-tillaar-2025", "DiVA institutional PDF locator", "failed"),
])
def test_failed_or_unverified_locators_do_not_claim_substantive_source_fields(study_id, source, access_status):
    provenance = next(p for p in records()[study_id]["provenance"] if p["source"] == source)
    assert provenance["fields"] == []
    assert provenance["purpose"] == "locator_or_access_attempt"
    assert provenance["access_status"] == access_status
    assert provenance["access_failure"]
    assert provenance["review_scope"]


def test_distance_topic_retrieves_anthropometry_records_and_both_indexes_match_fresh_rendering():
    corpus = records()
    index = build_topic_index(list(corpus.values()))
    assert {"bandy-pojskic-2025", "bandy-vanden-tillaar-2025", "hockey-budarick-2020", "inline-speed-wu-2025"} <= set(index.get("distance", []))
    render = getattr(topic_index_module, "render_topic_index", None)
    assert callable(render), "The CLI's deterministic rendering must be testable independently of committed indexes"
    fresh = render(list(corpus.values()))
    assert fresh == render(list(reversed(list(corpus.values()))))
    for filename in ("topic-index.md", "topic_index.md"):
        assert (ROOT / "data" / filename).read_text(encoding="utf-8") == fresh
    distance_section = fresh.split("## distance\n", 1)[1].split("## ", 1)[0]
    assert all(f"`{study_id}`" in distance_section for study_id in index["distance"])


def test_search_audit_is_append_only_and_records_access_failures_and_counts():
    searches = [json.loads(line) for line in (ROOT / "data/searches.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert searches[0]["run_id"] == "initial-seed-2026-09-28"
    audit = next((r for r in searches if r["run_at"] == "2026-10-11"), None)
    assert audit is not None, "The bounded source audit must be logged"
    assert audit["complete"] is False
    assert audit["counts"] == {"before": 5, "reviewed_candidates": 6, "added": 4, "upgraded": 2, "after": 9}
    assert audit["queries"] and audit["sources"] and audit["failures"]
    assert audit["coverage_notes"] and len(records()) == 9
