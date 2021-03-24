from model.contact import Contact
import pytest
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10  # + string.punctuation
    return prefix + "".join([random.choice(symbols) for _i in range(random.randrange(maxlen))])


def random_phone(maxlen):
    symbols = string.digits  # + "()+/*@#"
    return "".join([random.choice(symbols) for _i in range(random.randrange(maxlen))])


testdata = [Contact(first_name=random_string("first", 5), last_name=random_string("last", 5), tele_home=random_phone(10),
                    tele_mobile=random_phone(10), tele_work=random_phone(10))
            for i in range(2)]


@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_add_contact(app, contact):
    old_contacts = app.contact.get_contact_list()
    app.contact.create(contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)

