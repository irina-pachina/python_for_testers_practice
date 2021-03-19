from model.group import Group


def test_add_group(app):
    old_groups = app.group.get_group_list()
    app.group.create(Group(name="nameassert", header="header1", footer="footer1"))
    # imitate occasional logout or failed test to check function "ensure_login"
    # app.session.logout()
    new_groups = app.group.get_group_list()
    assert len(old_groups) + 1 == len(new_groups)

def test_add_empty_group(app):
    old_groups = app.group.get_group_list()
    app.group.create(Group(name="", header="", footer=""))
    new_groups = app.group.get_group_list()
    assert len(old_groups) + 1 == len(new_groups)