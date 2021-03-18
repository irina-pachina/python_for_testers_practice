class ContactHelper:
    def __init__(self, app):
        self.app = app

    def open_add_new_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()

    def create(self, contact):
        wd = self.app.wd
        self.open_add_new_page()
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").send_keys(contact.first_name)
        wd.find_element_by_name("home").click()
        wd.find_element_by_name("home").send_keys(contact.tele_home)
        wd.find_element_by_name("new_group").click()
        # choosing from existing group
        dropdown = wd.find_element_by_name("new_group")
        dropdown.find_element_by_xpath(f"//option[. = '{contact.group}']").click()
        wd.find_element_by_css_selector("input:nth-child(87)").click()