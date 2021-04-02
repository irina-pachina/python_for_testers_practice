from model.contact import Contact
import re


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
        self.contact_cache = None

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.insert_value("firstname", contact.first_name)
        self.insert_value("lastname", contact.last_name)
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
            dropdown.find_element_by_xpath(f".//option[. = '{text}']").click()

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            # self.app.open_home_page()
            self.contact_cache = []
            # wd.find_elements_by_css_selector("tr[name='entry']")
            for element in wd.find_elements_by_name("entry"):
                # name = element.find_element_by_css_selector("td:nth-child(3)").text
                # id = element.find_element_by_name("selected[]").get_attribute("value")
                cells = element.find_elements_by_tag_name("td")
                first_name = cells[2].text
                last_name = cells[1].text
                id = cells[0].find_element_by_tag_name("input").get_attribute("value")
                all_phones = cells[5].text
                self.contact_cache.append(
                    Contact(first_name=first_name, last_name=last_name, id=id, all_phones_home=all_phones))
        return list(self.contact_cache)

    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    def open_view_contact_page(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_view_contact_page(index)
        text = wd.find_element_by_id("content").text
        tele_home = re.search("H: (.*)", text).group(1) if re.search("H: (.*)", text) else ""
        tele_mobile = re.search("M: (.*)", text).group(1) if re.search("M: (.*)", text) else ""
        tele_work = re.search("W: (.*)", text).group(1) if re.search("W: (.*)", text) else ""
        tele_second = re.search("P: (.*)", text).group(1) if re.search("P: (.*)", text) else ""
        return Contact(tele_home=tele_home, tele_mobile=tele_mobile, tele_work=tele_work, tele_second=tele_second)

    def open_edit_contact_page(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def get_contact_from_edit_page(self, index):
        wd = self.app.wd
        self.open_edit_contact_page(index)
        first_name = wd.find_element_by_name("firstname").get_attribute("value")
        last_name = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        tele_home = wd.find_element_by_name("home").get_attribute("value")
        tele_mobile = wd.find_element_by_name("mobile").get_attribute("value")
        tele_work = wd.find_element_by_name("work").get_attribute("value")
        tele_second = wd.find_element_by_name("phone2").get_attribute("value")
        return Contact(first_name=first_name, last_name=last_name, tele_home=tele_home, tele_mobile=tele_mobile,
                       tele_work=tele_work, tele_second=tele_second, id=id)

    def add_to_group(self, contact, group):
        wd = self.app.wd
        self.app.open_home_page()
        self.choose_dropdown("to_group", group.name)
        wd.find_element_by_name("to_group").click()
        wd.find_element_by_id(contact.id).click()
        wd.find_element_by_name("add").click()
        wd.find_element_by_link_text(f'group page "{group.name}"').click()

    def delete_from_group(self, contact, group):
        wd = self.app.wd
        self.app.open_home_page()
        self.choose_dropdown("group", group.name)
        wd.find_element_by_name("group").click()
        wd.find_element_by_id(contact.id).click()
        wd.find_element_by_name("remove").click()
        wd.find_element_by_link_text(f'group page "{group.name}"').click()
