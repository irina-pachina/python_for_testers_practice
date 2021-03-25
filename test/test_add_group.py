from model.group import Group
import pytest
from data.add_group import testdata
# or can import different variable as testdata
# from data.add_group import constant as testdata


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
