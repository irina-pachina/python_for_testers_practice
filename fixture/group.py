from model.group import Group


class GroupHelper:
    def __init__(self, app):
        self.app = app

    def open_groups_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("group.php") and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("groups").click()

    def create(self, group):
        wd = self.app.wd
        self.open_groups_page()
        wd.find_element_by_name("new").click()
        self.fill_group_form(group)
        wd.find_element_by_name("submit").click()
        self.return_to_group_page()

    def insert_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_group_form(self, group):
        self.insert_value("group_name", group.name)
        self.insert_value("group_header", group.header)
        self.insert_value("group_footer", group.footer)

    def return_to_group_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("group page").click()

    def select_first_group(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def delete_first_group(self):
        wd = self.app.wd
        self.open_groups_page()
        self.select_first_group()
        wd.find_element_by_name("delete").click()
        self.return_to_group_page()

    def modify_first_group(self, new_data):
        wd = self.app.wd
        self.open_groups_page()
        self.select_first_group()
        # open modification form
        wd.find_element_by_name("edit").click()
        self.fill_group_form(new_data)
        wd.find_element_by_name("update").click()
        self.return_to_group_page()

    def count(self):
        wd = self.app.wd
        self.open_groups_page()
        return len(wd.find_elements_by_name("selected[]"))

    def get_group_list(self):
        wd = self.app.wd
        self.open_groups_page()
        group_list = []
        for element in wd.find_elements_by_css_selector("span.group"):
            name = element.text
            id = element.find_element_by_name("selected[]").get_attribute("value")
            group_list.append(Group(name=name, id=id))
        return group_list