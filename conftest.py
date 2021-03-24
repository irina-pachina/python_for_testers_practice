# in pytest "conftest" makes fixture function accessible to all tests
import pytest
from fixture.application import Application


fixture = None


# in pytest fixture is passed it test functions as parameter
# this way there is no need in test class, test functions are isolated
# to declare function as fixture use:
# fixture initialization
@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    stand_url = request.config.getoption("--standURL")
    if fixture is None:
        fixture = Application(browser=browser, stand_url=stand_url)
    else:
        if not fixture.is_valid():
            fixture = Application(browser=browser, stand_url=stand_url)
    fixture.session.ensure_login(username="admin", password="secret")
    return fixture


# fixture finalization
# scope = "session" means that fixture is created once for all tests
# in pytest "autouse" call fixture automatically
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(finalizer)
    return fixture


# hook function when running from command line
# (dest) D:\code\python_software_testing>py.test --browser=firefox test\test_delete_group.py
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--standURL", action="store", default="http://addressbook/")
