"""Pytest configuration and shared fixtures."""

import asyncio
from typing import Generator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

# TODO: Uncomment when these modules are created
# from pipeline.config.settings import Settings
# from pipeline.core.pipeline import Pipeline


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Commented out until Settings and Pipeline modules are created
# @pytest.fixture
# def test_settings() -> Settings:
#     """Create test settings with overrides for testing."""
#     settings = Settings(
#         environment="test",
#         debug=True,
#         database={"host": "localhost", "name": "test_pipeline"},
#         logging={"level": "DEBUG"},
#     )
#     return settings


# @pytest.fixture
# def mock_settings(mocker: MockerFixture) -> Mock:
#     """Create mock settings for testing."""
#     mock_settings = mocker.Mock(spec=Settings)
#     mock_settings.environment = "test"
#     mock_settings.debug = True
#     mock_settings.batch_size = 100
#     mock_settings.max_workers = 2
#     return mock_settings


# @pytest.fixture
# def pipeline(test_settings: Settings) -> Pipeline:
#     """Create a pipeline instance with test settings."""
#     return Pipeline(config=test_settings)


# @pytest.fixture
# def mock_pipeline(mocker: MockerFixture) -> Mock:
#     """Create a mock pipeline for testing."""
#     return mocker.Mock(spec=Pipeline)


@pytest.fixture
def sample_data() -> dict:
    """Provide sample data for testing."""
    return {
        "id": "test-123",
        "name": "Test Record",
        "value": 42,
        "tags": ["test", "sample"],
        "metadata": {"created_by": "test_user", "priority": "high"},
    }


@pytest.fixture
def sample_batch_data() -> list:
    """Provide sample batch data for testing."""
    return [{"id": f"test-{i}", "value": i, "batch": "test_batch"} for i in range(10)]


# Async fixtures for testing async code
# @pytest.fixture
# async def async_pipeline(test_settings: Settings) -> Pipeline:
#     """Create an async pipeline instance."""
#     pipeline = Pipeline(config=test_settings)
#     yield pipeline
#     # Cleanup if needed


# Database fixtures (if using a test database)
@pytest.fixture
def test_db_url() -> str:
    """Provide test database URL."""
    return "sqlite:///:memory:"


# Mock external services
@pytest.fixture
def mock_external_api(mocker: MockerFixture) -> Mock:
    """Mock external API calls."""
    return mocker.Mock()


@pytest.fixture(autouse=True)
def configure_test_logging(caplog):
    """Configure logging for tests."""
    import logging

    # Set logging level to capture all logs in tests
    caplog.set_level(logging.DEBUG)


# Markers for test categorization
pytest_plugins = ["pytest_asyncio"]


# Add custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line(
        "markers", "requires_database: mark test as requiring database"
    )
    config.addinivalue_line("markers", "requires_redis: mark test as requiring Redis")

