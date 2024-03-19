import os


class Directory:
    def __init__(self):
        self.__path = None
        self.path = None

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        if value is None:
            value = os.getcwd()

        if not isinstance(value, str):
            raise TypeError("path property value must be a str type or None")

        if self.path != value:
            self.__path = value
