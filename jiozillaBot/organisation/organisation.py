import hashlib

class Organisation:
    def __init__(self, name):
        self.name = name;
        self.id = int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    def getName(self):
        return self.name
    
    def getId(self):
        return self.id


