"""Tests for the Government Scheme MCP server."""

import pytest
import json
from unittest.mock import AsyncMock, patch
from gov_scheme_mcp.server import health, http_request, create_scheme


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


class TestCreateScheme:
    @pytest.mark.asyncio
    async def test_create_scheme_passes_new_fields(self):
        payload_capture = {}

        async def fake_http_request(method, url_path, body=None):
            nonlocal payload_capture
            payload_capture = body or {}
            return {"id": 1, **(body or {})}

        with patch('gov_scheme_mcp.server.http_request', new=AsyncMock(side_effect=fake_http_request)):
            res = await create_scheme(
                code="SCM001",
                name="Test Scheme",
                benifit_details="Monthly stipend of 1000 INR",
                terms_and_conditions="Must be resident of state",
                scheme_raw_text="Long raw text...",
                official_website="https://example.gov/scheme",
                application_link="https://example.gov/apply",
                is_active=True,
            )
            data = json.loads(res)
            # Ensure the API was called with new fields
            assert payload_capture.get("benifit_details") == "Monthly stipend of 1000 INR"
            assert payload_capture.get("terms_and_conditions") == "Must be resident of state"
            assert payload_capture.get("scheme_raw_text") == "Long raw text..."
            assert payload_capture.get("official_website") == "https://example.gov/scheme"
            assert payload_capture.get("application_link") == "https://example.gov/apply"
            assert data["id"] == 1


if __name__ == "__main__":
    pytest.main([__file__])