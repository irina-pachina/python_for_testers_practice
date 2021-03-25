from model.group import Group
from timeit import timeit


# both fixtures app and db are needed to compare lists
def test_group_list(app, db):
    ui_list = app.group.get_group_list()
    # ui requests are slower than db ones: 2.1 against 0.0007266
    print(timeit(lambda: app.group.get_group_list(), number=1))

    def clean(group):
        return Group(id=group.id, name=group.name.strip())
    db_list = map(clean, db.get_group_list())
    print(timeit(lambda: map(clean, db.get_group_list()), number=1))
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)
