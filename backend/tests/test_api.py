from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from mobility_engine.validation import ValidationIssue


client = TestClient(app)


class ApiTests(unittest.TestCase):
    def test_health_does_not_claim_dataset_validity(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "service": "mobilityforge-api",
            "research_data": "not evaluated by health check",
        }

    def test_observations_preserve_all_source_dimensions(self):
        response = client.get("/observations")
        assert response.status_code == 200
        records = response.json()
        assert len(records) == 24
        assert {record["period"] for record in records} == {"morning", "evening"}
        assert {record["direction"] for record in records} == {
            "towards_yeshwanthpur",
            "towards_nagasandra",
        }
        assert records[0]["road_section"] == "Yeshwanthpur TTMC"
        assert records[0]["volume_pcu"] == "3407"
        assert records[0]["vc_ratio"] == "1.26"

    def test_validation_reports_loaded_data_status(self):
        response = client.get("/observations/validation")
        assert response.status_code == 200
        payload = response.json()
        assert payload["valid"] is True
        assert payload["observation_count"] == 24
        assert payload["issues"] == []

    def test_validation_exposes_validation_failures(self):
        issue = ValidationIssue("source_page", "expected Table 8 source page 46", "Table 8 page 99, section 1")
        with patch("api.main.validate_observations", return_value=[issue]):
            response = client.get("/observations/validation")
        assert response.status_code == 200
        assert response.json() == {
            "valid": False,
            "observation_count": 24,
            "issues": [
                {
                    "code": "source_page",
                    "message": "expected Table 8 source page 46",
                    "source_row": "Table 8 page 99, section 1",
                }
            ],
        }

    def test_missing_source_data_returns_service_unavailable(self):
        with patch("api.main.load_observations", side_effect=FileNotFoundError):
            observations_response = client.get("/observations")
            validation_response = client.get("/observations/validation")
        assert observations_response.status_code == 503
        assert validation_response.status_code == 503
        assert observations_response.json() == {"detail": "source observation data is unavailable"}

    def test_unexpected_source_failure_does_not_leak_details(self):
        with patch("api.main.load_observations", side_effect=RuntimeError("private implementation detail")):
            response = client.get("/observations")
        assert response.status_code == 500
        assert response.json() == {"detail": "unexpected source-data failure"}

    def test_unexpected_validation_failure_does_not_leak_details(self):
        with patch("api.main.validate_observations", side_effect=RuntimeError("private validation detail")):
            response = client.get("/observations/validation")
        assert response.status_code == 500
        assert response.json() == {"detail": "unexpected validation failure"}

    def test_decision_run_returns_one_provisional_slice(self):
        response = client.post("/decision-engine/run", json={
            "period": "morning",
            "direction": "towards_yeshwanthpur",
            "weights": {"pcu": "0.5", "vc": "0.5"},
            "acknowledge_provisional": True,
        })
        assert response.status_code == 200
        payload = response.json()
        assert payload["provisional"] is True
        assert payload["period"] == "morning"
        assert payload["direction"] == "towards_yeshwanthpur"
        assert len(payload["alternatives"]) == 6
        assert {item["section_no"] for item in payload["alternatives"]} == {1, 2, 3, 4, 5, 6}
        assert {item["rank"] for item in payload["alternatives"]} == {1, 2, 3, 4, 5, 6}
        assert "unresolved" in payload["disclosure"]

    def test_decision_run_supports_all_four_separate_runs(self):
        for period in ("morning", "evening"):
            for direction in ("towards_yeshwanthpur", "towards_nagasandra"):
                with self.subTest(period=period, direction=direction):
                    response = client.post("/decision-engine/run", json={
                        "period": period, "direction": direction,
                        "weights": {"pcu": "0.5", "vc": "0.5"},
                        "acknowledge_provisional": True,
                    })
                    assert response.status_code == 200
                    payload = response.json()
                    assert payload["period"] == period
                    assert payload["direction"] == direction
                    assert len(payload["alternatives"]) == 6

    def test_decision_run_requires_acknowledgement_and_valid_weights(self):
        base = {"period": "evening", "direction": "towards_nagasandra", "weights": {"pcu": "0.5", "vc": "0.5"}}
        assert client.post("/decision-engine/run", json=base).status_code == 400
        invalid = {**base, "acknowledge_provisional": True, "weights": {"pcu": "0.4", "vc": "0.4"}}
        response = client.post("/decision-engine/run", json=invalid)
        assert response.status_code == 422

    def test_decision_run_does_not_hide_source_validation_failure(self):
        with patch("api.main.validate_observations", return_value=[ValidationIssue("bad", "bad")]):
            response = client.post("/decision-engine/run", json={
                "period": "morning", "direction": "towards_nagasandra",
                "weights": {"pcu": "0.5", "vc": "0.5"}, "acknowledge_provisional": True,
            })
        assert response.status_code == 503

    def test_decision_run_reports_missing_source_data(self):
        with patch("api.main.load_observations", side_effect=FileNotFoundError):
            response = client.post("/decision-engine/run", json={
                "period": "morning", "direction": "towards_nagasandra",
                "weights": {"pcu": "0.5", "vc": "0.5"}, "acknowledge_provisional": True,
            })
        assert response.status_code == 503
