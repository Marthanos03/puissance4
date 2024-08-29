class NoGameFoundException(Exception):
    """class to handle exceptions"""
    def __init__(self):
        pass


class FullColumnException(Exception):
    """if the column is full"""
    def __init__(self, column: int):
        self.column = column


class NonExistingColumnException(Exception):
    """if the column doesn't exist"""
    def __init__(self, column: int):
        self.column = column


class AlreadyExistingPseudoException(Exception):
    """if the column doesn't exist"""
    def __init__(self, pseudo: str):
        self.pseudo = pseudo
