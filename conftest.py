# in pytest "conftest" makes fixture function accessible to all tests
import pytest
from fixture.application import Application


# in pytest fixture is passed it test functions as parameter
# this way there is no need in test class, test functions are isolated
# to declare function as fixture use:
# scope = "session" means that fixture is created once for all tests
@pytest.fixture(scope = "session")
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture
