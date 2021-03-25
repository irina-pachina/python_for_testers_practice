# in pytest "conftest" makes fixture function accessible to all tests
import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application
from fixture.database import DataBase


fixture = None
target = None


def load_config(config):
    global target
    if target is None:
        # w/o __file__ 'tricks' "target.json" will tried to be open in current directory
        # i.e. in ../test or Configuration>Working Directory
        # thus config path should be stored in root directory and 'built' from current one
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config)
        with open(config_path) as file:
            target = json.load(file)
    return target


# in pytest fixture is passed it test functions as parameter
# this way there is no need in test class, test functions are isolated
# to declare function as fixture use:
# fixture initialization
# this fixture use class Application to work only with browser
@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, stand_url=web_config["standURL"])
    fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


# this fixture use class DataBase to work only with db
@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    db_fixture = DataBase(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])

    def finalizer():
        db_fixture.destroy()

    request.addfinalizer(finalizer)
    return db_fixture


@pytest.fixture(scope="session")
def check_ui(request):
    return request.config.getoption("--check_ui")


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
    parser.addoption("--check_ui", action="store_true")
    # the rest of parameters are stored in config file
    parser.addoption("--target", action="store", default="target.json")


# pytest_generate_tests hook function is called when collecting a test function
# to make parametrization dynamic and custom
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
