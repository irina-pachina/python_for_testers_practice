from model.group import Group


def test_add_group(app, db, json_groups):
    group = json_groups
    old_groups = db.get_group_list()
    app.group.create(group)
    # imitate occasional logout or failed test to check function "ensure_login"
    # app.session.logout()
    # hashing app.group.count() is redundant due to long execution in contrast with db request
    # assert len(old_groups) + 1 == app.group.count()
    new_groups = db.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
