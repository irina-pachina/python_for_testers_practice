from model.contact import Contact


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def open_add_new_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()

    def create(self, contact):
        wd = self.app.wd
        self.open_add_new_page()
        self.fill_contact_form(contact)
        wd.find_element_by_name("submit").click()
        self.return_to_home_page()

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.insert_value("firstname", contact.first_name)
        self.insert_value("home", contact.tele_home)
        # choosing from existing group
        self.choose_dropdown("new_group", contact.group)

    def insert_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def choose_dropdown(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            dropdown = wd.find_element_by_name(field_name)
            dropdown.find_element_by_xpath(f"//option[. = '{text}']").click()

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    def get_contact_list(self):
        wd = self.app.wd
        self.app.open_home_page()
        contact_list = []
        for element in wd.find_elements_by_css_selector("tr[name='entry']"):
            name = element.find_element_by_css_selector("td:nth-child(3)").text
            id = element.find_element_by_name("selected[]").get_attribute("value")
            contact_list.append(Contact(first_name=name, id=id))
        return contact_list
