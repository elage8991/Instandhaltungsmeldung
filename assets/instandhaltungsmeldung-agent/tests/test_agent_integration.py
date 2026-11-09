"""Integration test: end-to-end agent dialog flow (all external systems mocked)."""
import os
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.tools import StructuredTool
from pydantic import BaseModel

os.environ.setdefault("IBD_TESTING", "1")


class _EmptySchema(BaseModel):
    """Empty input schema for mock tools."""


def _make_mock_tool(name: str) -> StructuredTool:
    """Create a minimal LangChain StructuredTool for testing."""
    async def _noop(**kwargs) -> str:
        return json.dumps({"mock": True, "tool": name})

    def _noop_sync(**kwargs) -> str:
        return json.dumps({"mock": True, "tool": name})

    return StructuredTool(
        name=name,
        description=f"Mock tool: {name}",
        args_schema=_EmptySchema,
        coroutine=_noop,
        func=_noop_sync,
    )


@pytest.fixture
def sample_fl_response():
    return json.dumps({
        "results": [
            {
                "FunctionalLocation": "ZTP-BEESKOW-001",
                "FunctionalLocationName": "Beeskowdamm 3, Hauptgebäude",
                "Plant": "1000",
                "Location": "Berlin",
            }
        ]
    })


@pytest.fixture
def sample_create_response():
    return json.dumps({
        "MaintenanceNotification": "10000042",
        "NotifShortText": "Wasserschaden 2.OG Raum 204",
        "FunctionalLocation": "ZTP-BEESKOW-001",
        "Priority": "2",
        "CreationDate": "/Date(1744588800000)/",
        "RequiredStartDate": "/Date(1744675200000)/",
    })


@pytest.mark.asyncio
async def test_agent_invoke_responds(sample_fl_response):
    """Agent invoke returns a completed status with a non-empty message."""
    from agent import SampleAgent

    mock_tools = [
        _make_mock_tool("list_linearassetmanagementdata_for_cds_api_maintnotification")
    ]

    mock_graph = AsyncMock()
    mock_graph.ainvoke.return_value = {
        "messages": [MagicMock(content="Ich habe 2 technische Plätze gefunden.")]
    }

    with patch("mcp_tools.get_mcp_tools", new=AsyncMock(return_value=mock_tools)):
        with patch("agent.create_agent", return_value=mock_graph):
            agent = SampleAgent()
            result = await agent.invoke(
                query="Ich möchte einen Schaden am Beeskowdamm 3 melden.",
                context_id="test-context-001",
                tools=mock_tools,
            )

    assert result.status == "completed"
    assert result.message != ""


@pytest.mark.asyncio
async def test_agent_full_dialog_flow(sample_fl_response, sample_create_response):
    """Full dialog: address → FL confirmed → description → text → values → create."""
    from agent import SampleAgent

    mock_tools = [
        _make_mock_tool("list_linearassetmanagementdata_for_cds_api_maintnotification"),
        _make_mock_tool("create_maintenancenotification_for_cds_api_maintnotification"),
    ]

    responses = [
        "Ich habe folgende technische Plätze gefunden: ZTP-BEESKOW-001 – Beeskowdamm 3, Hauptgebäude. Möchten Sie diesen verwenden?",
        "Ich habe alle Pflichtfelder: Ort: 2.OG Raum 204, Schaden: Wasserschaden, Beginn: gestern, Gefährdung: Nein.",
        "Kurztext: 'Wasserschaden 2.OG Raum 204'. Langtext generiert.",
        "Priorität: 2 (Hoch), Ausfallkennzeichen: leer, Beginn-Termin: morgen.",
        "Meldung 10000042 erfolgreich angelegt.",
    ]

    call_count = 0

    async def mock_ainvoke(messages, config):
        nonlocal call_count
        resp = responses[min(call_count, len(responses) - 1)]
        call_count += 1
        return {"messages": [MagicMock(content=resp)]}

    mock_graph = AsyncMock()
    mock_graph.ainvoke.side_effect = mock_ainvoke

    with patch("mcp_tools.get_mcp_tools", new=AsyncMock(return_value=mock_tools)):
        with patch("agent.create_agent", return_value=mock_graph):
            agent = SampleAgent()

            # Step 1: address input
            r1 = await agent.invoke("Beeskowdamm 3", "ctx-e2e", tools=mock_tools)
            assert r1.status == "completed"

            # Step 2: damage description
            r2 = await agent.invoke(
                "2.OG Raum 204, Wasserschaden seit gestern, keine Gefährdung",
                "ctx-e2e", tools=mock_tools,
            )
            assert r2.status == "completed"

            # Step 3: text preparation
            r3 = await agent.invoke("Text aufbereiten", "ctx-e2e", tools=mock_tools)
            assert r3.status == "completed"

            # Step 4: value proposal
            r4 = await agent.invoke("Werte vorschlagen", "ctx-e2e", tools=mock_tools)
            assert r4.status == "completed"

            # Step 5: confirm and create
            r5 = await agent.invoke("Ja, Meldung anlegen", "ctx-e2e", tools=mock_tools)
            assert r5.status == "completed"
            assert "10000042" in r5.message or "angelegt" in r5.message.lower()


@pytest.mark.asyncio
async def test_agent_no_tools_graceful():
    """Agent handles gracefully when no MCP tools are available."""
    from agent import SampleAgent

    mock_graph = AsyncMock()
    mock_graph.ainvoke.return_value = {
        "messages": [MagicMock(content="Keine Tools verfügbar.")]
    }
    with patch("agent.create_agent", return_value=mock_graph):
        agent = SampleAgent()
        result = await agent.invoke(
            query="Schaden melden",
            context_id="test-no-tools",
            tools=[],
        )
    assert result.status in ("completed", "error", "input_required")


@pytest.mark.asyncio
async def test_milestone_m1_achieved():
    """M1 milestone logging is called when functional location is confirmed."""
    from agent import SampleAgent

    agent = SampleAgent()
    # Should not raise — just logs
    await agent._milestone_m1(achieved=True, details="ZTP-BEESKOW-001")


@pytest.mark.asyncio
async def test_milestone_m5_missed():
    """M5 milestone logging for missed case includes error message."""
    from agent import SampleAgent

    agent = SampleAgent()
    await agent._milestone_m5(
        achieved=False, error_message="HTTP 400 Bad Request"
    )


def test_system_prompt_contains_skill_instruction():
    """System prompt instructs agent to load the instandhaltungsmeldung skill."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "instandhaltungsmeldung" in prompt.lower()


def test_system_prompt_contains_kurztext_limit():
    """System prompt mentions the 40-character limit for Kurztext."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "40" in prompt
