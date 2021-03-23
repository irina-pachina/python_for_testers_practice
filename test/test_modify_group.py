from model.group import Group
import random


def test_modify_group_name(app):
    group_count = app.group.count()
    if group_count == 0:
        app.group.create(Group(name="to_modify", header="header_mod", footer="footer_mod"))
    old_groups = app.group.get_group_list()
    index = random.randrange(len(old_groups))
    group = Group(name="new name")
    group.id = old_groups[index].id
    app.group.modify_group_by_index(group, index)
    assert len(old_groups) == group_count
    new_groups = app.group.get_group_list()
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


def test_modify_group_header(app):
    group_count = app.group.count()
    if group_count == 0:
        app.group.create(Group(name="to_modify", header="header_mod", footer="footer_mod"))
    old_groups = app.group.get_group_list()
    index = random.randrange(len(old_groups))
    group = Group(header="header")
    group.name = old_groups[index].name
    group.id = old_groups[index].id
    app.group.modify_group_by_index(group, index)
    assert len(old_groups) == group_count
    new_groups = app.group.get_group_list()
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)

