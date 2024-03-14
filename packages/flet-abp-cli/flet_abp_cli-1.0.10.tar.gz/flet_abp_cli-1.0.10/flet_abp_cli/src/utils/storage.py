class Storage:
    """
    Класс хранилища

    После set(), если уверены что объект с ключом key сущестует можно обращаться storage.key
    """
    def __init__(self, data: dict = None):
        self.data = {}
        if data is not None:
            self.data = data

    def set(self, key, value):
        self.data[key] = value
        setattr(self, key, value)

    def pop(self, key):
        if self.get_or_none(key):
            delattr(self, key)
            return self.data.pop(key)

    def get(self, key):
        return self.data[key]

    def get_or_none(self, key):
        return self.data.get(key, None)


storage = Storage()
