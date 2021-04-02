from model.group import Group
from model.contact import Contact
import random


def test_delete_contact_from_group(app, db_orm, check_ui):
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
        app.contact.add_to_group(contact, group)

    group = random.choice(group_list)
    contacts_in_group_before = db_orm.get_contacts_in_group(group)
    contacts_not_in_group_before = db_orm.get_contacts_not_in_group(group)
    if len(contacts_in_group_before) == 0:
        contact_list = db_orm.get_contact_list()
        if len(contact_list) == 0:
            app.contact.create(Contact(first_name="for group"))
            contact_list = db_orm.get_contact_list()

        contact = random.choice(contact_list)
        app.contact.add_to_group(contact, group)
        contacts_in_group_before.append(contact)

    contact = random.choice(contacts_in_group_before)
    app.contact.delete_from_group(contact, group)

    contacts_in_group_after = db_orm.get_contacts_in_group(group)
    contacts_in_group_before = [c for c in contacts_in_group_before if c != contact]
    assert sorted(contacts_in_group_before, key=Contact.id_or_max) == sorted(contacts_in_group_after,
                                                                             key=Contact.id_or_max)

    contacts_not_in_group_before.append(contact)
    contacts_not_in_group_after = db_orm.get_contacts_not_in_group(group)
    assert sorted(contacts_not_in_group_before, key=Contact.id_or_max) == sorted(contacts_not_in_group_after,
                                                                                 key=Contact.id_or_max)

