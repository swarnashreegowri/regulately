import pytest
import tests.utils

@pytest.fixture
def client():
    return tests.utils.Client()
