from datetime import datetime
from pony.orm import *
from model.contact import Contact
from model.group import Group


class ORM:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORM.ORMContact, table='address_in_groups', column='id', reverse='groups', lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        first_name = Optional(str, column='firstname')
        last_name = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')
        groups = Set(lambda: ORM.ORMGroup, table='address_in_groups', column='group_id', reverse='contacts', lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_ormgroup_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    @db_session
    def get_group_list(self):
        return self.convert_ormgroup_to_model(select(g for g in ORM.ORMGroup))

    def convert_ormcontact_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), first_name=contact.first_name, last_name=contact.last_name)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        return self.convert_ormcontact_to_model(select(c for c in ORM.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORM.ORMGroup if g.id == group.id))[0]
        return self.convert_ormcontact_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORM.ORMGroup if g.id == group.id))[0]
        return self.convert_ormcontact_to_model(
            select(c for c in ORM.ORMContact if c.deprecated is None and orm_group not in c.groups))