import json

class JSONTable:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def lookup(self, name):
        for item in self.data:
            if item.get("Name") == name:
                return item
        return None

    def add(self, name, srv):
        new_item = {"Name": name, "Service": srv}
        self.data.append(new_item)
        self.save()
