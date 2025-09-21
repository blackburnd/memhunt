"""Pytest configuration for memhunt tests"""
import pytest
import sys
import os

# Add the package root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def mock_context():
    """Fixture providing a mock context object"""
    from unittest.mock import Mock
    return Mock()


@pytest.fixture
def mock_request():
    """Fixture providing a mock request object"""
    from unittest.mock import Mock
    request = Mock()
    request.form = {}
    request.response = Mock()
    return request


@pytest.fixture
def memory_view():
    """Fixture providing a DebugView instance for memory testing"""
    from memhunt.browser.views import DebugView
    from unittest.mock import Mock
    
    context = Mock()
    request = Mock()
    request.form = {}
    request.response = Mock()
    
    return DebugView(context, request)


@pytest.fixture
def ref_count_view():
    """Fixture providing a RefCount view instance for testing"""
    from memhunt.browser.views import RefCount
    from unittest.mock import Mock
    
    context = Mock()
    request = Mock()
    request.form = {}
    request.response = Mock()
    
    return RefCount(context, request)
