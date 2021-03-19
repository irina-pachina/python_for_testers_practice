from selenium.webdriver.chrome.webdriver import WebDriver
from fixture.session import SessionHelper
from fixture.group import GroupHelper
from fixture.contact import ContactHelper


# class Application represents a complex fixture.
# contains a link to the driver, methods that interact with the browser through the driver
# and perform primitive actions. it provides high-level methods, i.e. login, group_creation
#
class Application:
    def __init__(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get("http://addressbook/")

    def destroy(self):
        self.wd.quit()