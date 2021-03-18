# coding=utf-8
from Utils import Stack, generate_uid
from Color import Color

GLASS_MAX_SIZE = 4


class Glass(object):
    def __init__(self):
        self.id = generate_uid()
        self.colors = Stack()
        self.max_count = GLASS_MAX_SIZE

    @property
    def empty_count(self):
        size = 0
        for color in self.colors.get_all():
            size += color.count
        return self.max_count - size

    def show(self):
        print '\nglass_id', self.id
        is_empty = self.is_empty()
        if not is_empty:
            for c in self.colors.get_all():
                print 'color_id: {0}, count: {1}'.format(c.id, c.get_count())
        else:
            print 'is_empty'

    def is_empty(self):
        return self.empty_count == self.max_count

    def is_single_color(self):
        return self.colors.size == 1

    def is_full(self):
        return self.empty_count <= 0

    def is_complete(self):
        return self.empty_count == 0 and self.colors.size == 1

    def set_colors(self, colors):
        self.colors = colors

    def get_colors(self):
        return self.colors

    def get_color_by_index(self, index=0):
        """index 0为栈顶"""
        color = self.colors.get_data_by_index(index)
        return color

    def get_index_by_color_id(self, color_id):
        for idx, c in enumerate(self.colors.get_all()):
            if c.id == color_id:
                return idx
        return -1

    def can_pour_in(self, new_color_id):
        if self.is_empty():
            return True
        if self.is_full():
            return False

        top_color = self.get_color_by_index()
        return top_color.id == new_color_id

    def pour_in(self, new_color_id, count):
        if not self.can_pour_in(new_color_id):
            return False
        add_count = min(self.empty_count, count)
        top_color = self.get_color_by_index()
        if top_color is not None:
            top_color.add_count(add_count)
        else:
            c = Color(new_color_id, count)
            self.colors.push(c)
        return True

    def can_pour_out(self):
        return not self.is_empty()

    def pour_out(self, count):
        if not self.can_pour_out():
            return False
        top_color = self.get_color_by_index()
        if top_color is not None:
            top_color.sub_count(count)
            if top_color.count <= 0:
                self.colors.pop()
            return True
        return False
