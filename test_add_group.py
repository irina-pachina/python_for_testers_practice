import pytest
from group import Group
from application import Application


# in pytest fixture is passed it test functions as parameter
# this way there is no need in test class, test functions are isolated
# to declare function as fixture use:
@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_add_group(app):
    app.login(username="admin", password="secret")
    app.group_creation(Group(name="name1", header="header1", footer="footer1"))
    app.logout()


def test_add_empty_group(app):
    app.login(username="admin", password="secret")
    app.group_creation(Group(name="", header="", footer=""))
    app.logout()
