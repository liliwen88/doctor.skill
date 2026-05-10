"""Tests for drug_interaction.py — OpenFDA/DailyMed/RxNorm drug queries."""

import json
import sys
import os
import unittest.mock as mock
import urllib.error
from io import BytesIO

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", ".github", "skills", "doctor", "scripts")
)

from drug_interaction import (
    query_drug_info,
    _query_drug_events,
    _safe_get,
    OPENFDA_BASE_URL,
)


# ── _safe_get ───────────────────────────────────────────────────────


def test_safe_get_list():
    data = {"openfda": {"generic_name": ["Ibuprofen"]}}
    assert _safe_get(data["openfda"], "generic_name", 0) == "Ibuprofen"


def test_safe_get_string():
    data = {"purpose": ["Pain reliever"]}
    assert _safe_get(data, "purpose", 0) == "Pain reliever"


def test_safe_get_missing_key():
    assert _safe_get({}, "nonexistent", 0) is None
    assert _safe_get({"key": []}, "key", 0) is None


def test_safe_get_index_out_of_range():
    assert _safe_get({"key": ["only"]}, "key", 99) is None


# ── query_drug_info (with mocked HTTP) ──────────────────────────────


@mock.patch("drug_interaction.urllib.request.urlopen")
def test_query_drug_success(mock_urlopen):
    """Successful OpenFDA label query returns drug info dict."""
    mock_response = {
        "results": [
            {
                "openfda": {
                    "generic_name": ["Ibuprofen"],
                    "brand_name": ["Advil"],
                    "pharm_class_epc": ["NSAID"],
                    "manufacturer_name": ["Pfizer"],
                },
                "purpose": ["Pain reliever"],
                "indications_and_usage": ["For pain relief"],
                "warnings": ["Do not exceed recommended dose"],
                "adverse_reactions": ["Nausea", "Stomach pain"],
                "contraindications": ["History of GI bleeding"],
                "drug_interactions": ["Warfarin"],
            }
        ]
    }
    mock_urlopen.return_value = BytesIO(
        json.dumps(mock_response).encode("utf-8")
    )

    result = query_drug_info("Ibuprofen")
    assert "drug" in result
    drug = result["drug"]
    assert drug["genericName"] == "Ibuprofen"
    assert drug["brandName"] == "Advil"
    assert drug["drugClass"] == "NSAID"


@mock.patch("drug_interaction.urllib.request.urlopen")
def test_query_drug_http_error_fallback_to_events(mock_urlopen):
    """HTTPError from label endpoint → fallback to adverse events."""
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.fda.gov/drug/label.json",
        code=404,
        msg="Not Found",
        hdrs={},
        fp=None,
    )

    # Patch _query_drug_events to return known dict
    with mock.patch("drug_interaction._query_drug_events") as mock_events:
        mock_events.return_value = {"drug": None, "error": "not found"}
        result = query_drug_info("UnknownDrug")
        assert mock_events.called
        assert "drug" in result


@mock.patch("drug_interaction.urllib.request.urlopen")
def test_query_drug_empty_results_fallback(mock_urlopen):
    """Empty OpenFDA results → fallback to events endpoint."""
    mock_urlopen.return_value = BytesIO(
        json.dumps({"results": []}).encode("utf-8")
    )

    with mock.patch("drug_interaction._query_drug_events") as mock_events:
        mock_events.return_value = {"drug": None, "error": "no data"}
        result = query_drug_info("MadeUpDrug")
        assert mock_events.called


@mock.patch("drug_interaction.urllib.request.urlopen")
def test_query_drug_generic_exception(mock_urlopen):
    """Generic exception should return error dict gracefully."""
    mock_urlopen.side_effect = Exception("Network failure")

    result = query_drug_info("Aspirin")
    assert "drug" in result
    assert result["drug"] is None
    assert "error" in result
    assert "Network failure" in result["error"]


# ── _query_drug_events ──────────────────────────────────────────────


@mock.patch("drug_interaction.urllib.request.urlopen")
def test_query_drug_events_success(mock_urlopen):
    """Successful adverse events query."""
    mock_response = {
        "results": [
            {
                "patient": {
                    "drug": [{"medicinalproduct": "Ibuprofen"}],
                    "reaction": [{"reactionmeddrapt": "Headache"}],
                },
                "serious": "1",
            }
        ]
    }
    mock_urlopen.return_value = BytesIO(
        json.dumps(mock_response).encode("utf-8")
    )

    result = _query_drug_events("Ibuprofen")
    assert "events" in result or "drug" in result


# ── API URL construction ────────────────────────────────────────────


def test_openfda_base_url():
    """Sanity check that the base URL is correctly defined."""
    assert OPENFDA_BASE_URL == "https://api.fda.gov/drug"
    assert "open.fda.gov" in OPENFDA_BASE_URL or "api.fda.gov" in OPENFDA_BASE_URL
