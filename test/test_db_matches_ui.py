from model.group import Group


# both fixtures app and db are needed to compare lists
def test_group_list(app, db):
    ui_list = app.group.get_group_list()

    def clean(group):
        return Group(id=group.id, name=group.name.strip())
    db_list = map(clean, db.get_group_list())
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)
