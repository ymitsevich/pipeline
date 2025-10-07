"""
Tests for api_client module demonstrating pytest with requests.

Key concepts:
- Mocking HTTP requests to avoid real network calls
- Parametrize for testing multiple scenarios
- Fixtures for reusable test setup
"""

import pytest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout, ConnectionError, HTTPError
from src.pipeline.api_client import (
    robust_api_call,
    APIClient,
    create_session_with_retries,
)


# ===== FIXTURES =====


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"id": 1, "login": "testuser"}
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def api_client():
    """Create an APIClient instance for testing."""
    client = APIClient(
        base_url="https://api.example.com",
        timeout=5,
        max_retries=2,
    )
    yield client
    client.close()


# ===== BASIC REQUEST TESTS =====


@patch("src.pipeline.api_client.requests.get")
def test_robust_api_call_success(mock_get, mock_response):
    """Test successful API call."""
    mock_get.return_value = mock_response

    result = robust_api_call("https://api.example.com/test")

    assert result["success"] is True
    assert result["data"]["login"] == "testuser"
    assert result["status_code"] == 200
    mock_get.assert_called_once_with("https://api.example.com/test", timeout=5)


@patch("src.pipeline.api_client.requests.get")
def test_robust_api_call_timeout(mock_get):
    """Test handling of timeout error."""
    mock_get.side_effect = Timeout("Connection timed out")

    result = robust_api_call("https://api.example.com/test", timeout=3)

    assert result["success"] is False
    assert "timed out" in result["error"]
    assert result["status_code"] is None


@patch("src.pipeline.api_client.requests.get")
def test_robust_api_call_connection_error(mock_get):
    """Test handling of connection error."""
    mock_get.side_effect = ConnectionError("Failed to connect")

    result = robust_api_call("https://api.example.com/test")

    assert result["success"] is False
    assert "Connection failed" in result["error"]


@patch("src.pipeline.api_client.requests.get")
def test_robust_api_call_http_error(mock_get):
    """Test handling of HTTP error (4xx/5xx)."""
    response = Mock()
    response.status_code = 404
    response.reason = "Not Found"
    response.raise_for_status.side_effect = HTTPError(response=response)
    mock_get.return_value = response

    result = robust_api_call("https://api.example.com/test")

    assert result["success"] is False
    assert "404" in result["error"]
    assert result["status_code"] == 404


# ===== PARAMETRIZED TESTS =====


@pytest.mark.parametrize(
    "status_code,expected_success",
    [
        (200, True),
        (201, True),
        (400, False),
        (404, False),
        (500, False),
    ],
)
@patch("src.pipeline.api_client.requests.get")
def test_robust_api_call_status_codes(mock_get, status_code, expected_success):
    """Test different HTTP status codes."""
    response = Mock()
    response.status_code = status_code
    response.json.return_value = {"status": "ok"}

    if status_code >= 400:
        response.raise_for_status.side_effect = HTTPError(response=response)
    else:
        response.raise_for_status.return_value = None

    mock_get.return_value = response

    result = robust_api_call("https://api.example.com/test")

    assert result["success"] == expected_success
    if expected_success:
        assert result["status_code"] == status_code


# ===== API CLIENT TESTS =====


def test_api_client_get(api_client, mock_response):
    """Test APIClient GET method."""
    with patch.object(api_client.session, "request", return_value=mock_response):
        result = api_client.get("/users/1")

        assert result["success"] is True
        assert result["data"]["login"] == "testuser"
        assert result["status_code"] == 200


def test_api_client_post(api_client, mock_response):
    """Test APIClient POST method."""
    with patch.object(api_client.session, "request", return_value=mock_response):
        result = api_client.post("/users", json={"name": "test"})

        assert result["success"] is True
        assert result["data"]["login"] == "testuser"


def test_api_client_url_construction(api_client):
    """Test that URLs are constructed correctly."""
    with patch.object(api_client.session, "request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        api_client.get("/users/1")

        called_url = mock_request.call_args[0][1]
        assert called_url == "https://api.example.com/users/1"


def test_api_client_timeout_error(api_client):
    """Test APIClient handles timeout."""
    with patch.object(api_client.session, "request", side_effect=Timeout):
        result = api_client.get("/users/1")

        assert result["success"] is False
        assert "timed out" in result["error"]


# ===== SESSION TESTS =====


def test_create_session_with_retries():
    """Test session creation with retry configuration."""
    session = create_session_with_retries(
        retries=5,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503),
    )

    assert session is not None
    adapter = session.get_adapter("https://example.com")
    assert adapter.max_retries.total == 5
    assert adapter.max_retries.backoff_factor == 0.5


# ===== INTEGRATION-STYLE TESTS (still mocked but more realistic) =====


@pytest.mark.parametrize(
    "endpoint,params,expected_query",
    [
        ("/search", {"q": "python", "page": 1}, True),
        ("/users/123", None, False),
    ],
)
def test_api_client_with_params(
    api_client, mock_response, endpoint, params, expected_query
):
    """Test API client with query parameters."""
    with patch.object(
        api_client.session, "request", return_value=mock_response
    ) as mock_request:
        result = api_client.get(endpoint, params=params)

        assert result["success"] is True
        if expected_query:
            assert mock_request.call_args[1].get("params") == params

