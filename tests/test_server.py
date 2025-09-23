"""Tests for the Government Scheme MCP server."""

import pytest
import json
from unittest.mock import AsyncMock, patch
from gov_scheme_mcp.server import health, http_request


class TestHTTPRequest:
    """Test HTTP request functionality."""
    
    @pytest.mark.asyncio
    async def test_http_request_success(self):
        """Test successful HTTP request."""
        # This would need proper mocking for httpx
        # For now, just test the function signature
        pass
    
    @pytest.mark.asyncio
    async def test_http_request_error(self):
        """Test HTTP request error handling."""
        # This would need proper mocking for httpx
        # For now, just test the function signature
        pass


class TestHealthTool:
    """Test health check tool."""
    
    @pytest.mark.asyncio
    async def test_health_success(self):
        """Test health check with successful API response."""
        with patch('gov_scheme_mcp.server.http_request') as mock_request:
            mock_request.return_value = {"status": "ok"}
            result = await health()
            response = json.loads(result)
            assert response["ok"] is True
            assert "api" in response
    
    @pytest.mark.asyncio
    async def test_health_failure(self):
        """Test health check with API failure."""
        with patch('gov_scheme_mcp.server.http_request') as mock_request:
            mock_request.side_effect = Exception("Connection failed")
            result = await health()
            response = json.loads(result)
            assert response["ok"] is False
            assert "error" in response


if __name__ == "__main__":
    pytest.main([__file__])