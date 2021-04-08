from model.group import Group
import allure


def test_add_group(app, db, json_groups):
    group = json_groups
    with allure.step("Given a group list"):
        old_groups = db.get_group_list()
    with allure.step("When I add the group %s to the list" % group):
        app.group.create(group)
    # imitate occasional logout or failed test to check function "ensure_login"
    # app.session.logout()
    # hashing app.group.count() is redundant due to long execution in contrast with db request
    # assert len(old_groups) + 1 == app.group.count()
    with allure.step("Then the new group list is equal to the old list with the added group"):
        new_groups = db.get_group_list()
        old_groups.append(group)
        assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
