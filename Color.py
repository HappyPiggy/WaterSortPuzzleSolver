

class Color(object):
    def __init__(self, color_id, count=1):
        self.id = color_id
        self.count = count

    def get_count(self):
        return self.count

    def add_count(self, count):
        self.count += count

    def sub_count(self, count):
        if self.count >= count:
            self.count -= count

    def is_valid(self):
        return self.count > 0
