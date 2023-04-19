class Space:
    def __init__(self, ids, occupied, res):
        self.id = ids
        self.occupied = occupied
        self.type = res

    def get_occupied(self):
        return self.occupied

    def set_occupied(self, change):
        self.occupied = change

    def get_type(self):
        return self.type

    def to_string(self):
        return str(self.occupied) + ', ' + str(self.type)
