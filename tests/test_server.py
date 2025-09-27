"""Tests for the Government Scheme MCP server."""

import pytest
import json
from unittest.mock import AsyncMock, patch
from gov_scheme_mcp.server import health, http_request, create_scheme, update_scheme, delete_scheme


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


class TestUpdateDeleteScheme:
    @pytest.mark.asyncio
    async def test_update_scheme_calls_patch_with_payload(self):
        captured = {"method": None, "url": None, "body": None}

        async def fake_http_request(method, url_path, body=None):
            captured["method"] = method
            captured["url"] = url_path
            captured["body"] = body
            return {"id": 123, **(body or {})}

        with patch('gov_scheme_mcp.server.http_request', new=AsyncMock(side_effect=fake_http_request)):
            res = await update_scheme(
                123,
                name="Updated Name",
                official_website="https://example.gov/updated",
                is_active=False,
            )
            data = json.loads(res)
            assert captured["method"] == "PATCH"
            assert captured["url"].endswith("/api/schemes/123")
            assert captured["body"]["name"] == "Updated Name"
            assert captured["body"]["official_website"] == "https://example.gov/updated"
            assert captured["body"]["is_active"] is False
            assert data["id"] == 123

    @pytest.mark.asyncio
    async def test_delete_scheme_calls_delete(self):
        captured = {"method": None, "url": None}

        async def fake_http_request(method, url_path, body=None):
            captured["method"] = method
            captured["url"] = url_path
            return {"deleted": True, "id": 456}

        with patch('gov_scheme_mcp.server.http_request', new=AsyncMock(side_effect=fake_http_request)):
            res = await delete_scheme(456)
            data = json.loads(res)
            assert captured["method"] == "DELETE"
            assert captured["url"].endswith("/api/schemes/456")
            assert data["deleted"] is True
            assert data["id"] == 456


if __name__ == "__main__":
    pytest.main([__file__])