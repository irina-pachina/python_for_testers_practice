# in pytest "conftest" makes fixture function accessible to all tests
import pytest
from fixture.application import Application


fixture = None

# in pytest fixture is passed it test functions as parameter
# this way there is no need in test class, test functions are isolated
# to declare function as fixture use:

# fixture initialization
@pytest.fixture
def app():
    global fixture
    if fixture is None:
        fixture = Application()
        fixture.session.login(username="admin", password="secret")
    else:
        if not fixture.is_valid():
            fixture = Application()
            fixture.session.login(username="admin", password="secret")
    return fixture


# fixture finalization
# scope = "session" means that fixture is created once for all tests
# in pytest "autouse" call fixture automatically
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.logout()
        fixture.destroy()

    request.addfinalizer(finalizer)
    return fixture
