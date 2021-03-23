from model.contact import Contact
import re


def test_contacts_home(app):
    contact_from_home = app.contact.get_contact_list()[0]
    contact_from_edit = app.contact.get_contact_from_edit_page(0)
    assert contact_from_home.tele_home == clear(contact_from_edit.tele_home)
    assert contact_from_home.tele_mobile == clear(contact_from_edit.tele_mobile)
    assert contact_from_home.tele_work == clear(contact_from_edit.tele_work)
    assert contact_from_home.tele_second == clear(contact_from_edit.tele_second)


def test_contacts_view(app):
    contact_from_view = app.contact.get_contact_from_view_page(0)
    contact_from_edit = app.contact.get_contact_from_edit_page(0)
    assert contact_from_view.tele_home == contact_from_edit.tele_home
    assert contact_from_view.tele_mobile == contact_from_edit.tele_mobile
    assert contact_from_view.tele_work == contact_from_edit.tele_work
    assert contact_from_view.tele_second == contact_from_edit.tele_second


def clear(string):
    return re.sub("[() -]", "", string)