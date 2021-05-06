class Stone:
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        if isinstance(other, Stone):
            return self.string == other.string
        else:
            return False

    def __ne__(self, other):
        return not (self == other)


Red    = Stone("R")
Yellow = Stone("Y")
Empty  = Stone(" ")

