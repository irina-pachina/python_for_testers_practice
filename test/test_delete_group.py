from model.group import Group
import random


def test_delete_random_group(app, db):
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="to_delete"))
    old_groups = db.get_group_list()

    # delete by index works incorrect because of different order on ui and in db
    # index = random.randrange(len(old_groups))
    # app.group.delete_group_by_index(index)
    group = random.choice(old_groups)
    app.group.delete_group_by_id(group.id)

    # hashing app.group.count() is redundant due to long execution in contrast with db request
    # assert len(old_groups) - 1 == app.group.count()
    new_groups = db.get_group_list()
    old_groups.remove(group)
    assert old_groups == new_groups
