class Card:
    def __init__(self, v):
        self.value = v

    def set_value(self, setter):
        self.value = setter

    def get_value(self):
        return self.value
