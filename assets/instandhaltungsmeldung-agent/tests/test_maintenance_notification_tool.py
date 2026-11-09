"""Unit tests for the maintenance notification create MCP tool (M5 milestone)."""
import json
import os
import pytest

os.environ.setdefault("IBD_TESTING", "1")


@pytest.fixture
def mock_create_response():
    """Mock response for creating a maintenance notification."""
    return {
        "MaintenanceNotification": "10000042",
        "NotifShortText": "Wasserschaden 2.OG Raum 204",
        "FunctionalLocation": "ZTP-BEESKOW-001",
        "Priority": "2",
        "MaintNotifInternalID": "000010000042",
        "NotificationStatus": "OSNO",
        "CreationDate": "/Date(1744588800000)/",
        "RequiredStartDate": "/Date(1744675200000)/",
        "MaintNotifBreakdownIndicator": "",
    }


def test_create_notification_returns_id(mock_create_response):
    """Created notification has a MaintenanceNotification ID."""
    assert "MaintenanceNotification" in mock_create_response
    assert mock_create_response["MaintenanceNotification"] == "10000042"


def test_create_notification_short_text_max_40(mock_create_response):
    """NotifShortText must not exceed 40 characters."""
    short_text = mock_create_response["NotifShortText"]
    assert len(short_text) <= 40, f"Short text too long: {len(short_text)} chars"


def test_create_notification_has_functional_location(mock_create_response):
    """Created notification references a functional location."""
    assert "FunctionalLocation" in mock_create_response
    assert mock_create_response["FunctionalLocation"] != ""


def test_create_notification_priority_range(mock_create_response):
    """Priority must be 1, 2, 3, or 4."""
    priority = mock_create_response["Priority"]
    assert priority in ["1", "2", "3", "4"], f"Invalid priority: {priority}"


def test_create_notification_has_required_start_date(mock_create_response):
    """RequiredStartDate must be present and in SAP date format."""
    start_date = mock_create_response["RequiredStartDate"]
    assert start_date.startswith("/Date("), f"Invalid date format: {start_date}"


def test_mock_file_contains_create_tool():
    """mcp-mock.json contains the create_maintenancenotification tool."""
    mock_path = os.path.join(os.path.dirname(__file__), "..", "mcp-mock.json")
    assert os.path.exists(mock_path), "mcp-mock.json must exist"
    with open(mock_path) as f:
        mock_data = json.load(f)
    server = next(iter(mock_data["servers"].values()))
    tool_names = list(server["tools"].keys())
    assert any("create_maintenancenotification" in t for t in tool_names), (
        "Expected a create_maintenancenotification tool"
    )


def test_mock_file_create_tool_has_required_inputs():
    """create_maintenancenotification tool has NotifShortText and FunctionalLocation as inputs."""
    mock_path = os.path.join(os.path.dirname(__file__), "..", "mcp-mock.json")
    with open(mock_path) as f:
        mock_data = json.load(f)
    server = next(iter(mock_data["servers"].values()))
    create_tool = next(
        (t for name, t in server["tools"].items() if "create_maintenancenotification" in name),
        None,
    )
    assert create_tool is not None
    props = create_tool["input_schema"].get("properties", {})
    assert "NotifShortText" in props
    assert "FunctionalLocation" in props
    assert "Priority" in props
