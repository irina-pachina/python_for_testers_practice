from model.contact import Contact
import re


def test_contacts_home(app):
    contact_from_home = app.contact.get_contact_list()[0]
    contact_from_edit = app.contact.get_contact_from_edit_page(0)
    assert contact_from_home.all_phones_home == merge_phones_like_home(contact_from_edit)


def test_contacts_view(app):
    contact_from_view = app.contact.get_contact_from_view_page(0)
    contact_from_edit = app.contact.get_contact_from_edit_page(0)
    assert merge_phones_like_home(contact_from_view) == merge_phones_like_home(contact_from_edit)


def clear(string):
    return re.sub("[() -]", "", string)


def merge_phones_like_home(contact):
    return "\n".join(filter(lambda x: x != "",
                            (map(lambda x: clear(x),
                                 filter(lambda x: x is not None,
                                        [contact.tele_home, contact.tele_mobile, contact.tele_work, contact.tele_second])))))
