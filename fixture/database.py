import mysql.connector
from model.group import Group
from model.contact import Contact


class DataBase:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password)
        # autocommit mode means data are committed after every transaction
        self.connection.autocommit = True

    def get_group_list(self):
        group_list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT group_id, group_name, group_header, group_footer FROM group_list")
            for row in cursor:
                (id, name, header, footer) = row
                group_list.append(Group(name=name, header=header, footer=footer, id=str(id)))
        finally:
            cursor.close()
        return group_list

    def get_contact_list(self):
        contact_list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, firstname, lastname FROM addressbook where deprecated='0000-00-00 00:00:00'")
            for row in cursor:
                (id, first_name, last_name) = row
                contact_list.append(Contact(first_name=first_name, last_name=last_name, id=str(id)))
        finally:
            cursor.close()
        return contact_list

    def destroy(self):
        self.connection.close()
