from sys import maxsize


class Contact:
    def __init__(self, first_name=None, last_name=None, tele_home=None, tele_mobile=None, tele_work=None,
                 tele_second=None, group=None, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.tele_home = tele_home
        self.tele_mobile = tele_mobile
        self.tele_work = tele_work
        self.tele_second = tele_second
        self.group = group
        self.id = id

    def __repr__(self):
        return f"{self.first_name} {self.last_name}, id = {self.id}"

    def __eq__(self, other):
        # test data doesn't have id and such elements in old_contacts should be compared only by name
        return self.first_name == other.first_name and self.last_name == other.last_name \
               and (self.id == other.id or self.id is None or other.id is None)

    # when contact list is sorted with added test data (old_contacts) id is None.
    # method id_or_max makes element with empty id the last one
    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            # maxsize is max id in lists, usually used in python as maximum integer constant
            return maxsize
