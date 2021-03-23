from model.group import Group
import random


def test_delete_random_group(app):
    if app.group.count() == 0:
        app.group.create(Group(name="to_delete"))
    old_groups = app.group.get_group_list()
    index = random.randrange(len(old_groups))
    app.group.delete_group_by_index(index)
    assert len(old_groups) - 1 == app.group.count()
    new_groups = app.group.get_group_list()
    old_groups[index:index+1] = []
    assert old_groups == new_groups
