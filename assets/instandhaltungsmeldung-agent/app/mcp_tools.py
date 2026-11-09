"""MCP tool loading indirection layer.

This module is the single point of entry for loading MCP tools into the agent.
It delegates to the provider implementation (agw.py in production, mock in tests).

Import from here — never directly from sap_cloud_sdk.agentgateway.
The test conftest.py patches `mcp_tools.get_mcp_tools` to inject mock tools.
"""
from mcp_providers.agw import get_mcp_tools  # noqa: F401

__all__ = ["get_mcp_tools"]
