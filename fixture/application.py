# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from fixture.session import SessionHelper
from fixture.group import GroupHelper
from fixture.contact import ContactHelper


# class Application represents a complex fixture.
# contains a link to the driver, methods that interact with the browser through the driver
# and perform primitive actions. it provides high-level methods, i.e. login, group_creation
#
class Application:
    def __init__(self, browser, stand_url):
        # self.wd = WebDriver()
        if browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "firefox":
            self.wd = webdriver.Firefox()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        # self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.stand_url = stand_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.stand_url)

    def destroy(self):
        self.wd.quit()