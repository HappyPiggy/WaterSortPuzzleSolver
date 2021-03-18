class Stack(object):
    def __init__(self, stack=None):
        self.stack = stack if stack else list()

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def get_top(self):
        return self.stack[-1]

    def get_index(self, data):
        if data in self.stack:
            return self.size - (self.stack.index(data) + 1)
        return -1

    def get_data_by_index(self, index):
        if index >= self.size:
            return None
        data_index = self.size - 1 - index
        return self.stack[data_index]

    def get_all(self):
        copy_stack = list(self.stack)
        copy_stack.reverse()
        return copy_stack

    def is_empty(self):
        return self.size == 0

    @property
    def size(self):
        return len(self.stack)


uid = 0
def generate_uid():
    global uid
    uid += 1
    return uid
