from sys import maxsize


class Group:
    def __init__(self, name=None, header=None, footer=None, id=None):
        self.name = name
        self.header = header
        self.footer = footer
        self.id = id

    def __repr__(self):
        return f"name = {self.name}, id = {self.id}"

    def __eq__(self, other):
        # test data doesn't have id and such elements in old_groups should be compared only by name
        return self.name == other.name and (self.id == other.id or self.id is None or other.id is None)

    # when group list is sorted with added test data (old_groups) id is None.
    # method id_or_max makes element with empty id the last one
    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            # mazsize is max id in lists, usually used in python as maximum integer constant
            return maxsize
