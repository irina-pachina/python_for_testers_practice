from model.group import Group
from model.contact import Contact
import random


def test_add_contact_to_group(app, db_orm, check_ui):
    group_list = db_orm.get_group_list()
    if len(group_list) == 0:
        app.group.create(Group(name="for contact"))
        group_list = db_orm.get_group_list()
    contact_list = db_orm.get_contact_list()
    if len(contact_list) == 0:
        app.contact.create(Contact(first_name="for group"))
        contact_list = db_orm.get_contact_list()
    contact = random.choice(contact_list)
    group = random.choice(group_list)
    contacts_in_group_before = db_orm.get_contacts_in_group(group)
    app.contact.add_to_group(contact, group)
    contacts_in_group_before.append(contact)
    contacts_in_group_after = db_orm.get_contacts_in_group(group)
    assert sorted(contacts_in_group_before, key=Contact.id_or_max) == sorted(contacts_in_group_after, key=Contact.id_or_max)

    if check_ui:
        contacts_in_group_ui = app.contact.get_contact_list()
        assert sorted(contacts_in_group_ui, key=Contact.id_or_max) == sorted(contacts_in_group_after, key=Contact.id_or_max)
