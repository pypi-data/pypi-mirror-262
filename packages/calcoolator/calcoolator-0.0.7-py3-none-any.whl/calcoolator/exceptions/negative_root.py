class NegativeRootError(Exception):

    def __init__(self, n, value):
        self.n = n
        self.value = value
        self.message = f"{n}√{value} I don't undertand complex numbers, sorry 💅🏻"
        super().__init__(self.message)