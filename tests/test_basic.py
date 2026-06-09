"""Basic tests for MCPSentinel."""

import pytest
import asyncio


def test_import_mcpsentinel():
    """Test that mcpsentinel can be imported."""
    import mcpsentinel
    assert mcpsentinel.__version__ == "0.1.0"


def test_pytest_asyncio_plugin():
    """Test pytest-asyncio plugin is working."""
    assert asyncio.get_event_loop() is not None


@pytest.mark.asyncio
async def test_async_functionality():
    """Test basic async functionality."""
    async def sample_async_func():
        return "async works"
    
    result = await sample_async_func()
    assert result == "async works"


def test_basic_assertion():
    """Basic test to verify pytest is working."""
    assert True
    assert 1 + 1 == 2
