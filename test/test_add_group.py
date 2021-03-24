from model.group import Group
import pytest
import random
import string


# if generated ' symbol (string.punctuation) will cause failed test (it is a bug in the app)
def random_string(prefix, maxlen):
    symbols = string.ascii_letters +string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for _i in range(random.randrange(maxlen))])

# 1 case with all empty fields and 2 cases with all filled fields
testdata = [Group(name="", header="", footer="")] + \
           [Group(name=random_string("name", 5), header=random_string("header", 5), footer=random_string("footer", 5))
            for i in range(2)]


# 8 cases with combinations empty/filled
# testdata = [Group(name=name, header=header, footer=footer)
#             for name in ["", random_string("name", 5)]
#             for header in ["", random_string("header", 5)]
#             for footer in ["", random_string("footer", 5)]]


@pytest.mark.parametrize("group", testdata, ids=[repr(x) for x in testdata])
def test_add_group(app, group):
    old_groups = app.group.get_group_list()
    app.group.create(group)
    # imitate occasional logout or failed test to check function "ensure_login"
    # app.session.logout()
    assert len(old_groups) + 1 == app.group.count()
    new_groups = app.group.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
