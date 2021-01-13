class Vector(object):
    def __init__(self, x=0, y=0):
        if isinstance(x, (tuple, list, Vector)) and len(x) == 2 and y == 0:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __getitem__(self, key):
        return self.tuple[key]

    def __iter__(self):
        return iter(self.tuple)

    def __add__(self, value):
        if isinstance(value, (int, float)):
            return Vector(self.x + value, self.y + value)
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            return Vector(self.x + value[0],
                          self.y + value[1])
        elif isinstance(value, Vector):
            return Vector(self.x + value.x,
                          self.y + value.y)
        else:
            raise TypeError(f"Can't add {type(value)} to Vector")

    def __sub__(self, value):
        return self + -value

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector(self.x * value,
                          self.y * value)
        else:
            raise TypeError(f"Can't multiple Vector by {type(value)}")

    def __truediv__(self, value):
        return self * (1/value)

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __neg__(self):
        return self * -1

    def __len__(self):
        return 2

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def tuple(self):
        return self.x, self.y
