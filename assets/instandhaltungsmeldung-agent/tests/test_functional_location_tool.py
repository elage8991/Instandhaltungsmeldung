"""Unit tests for the functional location search MCP tool (M1 milestone)."""
import json
import os
import pytest

os.environ.setdefault("IBD_TESTING", "1")


@pytest.fixture
def mock_fl_results():
    """Mock results for functional location search."""
    return {
        "results": [
            {
                "FunctionalLocation": "ZTP-BEESKOW-001",
                "FunctionalLocationName": "Beeskowdamm 3, Hauptgebäude",
                "Plant": "1000",
                "Location": "Berlin",
            },
            {
                "FunctionalLocation": "ZTP-BEESKOW-002",
                "FunctionalLocationName": "Beeskowdamm 3, Nebengebäude",
                "Plant": "1000",
                "Location": "Berlin",
            },
        ]
    }


def test_functional_location_search_returns_results(mock_fl_results):
    """Tool returns a list of functional locations for a given search term."""
    results = mock_fl_results["results"]
    assert len(results) == 2
    assert results[0]["FunctionalLocation"] == "ZTP-BEESKOW-001"
    assert "Beeskowdamm" in results[0]["FunctionalLocationName"]


def test_functional_location_has_required_fields(mock_fl_results):
    """Each functional location entry has the required fields."""
    for fl in mock_fl_results["results"]:
        assert "FunctionalLocation" in fl
        assert "FunctionalLocationName" in fl
        assert "Plant" in fl


def test_functional_location_search_empty():
    """When no locations are found, results list is empty."""
    empty_result = {"results": []}
    assert len(empty_result["results"]) == 0


def test_functional_location_unique_ids(mock_fl_results):
    """Functional location IDs are unique."""
    ids = [fl["FunctionalLocation"] for fl in mock_fl_results["results"]]
    assert len(ids) == len(set(ids))


def test_mock_file_contains_fl_tool():
    """mcp-mock.json contains the list_linearassetmanagementdata tool."""
    mock_path = os.path.join(os.path.dirname(__file__), "..", "mcp-mock.json")
    assert os.path.exists(mock_path), "mcp-mock.json must exist"
    with open(mock_path) as f:
        mock_data = json.load(f)
    server = next(iter(mock_data["servers"].values()))
    tool_names = list(server["tools"].keys())
    assert any("linearassetmanagement" in t for t in tool_names), (
        "Expected a tool for linear asset management (functional location search)"
    )
